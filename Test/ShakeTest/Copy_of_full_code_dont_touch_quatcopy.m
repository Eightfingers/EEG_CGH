%%% This code would be the final code that is used to determine the 17 EEG
%%% locations. 
%% Add to path different folders containing data and code
% addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept');
% addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\helperfuncs');
% addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\myfuncs');
% addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Data\30_9_2021');

addpath('helperfuncs\')
addpath('myfuncs\')
addpath('quaternion')

%%% NZIZ
nziz = readmatrix ('NZIZ_shake_16_11_2021_2.csv');
nziz_wand = nziz(:,3:9); 
nziz_wand = rmmissing(nziz_wand);
plot3(nziz_wand(:,5),nziz_wand(:,7),nziz_wand(:,6), 'd');
hold on

nziz_specs = nziz(:,34:40); 
nziz_specs = rmmissing(nziz_specs);

quaternion_extracted = nziz(:,35:38); % extract the rotation vector out
quaternion_extracted = rmmissing(quaternion_extracted);
quaternion_extracted = [quaternion_extracted(:,4), quaternion_extracted(:,1), quaternion_extracted(:,2), quaternion_extracted(:,3)];
dis_matrix_nziz = nziz(:,39:41); % extract the displacement vector out
dis_matrix_nziz = [dis_matrix_nziz(:,1), dis_matrix_nziz(:,3), dis_matrix_nziz(:,2)];
dis_matrix_nziz = rmmissing(dis_matrix_nziz);

new_markers_nziz = [];
rotation_matrix = [];
for i = 1:1:length(nziz_wand)
%     disp(i);
    quat_vector = quaternion(quaternion_extracted(i,:));
    RPY1 = eulerd(quat_vector,'XYZ', 'frame' );
    rot_vector_nziz = [-RPY1(1), -RPY1(2), -RPY1(3)];
    rotation_matrix = [rotation_matrix; rot_vector_nziz ];
    
    dis_vector_circum = dis_matrix_nziz(i,:);
    wand_vector_circum = [nziz_wand(i,5); ... % X,Y,Z 
              nziz_wand(i,7); ...
              nziz_wand(i,6); ...
               1];
    transform_matrix_circum = construct_matrix_transform_xyz(dis_vector_circum, rot_vector_nziz);    
    new_vector_nziz = inv(transform_matrix_circum) * wand_vector_circum;
    new_markers_nziz = [new_markers_nziz; new_vector_nziz.';];
end

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
% hold on 
% plot(ydata_nziz(end-100),zdata_nziz(end-100),'ms','MarkerSize',20);

% % hold on
% scatter(nziz_y,nziz_z,'gd');
% hold on;
% plot(nziz_y(1:1),nziz_z(1:1),'rs','MarkerSize',20);
% plot(nziz_y(end),nziz_z(end),'bs','MarkerSize',20);

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

%% Find left out axis values

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
convert_final_nziz = num2cell(final_nziz);
nziz_label = {'Fpz' 'Fz' 'Cz' 'Pz' 'Oz'};
final_nziz_label = [nziz_label;  convert_final_nziz];

figure;
hold on
plot3(final_nziz(1:1,:),final_nziz(2:2,:),final_nziz(3:3,:),'d', 'MarkerSize', 20); 
return;

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
common_Fpz = [final_points_mat(:,1) final_points_mat(:,18)];
% plot3(-5.8823, 33.3660, 30.8926, 'bd','MarkerSize', 20);
% plot3(-3.6253, 28.1272, 46.1749, 'd','MarkerSize', 20);
midpoint_Fpz = mean(common_Fpz,2);
%%% Oz
common_Oz = [final_points_mat(:,7) final_points_mat(:,22)];
midpoint_Oz = mean(common_Oz,2);
%%% Cz
common_Cz = [final_points_mat(:,15) final_points_mat(:,20)];
midpoint_Cz = mean(common_Cz,2);
%%% T3
common_T3 = [final_points_mat(:,10) final_points_mat(:,17)];
midpoint_T3 = mean(common_T3,2);
%%% T4
common_T4 = [final_points_mat(:,4) final_points_mat(:,13)];
midpoint_T4 = mean(common_T4,2);

%%% 17 electrode positions
final_points = [midpoint_Fpz final_points_mat(:,2) final_points_mat(:,3) midpoint_T4 final_points_mat(:,5) final_points_mat(:,6) midpoint_Oz final_points_mat(:,8) final_points_mat(:,9) midpoint_T3 final_points_mat(:,11) final_points_mat(:,12) final_points_mat(:,14) midpoint_Cz final_points_mat(:,16) final_points_mat(:,19) final_points_mat(:,21)];
%% fvrv
ff=figure;
ff.Position = [10 10 550 400]; 
xlabel('X')
ylabel('Y')
zlabel('Z')
scatter3(final_points(1:1,:),final_points(2:2,:),final_points(3:3,:),'r*');
hold on
scatter3(new_markers_static(:,1), new_markers_static(:,2),new_markers_static(:,3));
% hold on
% scatter3(final_points_converted_x, final_points_converted_y, final_points_converted_z);
legend('Final points','Initial 22 electrodes');

% hold on
% scatter3(D1_x,D1_y,D1_z,'p');
%% Final 4 Points 

% MATLAB XYZ convention
final_points = final_points.';
figure;
plot3(final_points(:,1), final_points(:,2), final_points(:,3), 'd');
title('Final points');
% xlabel('X');
% ylabel('Y');
% zlabel('Z');
for i = 1:1:length(final_points)
    text(final_points(i,1), final_points(i,2), final_points(i,3),string(i));
end
figure;
hold on
scatter3(static_dataset(:,1), static_dataset(:,2),static_dataset(:,3));
for i = 1:1:length(static_dataset)
    text(static_dataset(i,1), static_dataset(i,2), static_dataset(i,3),string(i));
end

%%% Labelling of points - Predicted
Fpz = final_points(1,:);
Fp2 = final_points(12,:);
F8 = final_points(11,:);
T4 = final_points(10,:);
T6 = final_points(9,:);
O2 = final_points(8,:);
Oz = final_points(7,:);
O1 = final_points(6,:);
T5 = final_points(5,:);
T3 = final_points(4,:);
F7 = final_points(3,:);
Fp1 = final_points(2,:);
Fz = final_points(16,:);
Cz = final_points(14,:);
Pz = final_points(17,:);
C4 = final_points(15,:);
C3 = final_points(13,:);
% [ x, y, z ; x, y, z;]
%%% P3 spline approximation
%%% Find X
%%% Extract out the X and Y values of spline points
spline_pts = [T5; Pz; T6];
x_vector = spline_pts(:,1);
z_vector = spline_pts(:,3);
[xxdata, zzdata] = splineplot(x_vector, z_vector);
[P3_XZ,~,~] = interparc(0.25, xxdata, zzdata,'spline');
% Visual XZ spline plot
% figure;
% plot(P3_XZ(1), P3_XZ(2) ,'d');
% hold on;
% plot(x_vector, z_vector, 'o');
% plot(xxdata, zzdata);

%%% Find Y & Z
%%% Extract out the Y and Z values of spline points
spline_pts2 = [O1; C3; Fp1];
y_spline = spline_pts2(:,2);
z_spline = spline_pts2(:,3);
[xx_fit2, yy_fit2] = splineplot(y_spline, z_spline);
[P3_YZ,~,~] = interparc(0.25, xx_fit2, yy_fit2,'spline');
P3 = [P3_XZ(1) , P3_YZ(1), P3_YZ(2)];
plot3(P3(1), P3(2), P3(3), 'ko');

% % Visual YZ spline plot
% figure;
% plot(P3_YZ(1), P3_YZ(2),'d');
% hold on;
% plot(y_spline, z_spline, 'o');
% plot(xx_fit2, yy_fit2);

%%% P4 spline approximation
%%% Find X
spline_pts = [T5; Pz; T6];
x_vector = spline_pts(:,1);
z_vector = spline_pts(:,3);
[xxdata, zzdata] = splineplot(x_vector, z_vector);
[P4_XZ,~,~] = interparc(0.75, xxdata, zzdata,'spline');
% % Visual XZ spline plot
% figure;
% plot(P4_XZ(1), P4_XZ(2) ,'d');
% hold on;
% plot(x_vector, z_vector, 'o');
% plot(xxdata, zzdata);

% Find Y & Z
spline_pts3 = [O2; C4; Fp2];
y_spline = spline_pts3(:,2);
z_spline = spline_pts3(:,3);
[yy_fit3, zz_fit3] = splineplot(y_spline, z_spline);
[P4_YZ,~,~] = interparc(0.25, yy_fit3, zz_fit3,'spline');
P4 = [P4_XZ(1) , P4_YZ(1), P4_YZ(2)];
% plot3(P4(1), P4(2), P4(3), 'ko');

% % Visual YZ spline plot
% figure;
% plot(P4_YZ(1), P4_YZ(2),'d');
% hold on;
% plot(y_spline, z_spline, 'o');
% plot(yy_fit3, zz_fit3);

%%% F4 spline approximation
%%% Find X
spline_pts4 = [F7; Fz; F8];
x_spline = spline_pts4(:,1);
z_spline = spline_pts4(:,3);
[xxdata4, zzdata4] = splineplot(x_spline, z_spline);
[F4_XZ,~,~] = interparc(0.75, xxdata4,zzdata4,'spline'); % F4 is located from the right 

% % Visual XZ spline plot
% figure;
% plot(F4_XZ(1), F4_XZ(2) ,'d'); % the predicted points
% hold on;
% plot(x_spline, z_spline, 'o'); % the points
% plot(xxdata4, zzdata4); % spline

% Find Z Y Coordinate this spline3 is similar to the one used to find ZY of
% P4 however we find at the 75% position
y_spline = spline_pts3(:,2);
z_spline = spline_pts3(:,3);
[yy_fit3, zz_fit3] = splineplot(y_spline, z_spline);
[F4_YZ,~,~] = interparc(0.75, yy_fit3, zz_fit3,'spline');
F4 = [F4_XZ(1) , F4_YZ(1), F4_YZ(2)];
% plot3(F4(1), F4(2), F4(3), 'ko');

% % Visual YZ spline plot
% figure;
% plot(P4_YZ(1), P4_YZ(2),'d');
% hold on;
% plot(y_spline, z_spline, 'o');
% plot(yy_fit3, zz_fit3);


%%% F3 spline approximation
%%% Find X same spline approx as F4 to find x position
spline_pts4 = [F7; Fz; F8];
x_spline = spline_pts4(:,1);
z_spline = spline_pts4(:,3);
[xxdata4, zzdata4] = splineplot(x_spline, z_spline);
[F3_XZ,~,~] = interparc(0.25, xxdata4,zzdata4,'spline'); % F3 is located from the right 

% % Visual XZ spline plot
% figure;
% plot(F4_XZ(1), F4_XZ(2) ,'d'); % the predicted points
% hold on;
% plot(x_spline, z_spline, 'o'); % the points
% plot(xxdata4, zzdata4); % spline

% Find Z and Y
spline_pts2 = [O1; C3; Fp1];
y_spline = spline_pts2(:,2);
z_spline = spline_pts2(:,3);
[yy_fit2, zz_fit2] = splineplot(y_spline, z_spline);
[F3_YZ,~,~] = interparc(0.75, yy_fit2, zz_fit2,'spline');
F3 = [F3_XZ(1) , F3_YZ(1), F3_YZ(2)];
plot3(F3(1), F3(2), F3(3), 'ko');
hold on;

predicted = [Fpz; Fp2; F8; T4; T6; O2; Oz; O1; T5; T3; F7; Fp1; Fz; Cz; Pz; C4; C3; F4; F3; P3; P4 ];
four_points = [F4; F3; P3; P4];

% plot3(four_points(:,1), four_points(:,2), four_points(:,3), 'kd');
% hold on;
% plot(F3_YZ(1), F3_YZ(2), 'o');
figure;
hold on;
plot3(predicted(:,1), predicted(:,2), predicted(:,3), 'd');
hold on
scatter3(static_dataset(:,1), static_dataset(:,2),static_dataset(:,3));
for i = 1:1:length(static_dataset)
    text(static_dataset(i,1), static_dataset(i,2), static_dataset(i,3),string(i));
end
hold on;

xlabel('x');
ylabel('y');
zlabel('z')

%% Euclidean Distance Error

%%% Labelling of points - Static
Fpz_static = static_dataset(13,:);
Fp2_static = static_dataset(11,:);
F8_static = static_dataset(6,:);
T4_static = static_dataset(5,:);
T6_static = static_dataset(7,:);
O2_static = static_dataset(12,:);
Oz_static = static_dataset(16,:);
O1_static = static_dataset(19,:);
T5_static = static_dataset(24,:);
T3_static = static_dataset(25,:);
F7_static = static_dataset(23,:);
Fp1_static = static_dataset(18,:);
Fz_static = static_dataset(14,:);
Cz_static = static_dataset(15,:);
Pz_static = static_dataset(17,:);
C4_static = static_dataset(9,:);
C3_static = static_dataset(21,:);
F4_static = static_dataset(8,:);
F3_static = static_dataset(20,:);
P3_static = static_dataset(22,:);
P4_static = static_dataset(10,:);

%% Euclidean Error

Fpz_diff = norm(Fpz -Fpz_static);
Fp2_diff = norm(Fp2 -Fp2_static);
F8_diff = norm(F8 - F8_static); 
T4_diff = norm(T4 -T4_static);
T6_diff = norm(T6 -T6_static);
O2_diff = norm(O2 -O2_static);
Oz_diff =norm(Oz -Oz_static);
O1_diff = norm(O1 -O1_static);
T5_diff = norm(T5 -T5_static);
T3_diff = norm(T3 -T3_static);
F7_diff = norm(F7 -F7_static);
Fp1_diff = norm(Fp1 -Fp1_static);
Fz_diff = norm(Fz -Fz_static);
Cz_diff = norm(Cz -Cz_static);
Pz_diff = norm(Pz -Pz_static);
C4_diff = norm(C4 -C4_static);
C3_diff = norm(C3 -C3_static);
F4_diff = norm(F4 - F4_static);
F3_diff = norm(F3 - F3_static);
P3_diff = norm(P3 - P3_static);
P4_diff = norm(P4 - P4_static);
all_diff = [Fpz_diff; Fp2_diff; F8_diff; T4_diff; T6_diff; O2_diff; Oz_diff; O1_diff; ...
    T5_diff; T3_diff; F7_diff; Fp1_diff; Fz_diff; Cz_diff; Pz_diff; C4_diff; C3_diff;
    F4_diff; F3_diff; P3_diff; P4_diff]