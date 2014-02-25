from pymatbridge import Matlab
mlab = Matlab(matlab='/usr/local/MATLAB/R2013a/bin/matlab')
mlab.start()
res = mlab.run_func('/users/level3/1102103l/Desktop/pymatbridge/fiveandthree.m', {'arg1': 3, 'arg2': 5})
print res['result']

###http://stackoverflow.com/questions/2883189/calling-matlab-functions-from-python

