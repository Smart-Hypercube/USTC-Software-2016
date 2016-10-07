import numpy as np

from plugin import Plugin


class bio_simulation:
    def __init__(self, str_eqs, str_init):
        # parse equations to str arrays for further use
        self.eqs_arr = str.split(str_eqs, '\n')
        self.init_arr = str.split(str_init, '\n')

        # print(self.eqs_arr)
        # print(self.init_arr)

        # define defualt coef        
        start_t = 0
        end_t = 200
        step_l = 0.005

        self.start_t = start_t
        self.end_t = end_t
        self.step_l = step_l
        # print self.eqs_arr

    def run_sim(self):
        self.t_range = np.linspace(self.start_t, self.end_t, ((self.end_t - self.start_t) / self.step_l))
        # generate varable name : y[1] y[2]......        
        var_all = list(map(lambda x: "y" + str(x), range(1, len(self.eqs_arr) + 1)))
        self.data_all = np.zeros((len(self.eqs_arr), len(self.t_range) + 1))
        y = np.zeros(len(self.eqs_arr))

        index_init = 0
        for init_single_line in self.init_arr:
            parse_init = str.split(init_single_line, '=')
            self.data_all[index_init, 0] = parse_init[1]
            y[index_init] = parse_init[1]
            index_init = index_init + 1

        index_simu = 0
        for t in self.t_range:
            # get variabls ready
            index_var = 0
            for var_y in var_all:
                step_func = str.split(self.eqs_arr[index_var], '=')
                # print step_func
                self.data_all[index_var, index_simu + 1] = eval(step_func[1]) * self.step_l + self.data_all[
                    index_var, index_simu]
                index_var += 1

            y = self.data_all[:, index_simu + 1]
            index_simu += 1
        return 0

    def parse_data(self):
        return self.data_all

    def plot_data(self):
        plt.plot(self.t_range, self.data_all[0, 0:len(self.data_all[0, :]) - 1])
        plt.plot(self.t_range, self.data_all[1, 0:len(self.data_all[0, :]) - 1])
        plt.show()


'''
def main():
    str_eqs ="""# equations (one equation one line)
    dy0dt = 0.01*y[0] +0.005*y[1]
    dy1dt = 0.05*y[1]*(1-y[1]/2)
    # end line """
    str_init = """# init values
    y0 = 0.2
    y1 = 0.1
    # end line"""
    sim = bio_simulation(str_eqs, str_init)
    sim.run_sim()
    print(repr(list(map(list, sim.data_all))))
    sim.plot_data()
if __name__ in ("plugins.simulation", '__main__'):
    main()
'''


class Simulation(Plugin):
    name = 'simulation'

    def process(self, request):
        str_eqs = request['eqs']
        str_init = request['init']
        sim = bio_simulation(str_eqs, str_init)
        sim.run_sim()
        # print(repr(list(map(list, sim.data_all))))
        return dict(result=repr(list(map(list, sim.data_all))))


__plugin__ = Simulation()
