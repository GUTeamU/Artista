from pymatbridge import Matlab

def custom_filter(source, destination):
	mlab = Matlab(matlab='/usr/local/MATLAB/R2013a/bin/matlab')
	mlab.start()
	res = mlab.run_func('./lineDect.m', {'arg1': source, 'arg2':destination})
#print res['result']
