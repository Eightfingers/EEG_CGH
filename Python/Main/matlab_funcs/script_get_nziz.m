
% addpath('Main/RecordedData')
% addpath('C:\Users\65859\Desktop\eeg_cgh_main\Python\Main')
addpath('helperfuncs');
addpath('myfuncs');
addpath('6_10_2021');

%%% NZIZ
nziz_wand = readmatrix('data_NZIZstylus');

quaternions = readmatrix('rotation_data_NZIZspecs.csv'); % extract the rotation vector out

dis_matrix_nziz = readmatrix('data_NZIZspecs.csv'); % extract the displacement vector out

plot3(nziz_wand(:,1), nziz_wand(:,3), nziz_wand(:,2), 'o');
hold on;
plot3(dis_matrix_nziz(:,1), dis_matrix_nziz(:,3), dis_matrix_nziz(:,2), 'd');

% disp(rot_matrix_nziz);
% disp(nziz_wand);
% disp(dis_matrix_nziz);

dis_matrix_nziz = [dis_matrix_nziz(:,1), dis_matrix_nziz(:,3), dis_matrix_nziz(:,2)];
quaternions = [quaternions(:,4), quaternions(:,1), quaternions(:,2), quaternions(:,3)];

new_markers_nziz = [];
% Quaternion way

% for i = 1:1:length(nziz_wand)
%     quat_vector = quaternion(quaternions(i,:));
%     RPY1 = eulerd(quat_vector,'XYZ', 'frame' );
%     rot_vector_circum = [RPY1(1), RPY1(3), RPY1(2)];
%     dis_vector_nziz = dis_matrix_nziz(i,:);
%     wand_vector_nziz = [nziz_wand(i,1); ... % X,Y,Z 
%               nziz_wand(i,2); ...
%               nziz_wand(i,3); ...
%                1];
%     transform_matrix_circum = construct_matrix_transform_xyz(dis_vector_nziz, rot_vector_circum);    
%     new_vector_nziz = inv(transform_matrix_circum) * wand_vector_nziz;
%     new_markers_nziz = [new_markers_nziz; new_vector_nziz.';];
% end

%%% NZ-IZ
nziz_dataset =  nziz_wand;
nziz_dataset = rmmissing(nziz_dataset);
nziz_x = nziz_dataset(:,1);
nziz_y = nziz_dataset(:,2);
nziz_z = nziz_dataset(:,3); 

%% Perform Geometerical Fitting and Extract the datatips from the plots.
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
%% Predict EEG positions
%%% The EEG positions are determined using the conventional standard 10/20
%%% system. Here we are using the Distance Method/ Path Independant Method.
%%% The positions are predicted using the fractional arc length of the
%%% geometry usign the interparc() function. 

%%% NZIZ 
[pt20_nziz,~,~] = interparc(0,ydata_nziz,zdata_nziz,'spline');
[pt21_nziz,~,~] = interparc(0.1,ydata_nziz,zdata_nziz,'spline');
[pt22_nziz,~,~] = interparc(0.30,ydata_nziz,zdata_nziz,'spline');
[pt23_nziz,~,~] = interparc(0.50,ydata_nziz,zdata_nziz,'spline');
[pt24_nziz,~,~] = interparc(0.70,ydata_nziz,zdata_nziz,'spline');
[pt25_nziz,~,~] = interparc(0.95,ydata_nziz,zdata_nziz,'spline');
[pt26_nziz,~,~] = interparc(1,ydata_nziz,zdata_nziz,'spline');

%% Collate Data Points
%%% NZIZ
nziz = [pt25_nziz.' pt24_nziz.' pt23_nziz.' pt22_nziz.' pt21_nziz.'];

%% Find Shortest Euclidean Distance.
%%% The nearest point on the wanded data is found based on the predicted
%%% points. This is done such that we care able to determine the left out
%%% axis value for each data set. For this the Eudlidean distance between
%%% each predicted point and the wanded points are taken in the 2D plane. 

%%%NZ-IZ
A3 = [nziz_y nziz_z];
closest_array_nziz = find_closest_from_predicted_to_wanded(nziz, A3);

%%% NZIZ - The  NZIZ is orthogonally projected in the
%%% ZY plane and the X values need to be found. 
%%% If A(:,3)==closest(:,1) and A(:2)==closest(:,2). Then we need to extract
%%% that particular entire row and specifically its X value (1st column).

% nziz_dataset = unique(nziz_dataset, 'rows');
interpolate_closest_nziz = find_left_out_axis_values(closest_array_nziz, A3, nziz_dataset, 1, 2, 1);

% from_dataset = [1,1,1; 2,2,2; 3,3,3;]
% A4 = [from_dataset(:,2), from_dataset(:,2)];
% kekw = [5,5, 6,6]; 
% interpolate_test = find_left_out_axis_values(from_dataset, A3, nziz_dataset, 1, 2, 1);

trans_intrapolate_closest_nziz = interpolate_closest_nziz.';

%% Reorganize the data

%%% NZIZ 
final_nziz = [trans_intrapolate_closest_nziz; nziz(1:1,:); nziz(2:2,:)];
predicted_nziz = num2cell(final_nziz);
nziz_label = {'Fpz' 'Fz' 'Cz' 'Pz' 'Oz'};
final_nziz_label = [nziz_label;  predicted_nziz];
writecell(final_nziz_label,'NZIZ_POSITIONS__SADKASNDJJASNCJKX.csv') 
disp("ANSWER ISSSSS ");
disp(final_nziz_label);

plot3(final_nziz(1,:), final_nziz(2,:), final_nziz(3,:),'ro', 'MarkerSize', 20);
