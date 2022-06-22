function output = test(b,h)
    addpath('Main/matlab_funcs/')
    addpath('Main/matlab_funcs/helperfuncs')
    addpath('Main/matlab_funcs/myfuncs')
    addpath('Main/matlab_funcs/30_9_2021')
    addpath('Main/matlab_funcs/6_10_2021')

    results = [1.2,2.3,3.56; 1.2, 1.4,1.6; 1 1 1]
    label = ["kekw", "kek2", "kek3"]
    output =[label; results];
    disp(output);
end