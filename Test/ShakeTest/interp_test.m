% x = 0:pi/4:2*pi; 
% v = sin(x);
% xq = 0:pi/16:2*pi;
% 
% figure
% vq1 = interp1(x,v,xq);
% plot(x,v,'o',xq,vq1,':.');
% xlim([0 2*pi]);
% title('(Default) Linear Interpolation');

%  a = [1 2; 1 2; 2 3; 2 4; 2 5; 4 2; 4 2; 1 3; 1 3; 4 5];
%  C2 = unique(a,'rows');
%  [C,ia,ic] = unique(a,'rows');
%  [count key] = hist(ic,unique(ic));