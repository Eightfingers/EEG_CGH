function a = test(b,h)
    addpath('matlab_funcs')
    addpath('matlab_funcs/myfuncs')
    addpath('matlab_funcs/helperfuncs')
    a = 0.5*(b.* h);
end