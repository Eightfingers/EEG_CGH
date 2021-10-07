function output = test(b,h)
    addpath('Main/matlab_funcs/')
    addpath('Main/helper_funcs/helperfuncs')
    addpath('Main/matlab_funcs/')

    a = 0.5*(b.* h);
    x = [1,2,3]
    y = [1,2,3]
    plot(x,y)
    f1 = gcf; %current figure handle
    axesObjs = get(f1, 'Children');  %axes handles
    dataObjs = get(axesObjs, 'Children'); %handles t
    xdata_circum = get(dataObjs, 'XData'); 
    ydata_circum = get(dataObjs, 'YData');
    
    disp(xdata_circum)

    results = [1.2,2.3,3.56]
    label = {'kekw'}
    output =[label; results.'];

end