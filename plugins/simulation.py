'''
Potential exceptions:
Invoke construct function: 
    ParameterMissedError(Initial values don't match equations)
Invoke simulation:
    NameError(User use wrong variable name witch cannot be parsed)
    ZeroDivisionError()
    ValueError(Initial value cannot be converted to float number)

For the interface:
    Input:{
    'eqs': string,
    'init': string,
    'end_t': string,
    'step_l': string
    }
    Output:{
    'success': bool
    'result': repr(list)
    'ubstable': str(float)
    'lyapunov': repr(list)
    }

'''
from numpy import *
# from matplotlib import pyplot as plt
from scipy.integrate import odeint
from plugin import Plugin


class ParameterMissedError(Exception):
    pass


class bio_simulation:
    def __init__(self, str_eqs, str_init, start_t=0., end_t=20., step_l=0.005):
        # Clean all white space in input strings
        str_eqs = str_eqs.replace(' ', '')
        str_eqs = str_eqs.replace('\t', '')
        str_init = str_init.replace(' ', '')
        str_init = str_init.replace('\t', '')

        # Divide strings for parsing
        self.eqs_arr = str.split(str_eqs, '\n')
        self.init_arr = str.split(str_init, '\n')

        # Initial values and equations don't match
        if len(self.eqs_arr) != len(self.init_arr):
            raise ParameterMissedError

        self.start_t = start_t
        self.end_t = end_t
        self.step_l = step_l


    def func(self, y, t, eqs_arr):
        # Make a deep copy of eqs_arr
        eqs = list(eqs_arr)

        # Replace all variable to do eval()
        for i in range(len(eqs)):
            eqs[i] = eqs[i].replace('^', "**")

        dydt = list(map(eval, eqs))

        return dydt


    def run_sim(self, ratio=0.995):
        self.t_range = linspace(self.start_t, self.end_t, int((self.end_t - self.start_t) / self.step_l))

        # Get initial values
        y0 = []
        testy = []
        for init_single_line in self.init_arr:
            parse_init = str.split(init_single_line, '=')[1]
            y0.append(float(parse_init))

        # I recommend to modify interface to remove the following 2 lines.
        for i in range(len(self.eqs_arr)):
            self.eqs_arr[i] = self.eqs_arr[i].split('=')[1]

        # Solve DE system, for information about how to use odeint, please follow this link below:
        # http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html
        # self.data_all is a numpy.ndarray
        self.data_all = odeint(self.func, y0, self.t_range, args=(self.eqs_arr,))
        for i in y0:
            testy.append(ratio * i)

        test_res = odeint(self.func, testy, self.t_range, args=(self.eqs_arr,))
        res = (abs(test_res - self.data_all) / self.data_all) > (1 - ratio) * 1.5

        self.unstable = None
        counter = 0
        for i in range(len(res)):
            row = res[i, :]
            fc = 0
            for j in row:
                if j == False:
                    fc += 1
            # print(row, isUnstable)
            if fc <= 1:
                if counter == 2:
                    self.unstable = self.start_t + (i - 10) * self.step_l
                    # print(self.unstable)
                    break
                else:
                    counter += 1
            else:
                counter = 0

        self.data_all = self.data_all.transpose()
        self.lyapunov = log(abs((self.data_all[:, -1] - test_res.transpose()[:, -1]) / (array(y0) * (1 - ratio)))) / \
                        self.data_all.shape[1]
        # print(self.lyapunov)
        return 0


    def parse_data(self):
        return self.data_all

    '''
    def plot_data(self):
        for i in range(self.data_all.shape[0]):
            plt.plot(self.t_range, self.data_all[i, :], label='y' + str(i))

        if self.unstable is not None:
            plt.axvline(x=self.unstable, linewidth=3, color='r')
        plt.show()
    '''


'''
def main():
    str_eqs ="""dy0dt = -10*y[0] + 10*y[1]
    dy1dt = 28*y[0] - y[1]-y[0]*y[2]
    dy2dt = -8/3 * y[2] + y[0] * y[1]"""
    str_init = """y0 = 10
    y1 = 5
    y2 = 1.01"""

    #str_eqs = """dy0dt = 3.8 * y[0] * (1 - y[0])"""
    #str_init = """y0= 0.5"""

    sim = bio_simulation(str_eqs, str_init)
    sim.run_sim()
    #print(repr(list(map(list, sim.data_all))))
    sim.plot_data()
if __name__ in ("plugins.simulation", '__main__'):
    main()

'''


class Simulation(Plugin):
    name = 'simulation'

    def process(self, request):
        str_eqs = request['eqs']
        str_init = request['init']

        end_t = float(request['end_t'])
        step_l = float(request['step_l'])
        sim = bio_simulation(str_eqs, str_init, 0, end_t, step_l)
        sim.run_sim()

        # May be you should modify this line below to satify your interface
        return dict(result=repr(list(map(list, sim.data_all))), unstable=self.unstable,
                    lyapunov=repr(self.lyapunov))


__plugin__ = Simulation()
