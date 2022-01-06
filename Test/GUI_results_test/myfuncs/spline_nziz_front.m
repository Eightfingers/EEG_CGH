function nziz_front = spline_nziz_front(x, y)
% SPLINE_NZIZ_FRONT Reconstruct figure in SPLINETOOL.
%
%   SPLINE_NZIZ_FRONT(x, y) creates a plot, similar to the plot in
%   SPLINETOOL, using the data that you provide as input.
%   You can apply this function to the same data you used with SPLINETOOL
%   or with different data. You may want to edit the function to customize
%   the code or even this help message.
%
%   Because of data-dependent changes, this may not work for data sites
%   other than the ones used in SPLINETOOL when this file was written.

%   Make sure the data are in rows ...
x = x(:).'; y = y(:).';
% ... and start by plotting the data specific to the highlighted spline fit.

% firstbox = [0.1300  0.4900  0.7750  0.4850];
% subplot('Position',firstbox)
% plot(x,y,'ok'), hold on
% names={'data'};
% ylabel('y')
% xtick = get(gca,'Xtick');
% set(gca,'xtick',[])

% We are starting off with the least squares polynomial approximation of 
% order 4.
spline1 = spap2(1,6,x,y); 
% extract knots from current approximation:
knots = fnbrk(spline1,'knots'); 
% Least-squares approximation.
nziz_front = spap2(knots,6,x,y); 
% names{end+1} = 'spline1'; fnplt(spline1,'-',2)




% legend(names{:});
% hold off
% set(gcf,'NextPlot','replace');
