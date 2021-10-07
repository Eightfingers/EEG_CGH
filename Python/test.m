function output = test(b,h)
    addpath('Main/matlab_funcs/')
    addpath('Main/matlab_funcs/helperfuncs')
    addpath('Main/matlab_funcs/myfuncs')
    addpath('Main/matlab_funcs/30_9_2021')
    addpath('Main/matlab_funcs/6_10_2021')

    a = 0.5*(b.* h);
    x = [1,2,3]
    y = [1,2,3]
    % plot(x,y)
    f1 = gcf; %current figure handle
    axesObjs = get(f1, 'Children');  %axes handles
    dataObjs = get(axesObjs, 'Children'); %handles t
    xdata_circum = get(dataObjs, 'XData'); 
    ydata_circum = get(dataObjs, 'YData');
    
    results = [1.2,2.3,3.56; 1.2, 1.4,1.6;]
    label = ["kekw", "kek2", "kek3"]
    output =[label; results];
    disp(output);
end