from subprocess import Popen
from os import chdir


class InternalError(Exception):
    pass


class FileFormatError(Exception):
    pass


def ABACUS_prepare(path, file, abacuspath):
    chdir(abacuspath)
    chdir('.')
    p = Popen(["./ABACUS_prepare", path+file])
    while p.poll() is None:
        pass
    if p.poll():
        f = open(path+'err.log', 'r')
        exp = f.read(1E4)
        if exp.find("no protein chain detected") != -1:
            raise FileFormatError("File format error! No protein chain detected!")
        else:
            raise InternalError("We are sorry, something wrong happened")

    return p.poll()


def ABACUS_S1S2(path, file, abacuspath):
    chdir(abacuspath)
    chdir('.')
    p = Popen(["./ABACUS_S1S2", path+file])
    while p.poll() is None:
        pass
    if p.poll():
        raise InternalError("We are sorry, something wrong happened")

    return p.poll()


def ABACUS_vdwEtable(path, file, abacuspath):
    chdir(abacuspath)
    chdir('.')
    p = Popen(["./ABACUS_vdwEtable", path+file])
    while p.poll() is None:
        pass
    if p.poll():
        raise InternalError("We are sorry, something wrong happened")

    return p.poll()


def ABACUS_design(path, file, abacuspath, num, tag=None):
    chdir(abacuspath)
    chdir('.')
    if tag is None:
        p = Popen(["./ABACUS_design", path + file, str(num)])
    else:
        p = Popen(["./ABACUS_design", path + file, str(num), tag])

    while p.poll() is None:
        pass
    if p.poll():
        raise InternalError("We are sorry, something wrong happened")

    return p.poll()


def ABACUS_singleMutationScan(path, file, abacuspath, output, size=None):
    chdir(abacuspath)
    chdir('.')
    if size is None:
        p = Popen(["./ABACUS_singleMutationScan", path+file, output])
    else:
        p = Popen(["./ABACUS_singleMutationScan", path + file, output, size])

    while p.poll() is None:
        pass
    if p.poll():
        raise InternalError("We are sorry, something wrong happened")

    return p.poll()
