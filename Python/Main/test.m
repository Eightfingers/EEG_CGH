function a = test(b,h)
    addpath('matlab_funcs')
    addpath('matlab_funcs/myfuncs')
    addpath('matlab_funcs/helperfuncs')
    addpath('matlab_funcs/30_9_2021')
%     addpath('matlab_funcs/6_10_2021')
    addpath('RecordedData');
    a = 0.5*(b.* h);
end