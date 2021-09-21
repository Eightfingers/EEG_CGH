%%% This code would be the final code that is used to determine the 17 EEG
%%% locations. 
%% Add to path different folders containing data and code
addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept');
addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\helperfuncs');
addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\myfuncs');
addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Data\17_9_2021');
%% Load the different wanded data
%% Load the different wanded data
%%% Circumference
circumference = readmatrix('Specs_circum_17_9_2023.csv'); 
circum_wand = circumference(:,3:8); 
circum_wand = rmmissing(circum_wand);
hold on
scatter3(circum_wand(:,4), circum_wand(:,6),circum_wand(:,5));

circum_specs= circumference(:,34:39); 
circum_specs = rmmissing(circum_specs);
circum_specs = circum_specs(:, :); 

circum_specs = circum_specs(:, :);
rot_matrix_circum = circum_specs(:,1:3); % extract the rotation vector out
dis_matrix_circum = circum_specs(:,4:6); % extract the displacement vector out
dis_matrix_circum = [dis_matrix_circum(:,1), dis_matrix_circum(:,3), dis_matrix_circum(:,2)];
x_rot_circum = rot_matrix_circum(:,1);
y_rot_circum = rot_matrix_circum(:,3);
z_rot_circum = rot_matrix_circum(:,2);

new_markers_circum = [];
rot_matrix2_circum = rotx(-x_rot_circum(1)) * roty(-y_rot_circum(1)) * rotz(-z_rot_circum(1));
for i = 1:1:length(circum_wand)
    disp(i);
    rot_vector_circum = [-x_rot_circum(i), -y_rot_circum(i), -z_rot_circum(i)];
%     rot_vector = [-z_rot(i), -y_rot(i), -x_rot(i)];

    dis_vector_circum = dis_matrix_circum(i,:);
    transform_matrix_circum = construct_matrix_transform_xyz(dis_vector_circum, rot_vector_circum);    
    
    wand_vector_circum = [circum_wand(i,4); ... % X,Y,Z 
              circum_wand(i,6); ...
              circum_wand(i,5); ...
               1];

    new_vector_circum = inv(transform_matrix_circum) * wand_vector_circum;
    new_markers_circum = [new_markers_circum; new_vector_circum.';];
end

%%% Ear to Ear
ear2ear = readmatrix('Specs_ear2ear_17_9_2022.csv');
e2e_wand = ear2ear(:,3:8); 
e2e_wand = rmmissing(e2e_wand);
hold on
scatter3(e2e_wand(:,4), e2e_wand(:,6),e2e_wand(:,5));

e2e_specs= ear2ear(:,34:39); 
e2e_specs = rmmissing(e2e_specs);
e2e_specs = e2e_specs(:, :); 

e2e_specs = e2e_specs(:, :);
rot_matrix_e2e = e2e_specs(:,1:3); % extract the rotation vector out
dis_matrix_e2e = e2e_specs(:,4:6); % extract the displacement vector out
dis_matrix_e2e = [dis_matrix_e2e(:,1), dis_matrix_e2e(:,3), dis_matrix_e2e(:,2)];
x_rot_e2e = rot_matrix_e2e(:,1);
y_rot_e2e = rot_matrix_e2e(:,3);
z_rot_e2e = rot_matrix_e2e(:,2);
new_markers_e2e = [];
rot_matrix2_e2e = rotx(-x_rot_e2e(1)) * roty(-y_rot_e2e(1)) * rotz(-z_rot_e2e(1));
for i = 1:1:length(e2e_wand)
    disp(i);
    rot_vector_e2e = [-x_rot_e2e(i), -y_rot_e2e(i), -z_rot_e2e(i)];
%     rot_vector = [-z_rot(i), -y_rot(i), -x_rot(i)];

    dis_vector_e2e = dis_matrix_e2e(i,:);
    transform_matrix_e2e = construct_matrix_transform_xyz(dis_vector_e2e, rot_vector_e2e);    
    
    wand_vector_e2e = [e2e_wand(i,4); ... % X,Y,Z 
              e2e_wand(i,6); ...
              e2e_wand(i,5); ...
               1];

    new_vector_e2e = inv(transform_matrix_e2e) * wand_vector_e2e;
    new_markers_e2e = [new_markers_e2e; new_vector_e2e.';];
end

%%% NZIZ
nziz = readmatrix ('Specs_NZIZ_17_9_2021.csv');
nziz_wand = nziz(:,3:8); 
nziz_wand = rmmissing(nziz_wand);
hold on
scatter3(nziz_wand(:,4),nziz_wand(:,6),nziz_wand(:,5));

nziz_specs = nziz(:,34:39); 
nziz_specs = rmmissing(nziz_specs);
nziz_specs = nziz_specs(:, :); 

nziz_specs = nziz_specs(:, :);
rot_matrix_nziz = nziz_specs(:,1:3); % extract the rotation vector out
dis_matrix_nziz = nziz_specs(:,4:6); % extract the displacement vector out
dis_matrix_nziz = [dis_matrix_nziz(:,1), dis_matrix_nziz(:,3), dis_matrix_nziz(:,2)];
x_rot_nziz = rot_matrix_nziz(:,1);
y_rot_nziz = rot_matrix_nziz(:,3);
z_rot_nziz = rot_matrix_nziz(:,2);
new_markers_nziz = [];
rot_matrix2_nziz = rotx(-x_rot_nziz(1)) * roty(-y_rot_nziz(1)) * rotz(-z_rot_nziz(1));
for i = 1:1:length(nziz_wand)
    disp(i);
    rot_vector_nziz = [-x_rot_nziz(i), -y_rot_nziz(i), -z_rot_nziz(i)];
%     rot_vector = [-z_rot(i), -y_rot(i), -x_rot(i)];

    dis_vector_nziz = dis_matrix_nziz(i,:);
    transform_matrix_nziz = construct_matrix_transform_xyz(dis_vector_nziz, rot_vector_nziz);    
    
    wand_vector_nziz = [nziz_wand(i,4); ... % X,Y,Z 
              nziz_wand(i,6); ...
              nziz_wand(i,5); ...
               1];

    new_vector_nziz = inv(transform_matrix_nziz) * wand_vector_nziz;
    new_markers_nziz = [new_markers_nziz; new_vector_nziz.';];
end

%%% Static
static = readmatrix('static_all_001.csv'); 
static_wand = static(1,73:end); 
static_wand = rmmissing(static_wand);
D1 = [];
j = 1;
k = j +2 ;
while k <= length(static_wand)
    D1(end+1, :) = [static_wand(j:k)];
    j = j + 3;
    k = j + 2;
 
end 
static_wand = D1;

static_specs= static(:,3:8); 
static_specs = rmmissing(static_specs);
static_specs = static_specs(:, :); 

static_specs = static_specs(:, :);
rot_matrix_static = static_specs(:,1:3); % extract the rotation vector out
dis_matrix_static = static_specs(:,4:6); % extract the displacement vector out
dis_matrix_static = [dis_matrix_static(:,1), dis_matrix_static(:,3), dis_matrix_static(:,2)];
x_rot_static = rot_matrix_static(:,1);
y_rot_static = rot_matrix_static(:,3);
z_rot_static = rot_matrix_static(:,2);

new_markers_static = [];
rot_matrix2_static = rotx(-x_rot_static(1)) * roty(-y_rot_static(1)) * rotz(-z_rot_static(1));

for i = 1:1:length(static_wand)
    d = dis_matrix_static; % displacement vector
    v = [ 0, 0 ,0 1];
    rot_matrix = [-x_rot_static(i), -y_rot_static(i), -z_rot_static(i)];
    transform_matrix = construct_matrix_transform_xyz(d, rot_matrix);    
    marker = [static_wand(i,1); ... % X,Y,Z 
              static_wand(i,3); ...
              static_wand(i,2); ...
               1];
           
    new_vector = inv(transform_matrix) * marker;
    new_markers_static = [new_markers_static; new_vector.';];

end
%%
%%% Circumferene
circumference_dataset= new_markers_circum;
circumference_dataset = rmmissing(circumference_dataset);
circumference_x = circumference_dataset(:,1);
circumference_y = circumference_dataset(:,2);
circumference_z = circumference_dataset(:,3);
hold on
scatter3(circumference_x,circumference_y,circumference_z);

%%% Ear to Ear
e2e_dataset= new_markers_e2e;
e2e_dataset = rmmissing(e2e_dataset);
e2e_x = e2e_dataset(:,1);
e2e_y = e2e_dataset(:,2);
e2e_z = e2e_dataset(:,3);
scatter3(e2e_x,e2e_y,e2e_z);

%%% NZ-IZ
nziz_dataset =  new_markers_nziz;
nziz_dataset = rmmissing(nziz_dataset);
nziz_x = nziz_dataset(:,1);
nziz_y = nziz_dataset(:,2);
nziz_z = nziz_dataset(:,3);
scatter3(nziz_x,nziz_y,nziz_z);

%%% Static
static_dataset = new_markers_static;
static_x = static_dataset(:,1);
static_y = static_dataset(:,2);
static_z = static_dataset(:,3);
hold on
scatter3(static_x,static_y,static_z);
% hold on;
% plot3(nziz_x, nziz_y, nziz_z, 'd');
%% Perform Geometerical Fitting and Extract the datatips from the plots.

%%% Circumferene - The circumference is considered as and ellipse in 2D
%%% space. The points are orthogonally projected on the XZ plane and
%%% linear least squares ellipse fitting is performed usin fitellipse() &
%%% plotellipse()function
f1= figure('Name',' Circumference');
Ellipse=([circumference_x,circumference_y]);
[centre, a, b, alpha] = fitellipse(Ellipse,'linear');

plotellipse(centre, a, b, alpha, 'b-');
f1 = gcf; %current figure handle
axesObjs = get(f1, 'Children');  %axes handles
dataObjs = get(axesObjs, 'Children'); %handles t
xdata_circum = get(dataObjs, 'XData'); 
ydata_circum = get(dataObjs, 'YData');
start_A = circumference_dataset(1:1,:);

startpoint_2d_circum = [start_A(:,1) start_A(:,2)];
newmat_xy = [xdata_circum; ydata_circum];
trans_newmat_xy = newmat_xy.';
dist_startpoint_circum = sqrt(sum(bsxfun(@minus, trans_newmat_xy, startpoint_2d_circum).^2,2));
closest_startpoint_circum = trans_newmat_xy(find(dist_startpoint_circum==min(dist_startpoint_circum)),:);
[row_circum,~] = find(trans_newmat_xy==closest_startpoint_circum);
new_matrix_x_circum = [trans_newmat_xy(row_circum:2000,1); trans_newmat_xy(1:row_circum-1,1)].';
new_matrix_y_circum = [trans_newmat_xy(row_circum:2000,2); trans_newmat_xy(1:row_circum-1,2)].';

%%% Ear to Ear - The ear to ear tracking data is considered as a spline in
%%% 2D space. The data points are orthogonally projected on the 2D XY plane
%%% and smoothing spline fitting is performed. The smoothing spline with is
%%% from the MATLAB curve fitting toolbox. Createfit2() is used here. The
%%% smoothing parameter used here is 0.999999481874551. 

% Spline fit & extracting out the numerical X, Z data. 
spline_e2e = splinetest_e2e(e2e_x,e2e_z);
points = fnplt(spline_e2e);
xdata_e2e = points(1,:);
zdata_e2e = points(2,:);
%% The least square fit of the plot has excess length that exceed the starting 
%% and ending position of the e2e dataset. Uncomment the code below to see it.
% fnplt(spline_e2e);
% hold on;
% plot(e2e_x, e2e_z, 'o');

%% We fix this by finding the point on the fitted line that is closest to the actual e2e dataset.
%% And making the fitted line start and end nearest to the e2e starting and ending dataset.
% Get the starting and ending position of e2e dataset
start_B = e2e_dataset(1:1,:);
startpoint_2d_e2e = [start_B(:,1) start_B(:,3)];

end_B = e2e_dataset(end,:);
endpoint_2d_e2e = [end_B(:,1) end_B(:,3)];

newmat_xz = [xdata_e2e; zdata_e2e];
trans_newmat_xz = newmat_xz.';

dist_startpoint_e2e = sqrt(sum(bsxfun(@minus, trans_newmat_xz, startpoint_2d_e2e).^2,2));
closest_startpoint_e2e = trans_newmat_xz(find(dist_startpoint_e2e==min(dist_startpoint_e2e)),:);

dist_endpoint_e2e = sqrt(sum(bsxfun(@minus, trans_newmat_xz, endpoint_2d_e2e).^2,2));
closest_endpoint_e2e = trans_newmat_xz(find(dist_endpoint_e2e==min(dist_endpoint_e2e)),:);

[row_startpoint_e2e,~] = find(trans_newmat_xz==closest_startpoint_e2e);
[row_endpoint_e2e,~] = find(trans_newmat_xz==closest_endpoint_e2e);

new_matrix_x_e2e = [trans_newmat_xz(row_startpoint_e2e:row_endpoint_e2e,1)].';
new_matrix_z_e2e = [trans_newmat_xz(row_startpoint_e2e:row_endpoint_e2e,2)].';

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
ydata_nziz = [ydata_nziz_front ydata_nziz_back];
zdata_nziz = [zdata_nziz_front zdata_nziz_back];
% figure;
% scatter(ydata_nziz,zdata_nziz,'r*');
% hold on
% scatter(nziz_y,nziz_z);

%% Predict EEG positions
%%% The EEG positions are determined using the conventional standard 10/20
%%% system. Here we are using the Distance Method/ Path Independant Method.
%%% The positions are predicted using the fractional arc length of the
%%% geometry usign the interparc() function. 

%%% Circumference - 13 positions (first and last being the same)
[pt_circum,~,~] = interparc(0,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt1_circum,~,~] = interparc(0.05,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt2_circum,~,~] = interparc(0.15,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt3_circum,~,~] = interparc(0.25,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt4_circum,~,~] = interparc(0.35,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt5_circum,~,~] = interparc(0.45,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt6_circum,~,~] = interparc(0.50,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt7_circum,~,~] = interparc(0.55,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt8_circum,~,~] = interparc(0.65,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt9_circum,~,~] = interparc(0.75,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt10_circum,~,~] = interparc(0.85,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt11_circum,~,~] = interparc(0.95,new_matrix_x_circum,new_matrix_y_circum,'linear');
[pt12_circum,~,~] = interparc(1,new_matrix_x_circum,new_matrix_y_circum,'linear');

%%% Ear to Ear
[pt13_e2e,~,~] = interparc(0,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt14_e2e,~,~] = interparc(0.1,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt15_e2e,~,~] = interparc(0.3,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt16_e2e,~,~] = interparc(0.5,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt17_e2e,~,~] = interparc(0.7,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt18_e2e,~,~] = interparc(0.9,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt19_e2e,~,~] = interparc(1,new_matrix_x_e2e,new_matrix_z_e2e,'spline');

%%% NZIZ 
[pt20_nziz,~,~] = interparc(0,ydata_nziz,zdata_nziz,'spline');
[pt21_nziz,~,~] = interparc(0.1,ydata_nziz,zdata_nziz,'spline');
[pt22_nziz,~,~] = interparc(0.3,ydata_nziz,zdata_nziz,'spline');
[pt23_nziz,~,~] = interparc(0.5,ydata_nziz,zdata_nziz,'spline');
[pt24_nziz,~,~] = interparc(0.7,ydata_nziz,zdata_nziz,'spline');
[pt25_nziz,~,~] = interparc(0.9,ydata_nziz,zdata_nziz,'spline');
[pt26_nziz,~,~] = interparc(1,ydata_nziz,zdata_nziz,'spline');

%% Collate Data Points
%%% Circuference
circum = [pt_circum.' pt1_circum.' pt2_circum.' pt3_circum.' pt4_circum.' pt5_circum.' pt6_circum.' pt7_circum.' pt8_circum.' pt9_circum.' pt10_circum.' pt11_circum.'];
%%% Ear to Ear
e2e = [pt14_e2e.' pt15_e2e.' pt16_e2e.' pt17_e2e.' pt18_e2e.'];
%%% NZIZ
nziz = [pt21_nziz.' pt22_nziz.' pt23_nziz.' pt24_nziz.' pt25_nziz.'];

%% Find Shortest Euclidean Distance.
%%% The nearest point on the wanded data is found based on the predicted
%%% points. This is done such that we care able to determine the left out
%%% axis value for each data set. For this the Eudlidean distance between
%%% each predicted point and the wanded points are taken in the 2D plane. 

%%% Circumference

A1= [circumference_x circumference_y];
closest_array_circum = find_closest_from_predicted_to_wanded(circum, A1);

%%% Ear to Ear
A2 = [e2e_x e2e_z];
closest_array_e2e = find_closest_from_predicted_to_wanded(e2e, A2);

%%%NZ-IZ
A3 = [nziz_y nziz_z];
closest_array_nziz = find_closest_from_predicted_to_wanded(nziz, A3);

%% Find left out axis values 
%%% Circumference - The circumference is orthogonally projected in the XZ
%%% plane and the Y values need to be found. 
%%% If A(:,1)==closest(:,1) and A(:3)==closest(:,2). Then we need to extract
%%% that particular entire row and specifically its Y value (2nd column).
interpolate_closest_circum = find_left_out_axis_values(closest_array_circum, A1, circumference_dataset,1 , 1, 3);
trans_intrapolate_closest_circum = interpolate_closest_circum.';

%%% Ear to Ear - The ear to ear is orthogonally projected in the XY
%%% plane and the Z values need to be found. 
%%% If A(:,1)==closest(:,1) and A(:2)==closest(:,2). Then we need to extract
%%% that particular entire row and specifically its Z value (3rd column)
interpolate_closest_e2e = find_left_out_axis_values(closest_array_e2e, A2, e2e_dataset, 2, 3, 2);
trans_intrapolate_closest_e2e = interpolate_closest_e2e.';

%%% NZIZ - The  NZIZ is orthogonally projected in the
%%% ZY plane and the X values need to be found. 
%%% If A(:,3)==closest(:,1) and A(:2)==closest(:,2). Then we need to extract
%%% that particular entire row and specifically its X value (1st column).
interpolate_closest_nziz = find_left_out_axis_values(closest_array_nziz, A3, nziz_dataset, 1, 2, 1);
trans_intrapolate_closest_nziz = interpolate_closest_nziz.';

%% Reorganize the data
%%% Circumference
final_circumference = [circum(1:1,:); circum(2:2,:);trans_intrapolate_closest_circum]; 
% scatter3(final_circumference(1:1,:),final_circumference(2:2,:),final_circumference(3:3,:)); 
convert_final_circumference = num2cell(final_circumference);
circumference_label = {'Fpz' 'Fp2' 'F8' 'T4' 'T6' 'O2' 'Oz' 'O1' 'T5' 'T3' 'F7' 'Fp1'};
final_circumference_label = [circumference_label;  convert_final_circumference];
%%% Ear to Ear
final_e2e = [e2e(1:1,:);trans_intrapolate_closest_e2e;e2e(2:2,:)];
% scatter3(final_e2e(1:1,:),final_e2e(2:2,:),final_e2e(3:3,:)); 
convert_final_e2e = num2cell(final_e2e);
e2e_label = {'T4' 'C4' 'Cz' 'C3' 'T3'};
final_e2e_label = [e2e_label;  convert_final_e2e];
%%% NZIZ 
final_nziz = [trans_intrapolate_closest_nziz; nziz(1:1,:); nziz(2:2,:)];
% scatter3(final_nziz(1:1,:),final_nziz(2:2,:),final_nziz(3:3,:)); 
convert_final_nziz = num2cell(final_nziz);
nziz_label = {'Fpz' 'Fz' 'Cz' 'Pz' 'Oz'};
final_nziz_label = [nziz_label;  convert_final_nziz];

% figure;
% scatter3(final_circumference(1:1,:),final_circumference(2:2,:),final_circumference(3:3,:)); 
% hold on
% scatter3(final_e2e(1:1,:),final_e2e(2:2,:),final_e2e(3:3,:)); 
% hold on
% scatter3(final_nziz(1:1,:),final_nziz(2:2,:),final_nziz(3:3,:)); 

%% Append all together. 
%%% Create a new variable and append final_circumference, final_e2e and
%%% final_nziz together.
final_points_combined_label = [final_circumference_label final_e2e_label final_nziz_label];
final_points_converted_x = cell2mat(final_points_combined_label(2:2,:));
final_points_converted_y = cell2mat(final_points_combined_label(3:3,:));
final_points_converted_z = cell2mat(final_points_combined_label(4:4,:)) ;
final_points_mat = [final_points_converted_x; final_points_converted_y; final_points_converted_z];

%%%Extract Common Points
%%%Fpz
common_Fpz = final_points_mat(:,1);
midpoint_Fpz = common_Fpz;
%%% Oz
common_Oz = final_points_mat(:,7);
midpoint_Oz = common_Oz;
%%% Cz
common_Cz = final_points_mat(:,15);
midpoint_Cz = common_Cz;
%%% T3
common_T3 = [final_points_mat(:,10) final_points_mat(:,17)];
midpoint_T3 = mean(common_T3,2);
%%% T4
common_T4 = [final_points_mat(:,4) final_points_mat(:,13)];
midpoint_T4 = mean(common_T4,2);

%%% 17 electrode positions
final_points = [midpoint_Fpz final_points_mat(:,2) final_points_mat(:,3) midpoint_T4 final_points_mat(:,5) final_points_mat(:,6) midpoint_Oz final_points_mat(:,8) final_points_mat(:,9) midpoint_T3 final_points_mat(:,11) final_points_mat(:,12) final_points_mat(:,14) midpoint_Cz final_points_mat(:,16) final_points_mat(:,18) final_points_mat(:,22)];
%% fvrv
ff=figure;
ff.Position = [10 10 550 400]; 
xlabel('X')
ylabel('Y')
zlabel('Z')
scatter3(final_points(1:1,:),final_points(2:2,:),final_points(3:3,:),'r*');
% hold on
% scatter3(final_points_converted_x, final_points_converted_y, final_points_converted_z);
% legend('Final points','Initial 22 electrodes');
% hold on
% scatter3(D1_x,D1_y,D1_z,'p');
