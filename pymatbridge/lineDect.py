from pymatbridge import Matlab
mlab = Matlab(matlab='/usr/local/MATLAB/R2013a/bin/matlab')
mlab.start()
res = mlab.run_func('/users/level3/1102103l/Desktop/pymatbridge/lineDect.m', {'arg1': '/users/level3/1102103l/Desktop/pymatbridge/fraser.jpg', 'arg2':'/users/level3/1102103l/Desktop/pymatbridge/saved.jpg'})
#print res['result']