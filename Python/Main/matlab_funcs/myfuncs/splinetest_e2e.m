function spline_e2e = splinetest_e2e(x, y)
% SPLINETEST_E2E Reconstruct figure in SPLINETOOL.
%
%   SPLINETEST_E2E(x, y) creates a plot, similar to the plot in SPLINETOOL,
%   using the data that you provide as input.
%   You can apply this function to the same data you used with SPLINETOOL
%   or with different data. You may want to edit the function to customize
%   the code or even this help message.
%
%   Because of data-dependent changes, this may not work for data sites
%   other than the ones used in SPLINETOOL when this file was written.

%   Make sure the data are in rows ...
x = x(:).'; y = y(:).';
% ... and start by plotting the data specific to the highlighted spline fit.
% f2 = figure( 'Name', 'Ear to Ear' );
% f2.Position = [10 10 550 400]; 

% plot(x,y,'ok'), hold on
% names={'2D Ear to Ear datapoints'};
% xlabel('X')
% ylabel('Y')
% xtick = get(gca,'Xtick');
% set(gca,'xtick',[])

spline1 = spap2(1,8,x,y); 
% extract knots from current approximation:
knots = fnbrk(spline1,'knots'); 
% Least-squares approximation.
spline_e2e = spap2(knots,8,x,y); 

% names{end+1} = 'spline fit- Ear to Ear'; fnplt(spline1,'-',2)
% legend(names{:});
% hold off
% set(gcf,'NextPlot','replace');
