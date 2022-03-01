function [axis_1, axis_2] = splineplot(x_spline,y_spline)

    spline_plot = spap2(1,3,x_spline,y_spline); 
%     figure;
    points = fnplt(spline_plot,'-',2)
    axis_1 = points(1,:);
    axis_2 = points(2,:);
%     f2 = findobj(gcf,'Type','line');
%     x_fit=get(f2,'Xdata'); %// the x-axis vector smoothed data
%     y_fit=get(f2,'Ydata'); %// the y-axis vector smoothed data

end