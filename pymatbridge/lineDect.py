from pymatbridge import Matlab
mlab = Matlab(matlab='/usr/local/MATLAB/R2013a/bin/matlab')
mlab.start()
res = mlab.run_func('./lineDect.m', {'arg1': './fraser.jpg', 'arg2':'./saved.jpg'})
#print res['result']
