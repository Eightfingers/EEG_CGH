function [x_fit,y_fit] = splineplot(x_spline,y_spline)
    
    % Takes in a set x and y coordinate and returns a set of x coordinate fit and
    % y coordinate fit of a spline
    % Input: X and Y coordinates
    % Output: X and Y fit coordinates
    
    spline1 = spap2(1,3,x_spline,y_spline); 
    figure;
    fnplt(spline1,'-',2)

    f2 = findobj(gcf,'Type','line');
    x_fit=get(f2,'Xdata'); %// the x-axis vector smoothed data
    y_fit=get(f2,'Ydata'); %// the y-axis vector smoothed data

end

