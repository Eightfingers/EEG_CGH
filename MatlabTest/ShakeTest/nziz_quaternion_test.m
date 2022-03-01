%%% This code would be the final code that is used to determine the 17 EEG
%%% locations. 
%% Add to path different folders containing data and code
% addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept');
% addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\helperfuncs');
% addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\myfuncs');
% addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Data\30_9_2021');

addpath('helperfuncs\');
addpath('myfuncs\');
addpath('quaternion');

%%% NZIZ
nziz = readmatrix ('shake_nziz_16_11_2023.csv');
nziz_wand_position = [nziz(:,7), nziz(:,9), nziz(:,8)];
nziz_wand_position = rmmissing(nziz_wand_position);

scatter3(nziz_wand_position(:,1),nziz_wand_position(:,2),nziz_wand_position(:,3));
hold on;

nziz_specs = nziz(:,35:41); 
nziz_specs = rmmissing(nziz_specs);

rot_matrix_nziz = nziz_specs(:,1:4); % extract the rotation vector out
rot_matrix_nziz = [rot_matrix_nziz(:,4), rot_matrix_nziz(:,1), rot_matrix_nziz(:,3), rot_matrix_nziz(:,2)];
dis_matrix_nziz = nziz_specs(:,5:7); % extract the displacement vector out
dis_matrix_nziz = [dis_matrix_nziz(:,1), dis_matrix_nziz(:,3), dis_matrix_nziz(:,2)];

new_markers_nziz = transform_frame_quat(nziz_wand_position, rot_matrix_nziz, dis_matrix_nziz);
plot3(new_markers_nziz(:,1),new_markers_nziz(:,2),new_markers_nziz(:,3),'d');
hold on;

%%% NZ-IZ
nziz_dataset =  new_markers_nziz;
nziz_dataset = rmmissing(nziz_dataset);
nziz_x = nziz_dataset(:,1);
nziz_y = nziz_dataset(:,2);
nziz_z = nziz_dataset(:,3);
hold on
scatter3(nziz_x,nziz_y,nziz_z);

%%% NZ-IZ - The NZIZ tracking data is considered as a spline in
%%% 2D space. The data points are orthogonally projected on the 2D ZY plane
%%% and smoothing spline fitting is performed. The smoothing spline with is
%%% from the MATLAB curve fitting toolbox. Createfit1() is used here. The
%%% smoothing parameter used here is 0.999999662162161. 

%% There is something wrong with immideately doing a least square fit on the 
%% NZIZ data set so we need to split into 2 halves
%% And perform least square fit individually on the 2 halves
%% Then combine them back to get a better least square fitting of NZIZ.

size_of_nziz = size(nziz_dataset);
lengthof_nziz = size_of_nziz(:,1);
split_nziz =  lengthof_nziz/2;
split_nziz_round = round(split_nziz);

x_split_back = nziz_x(split_nziz_round+1 :lengthof_nziz);
y_split_back = nziz_y(split_nziz_round+1 :lengthof_nziz);
z_split_back = nziz_z(split_nziz_round+1 :lengthof_nziz);
nziz_back = spline_nziz_back(z_split_back,y_split_back);

points = fnplt(nziz_back,'-',2);
zdata_nziz_back = points(1,:);
ydata_nziz_back = points(2,:);

x_split_front = nziz_x(1 :split_nziz_round );
y_split_front = nziz_y(1 :split_nziz_round );
z_split_front = nziz_z(1 :split_nziz_round );
nziz_front = spline_nziz_front(y_split_front,z_split_front);

points = fnplt(nziz_front,'-',2);
ydata_nziz_front = points(1,:);
zdata_nziz_front = points(2,:);

%% Combine them back togather
ydata_nziz = [ydata_nziz_back ydata_nziz_front];
zdata_nziz = [zdata_nziz_back zdata_nziz_front];

figure;
hold on
scatter(ydata_nziz,zdata_nziz,'r*');
hold on
plot(ydata_nziz(1:1),zdata_nziz(1:1),'rs','MarkerSize',20);
hold on
plot(ydata_nziz(end),zdata_nziz(end),'ms','MarkerSize',20);

%%% NZIZ 
[pt20_nziz,~,~] = interparc(0,ydata_nziz,zdata_nziz,'spline');
[pt21_nziz,~,~] = interparc(0.1,ydata_nziz,zdata_nziz,'spline');
[pt22_nziz,~,~] = interparc(0.30,ydata_nziz,zdata_nziz,'spline');
[pt23_nziz,~,~] = interparc(0.50,ydata_nziz,zdata_nziz,'spline');
[pt24_nziz,~,~] = interparc(0.70,ydata_nziz,zdata_nziz,'spline');
[pt25_nziz,~,~] = interparc(0.95,ydata_nziz,zdata_nziz,'spline');
[pt26_nziz,~,~] = interparc(1,ydata_nziz,zdata_nziz,'spline');

%%% NZIZ
nziz = [pt25_nziz.' pt24_nziz.' pt23_nziz.' pt22_nziz.' pt21_nziz.'];

%%%NZ-IZ
A3 = [nziz_y nziz_z];
closest_array_nziz = find_closest_from_predicted_to_wanded(nziz, A3);

%%% NZIZ - The  NZIZ is orthogonally projected in the
%%% ZY plane and the X values need to be found. 
%%% If A(:,3)==closest(:,1) and A(:2)==closest(:,2). Then we need to extract
%%% that particular entire row and specifically its X value (1st column).
% unique_nziz_dataset = unique(nziz_dataset, 'rows');
% closest_array_nziz = unique(closest_array_nziz, 'rows');
interpolate_closest_nziz = find_left_out_axis_values(closest_array_nziz, nziz_dataset,1, 2, 1);
trans_intrapolate_closest_nziz = interpolate_closest_nziz.';

%%% NZIZ 
final_nziz = [trans_intrapolate_closest_nziz; nziz(1:1,:); nziz(2:2,:)];
plot3(final_nziz(1,:),final_nziz(2,:),final_nziz(3,:), 'ro', 'MarkerSize', 20); 
hold on
% plot3(final_nziz(1,1),final_nziz(2,1),final_nziz(3,1), 'rs','MarkerSize', 20); 
% plot3(final_nziz(1,2),final_nziz(2,2),final_nziz(3,2), 'bs','MarkerSize', 20); 
% plot3(final_nziz(1,3),final_nziz(2,3),final_nziz(3,3), 'gs','MarkerSize', 20); 
% plot3(final_nziz(1,4),final_nziz(2,4),final_nziz(3,4), 'ms','MarkerSize', 20); 
% plot3(final_nziz(1,5),final_nziz(2,5),final_nziz(3,5), 'ks','MarkerSize', 20); 
