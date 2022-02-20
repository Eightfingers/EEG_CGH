addpath('C:\Users\65914\Documents\GitHub\EEG_CGH\EEG_CGH\Python\Main\matlab_funcs\helperfuncs\');
addpath('C:\Users\65914\Documents\GitHub\EEG_CGH\EEG_CGH\Python\Main\matlab_funcs\myfuncs');

% addpath('C:\Users\65859\Desktop\eeg_cgh_main\Python\Main\matlab_funcs\helperfuncs\');
% addpath('C:\Users\65859\Desktop\eeg_cgh_main\Python\Main\matlab_funcs\myfuncs\');

addpath('9_2_2022\');

%% Load the different wanded data
circumference = readmatrix('brenda_circum_004.csv');
ear2ear = readmatrix('brenda_ear2ear_007.csv');
nziz = readmatrix ('brenda_nziz_002.csv');

%% Doing NZIZ
new_markers_nziz = nziz(:,7:9); 
new_markers_nziz = rmmissing(new_markers_nziz);
new_markers_nziz = new_markers_nziz(1:2:end,:); 
new_markers_nziz = [new_markers_nziz(:,1), new_markers_nziz(:,3), new_markers_nziz(:,2)];
hold on;
plot3(new_markers_nziz(:,1), new_markers_nziz(:,2), new_markers_nziz(:,3), '*');

%% Doing Ear to Ear 
new_markers_e2e = ear2ear(:,7:9);
new_markers_e2e = rmmissing(new_markers_e2e);
new_markers_e2e = new_markers_e2e(1:2:end, :); 
new_markers_e2e = [new_markers_e2e(:,1), new_markers_e2e(:,3), new_markers_e2e(:,2)];
hold on;
plot3(new_markers_e2e(:,1), new_markers_e2e(:,2), new_markers_e2e(:,3), '*');

%% Doing circumference 
new_markers_circum = circumference(:,7:9); 
new_markers_circum = rmmissing(new_markers_circum);
new_markers_circum = new_markers_circum(1:2:end,:); 
new_markers_circum = [new_markers_circum(:,1), new_markers_circum(:,3), new_markers_circum(:,2)];
hold on;
plot3(new_markers_circum(:,1), new_markers_circum(:,2), new_markers_circum(:,3), 'd');

xlabel('X');
ylabel('Y');
zlabel('Z');

%%% NZ-IZ;
nziz_dataset = new_markers_nziz;
noiseIntensity = 0.005; %
noise_x = rand(size(nziz_dataset(:,1))) * noiseIntensity;
noise_y = rand(size(nziz_dataset(:,1))) * noiseIntensity;
noise_z = rand(size(nziz_dataset(:,1))) * noiseIntensity;
nziz_x = nziz_dataset(:,1) +noise_x;
nziz_y = nziz_dataset(:,2) +noise_y; 
nziz_z = nziz_dataset(:,3) +noise_z;

%%% Ear to Ear
e2e_dataset = new_markers_e2e;
noiseIntensity = 0.005; %
noise_x = rand(size(e2e_dataset(:,1))) * noiseIntensity;
noise_y = rand(size(e2e_dataset(:,1))) * noiseIntensity;
noise_z = rand(size(e2e_dataset(:,1))) * noiseIntensity;
e2e_x = e2e_dataset(:,1)+ +noise_x;
e2e_y = e2e_dataset(:,2) + +noise_y;
e2e_z = e2e_dataset(:,3)+ +noise_z;

%%% Circumference
circumference_dataset = new_markers_circum;
noiseIntensity = 0.005; %
noise_x = rand(size(circumference_dataset(:,1))) * noiseIntensity;
noise_y = rand(size(circumference_dataset(:,1))) * noiseIntensity;
noise_z = rand(size(circumference_dataset(:,1))) * noiseIntensity;
circumference_x = circumference_dataset(:,1) + +noise_x;
circumference_y = circumference_dataset(:,2) +noise_y;
circumference_z = circumference_dataset(:,3)+ +noise_z;

%% Perform Geometerical Fitting and Extract the datatips from the plots.

%%% Circumference - The circumference is considered as and ellipse in 2D
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
ydata_nziz = [ydata_nziz_back ydata_nziz_front];
zdata_nziz = [zdata_nziz_back zdata_nziz_front];
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
[pt22_nziz,~,~] = interparc(0.30,ydata_nziz,zdata_nziz,'spline');
[pt23_nziz,~,~] = interparc(0.50,ydata_nziz,zdata_nziz,'spline');
[pt24_nziz,~,~] = interparc(0.70,ydata_nziz,zdata_nziz,'spline');
[pt25_nziz,~,~] = interparc(0.95,ydata_nziz,zdata_nziz,'spline');
[pt26_nziz,~,~] = interparc(1,ydata_nziz,zdata_nziz,'spline');

%% Collate Data Points
%%% Circuference
circum = [pt_circum.' pt1_circum.' pt2_circum.' pt3_circum.' pt4_circum.' pt5_circum.' pt6_circum.' pt7_circum.' pt8_circum.' pt9_circum.' pt10_circum.' pt11_circum.'];
%%% Ear to Ear
ear2ear = [pt14_e2e.' pt15_e2e.' pt16_e2e.' pt17_e2e.' pt18_e2e.'];
%%% NZIZ
nziz = [pt25_nziz.' pt24_nziz.' pt23_nziz.' pt22_nziz.' pt21_nziz.'];

%% Find Shortest Euclidean Distance.
%%% The nearest point on the wanded data is found based on the predicted
%%% points. This is done such that we care able to determine the left out
%%% axis value for each data set. For this the Eudlidean distance between
%%% each predicted point and the wanded points are taken in the 2D plane. 

%%% Circumference
A1= [circumference_x circumference_y];
% closest_array_circum = find_closest_from_predicted_to_wanded(circum, A1);
closest_array_circum = circum.';

%%% Ear to Ear
A2 = [e2e_x e2e_z];
% closest_array_e2e = find_closest_from_predicted_to_wanded(ear2ear, A2);
closest_array_e2e = ear2ear.';

%%%NZ-IZ
A3 = [nziz_y nziz_z];
% closest_array_nziz = find_closest_from_predicted_to_wanded(nziz, A3);
closest_array_nziz = nziz.';

%% Find left out axis values 
% Circumference - The circumference is orthogonally projected in the XZ
% plane and the Y values need to be found. 
% If A(:,1)==closest(:,1) and A(:3)==closest(:,2). Then we need to extract
% that particular entire row and specifically its Y value (2nd column).

% % % To confusing to make it to a function so I left it like this. Shouldn't
% % % be too much of a problem.

interpolate_closest_circum= [];

for i = 1:1:length(closest_array_circum) 
    distances_circum_1 = sqrt(sum(bsxfun(@minus, A1,closest_array_circum(i,:) ).^2,2));
    n = 4; 
    [~, ascendIdx] = sort(distances_circum_1); 
%     ascendIdx(ascendIdx==closest_array_circum(i,:)) = [];  %remove the pt point
    
    ANearest_circum = new_markers_circum(ascendIdx(1:n),:);  % 4 nearest points in 3D 
        
    %% Interpolation
    xq = closest_array_circum(i,1); % z value 
    zq = interp1(ANearest_circum(:,1), ANearest_circum(:,3), xq, 'linear', 'extrap');
    
    interpolate_closest_circum = [interpolate_closest_circum; zq]; % append to the interpolate losest
end
trans_intrapolate_closest_circum = interpolate_closest_circum.';

return;

%%% Ear to Ear - The ear to ear is orthogonally projected in the XY
%%% plane and the Z values need to be found. 
%%% If A(:,1)==closest(:,1) and A(:2)==closest(:,2). Then we need to extract
%%% that particular entire row and specifically its Z value (3rd column)
interpolate_closest_e2e= [];
for j = 1:1:length(closest_array_e2e) 
    distances_e2e_1 = sqrt(sum(bsxfun(@minus, A2,closest_array_e2e(j,:) ).^2,2));
    n = 4; 
    [~, ascendIdx] = sort(distances_e2e_1); 
    ascendIdx(ascendIdx==closest_array_e2e(j,:)) = [];  %remove the pt point
    ANearest_e2e = new_markers_e2e(ascendIdx(1:n),:);  % 4 nearest points in 3D 

    xq1 = closest_array_e2e(j,2); % x value 
    yq = interp1(ANearest_e2e(:,3), ANearest_e2e(:,2), xq1, 'linear', 'extrap');
    
    interpolate_closest_e2e = [interpolate_closest_e2e; yq]; % append to the interpolate losest
end
trans_intrapolate_closest_e2e = interpolate_closest_e2e.';

%%% NZIZ - The  NZIZ is orthogonally projected in the
%%% ZY plane and the X values need to be found. 
%%% If A(:,3)==closest(:,1) and A(:2)==closest(:,2). Then we need to extract
%%% that particular entire row and specifically its X value (1st column).
interpolate_closest_nziz= [];
for k = 1:1:length(closest_array_nziz) 
    distances_nziz_1 = sqrt(sum(bsxfun(@minus, A3,closest_array_nziz(k,:) ).^2,2));
    n = 4; 
    [~, ascendIdx] = sort(distances_nziz_1); 
    ascendIdx(ascendIdx==closest_array_nziz(k,:)) = [];  %remove the pt point
    ANearest_nziz = new_markers_nziz(ascendIdx(1:n),:);  % 4 nearest points in 3D 

    xq2 = closest_array_nziz(k,1); % x value 
    xxq = interp1(ANearest_nziz(:,2), ANearest_nziz(:,1), xq2, 'linear', 'extrap');
    
    interpolate_closest_nziz = [interpolate_closest_nziz; xxq]; % append to the interpolate losest
end
trans_intrapolate_closest_nziz = interpolate_closest_nziz.';

%% Reorganize the data
%%% Circumference
final_circumference = [circum(1:1,:); circum(2:2,:);trans_intrapolate_closest_circum]; 
% scatter3(final_circumference(1:1,:),final_circumference(2:2,:),final_circumference(3:3,:)); 
convert_final_circumference = num2cell(final_circumference);
circumference_label = {'Fpz' 'Fp2' 'F8' 'T4' 'T6' 'O2' 'Oz' 'O1' 'T5' 'T3' 'F7' 'Fp1'};
final_circumference_label = [circumference_label;  convert_final_circumference];

%%% Ear to Ear
final_e2e = [ear2ear(1:1,:);trans_intrapolate_closest_e2e;ear2ear(2:2,:)];
% scatter3(final_e2e(1:1,:),final_e2e(2:2,:),final_e2e(3:3,:)); 
convert_final_e2e = num2cell(final_e2e);
e2e_label = {'T4' 'C4' 'Cz' 'C3' 'T3'};
final_e2e_label = [e2e_label;  convert_final_e2e];

%%% NZIZ 
final_nziz = [trans_intrapolate_closest_nziz; nziz(1:1,:); nziz(2:2,:)];
convert_final_nziz = num2cell(final_nziz);
nziz_label = {'Fpz' 'Fz' 'Cz' 'Pz' 'Oz'};
final_nziz_label = [nziz_label;  convert_final_nziz];
 

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
% scatter3(final_points(:,1), final_points(:,2), final_points(:,3),'r*');

%% Final 4 Points 

% MATLAB XYZ convention
final_points = final_points.';
% for i = 1:1:length(final_points)
%     text(final_points(i,1), final_points(i,2), final_points(i,3),string(i));
% end
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
% plot(x_vector, z_vector, '*');
% hold on;
% plot(xxdata, zzdata, 'o', 'MarkerSize', 10);
% plot(P3_XZ(:,1), P3_XZ(:,2), 'd', 'MarkerSize', 10);

%%% Find Y & Z
%%% Extract out the Y and Z values of spline points
spline_pts2 = [O1; C3; Fp1];
y_vector = spline_pts2(:,2);
z_vector = spline_pts2(:,3);
[xx_fit2, yy_fit2] = splineplot(y_vector, z_vector);
[P3_YZ,~,~] = interparc(0.25, xx_fit2, yy_fit2,'spline');
P3 = [P3_XZ(1) , P3_YZ(1), P3_YZ(2)];
% plot3(P3(1), P3(2), P3(3), 'ko');

% % Visual YZ spline plot
% figure;
% plot(P3_YZ(1), P3_YZ(2),'d');
% hold on;
% plot(xx_fit2, yy_fit2, '*');

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
[F4_XZ,~,~] = interparc(0.80, xxdata4, zzdata4,'spline'); % F4 is located from the right 

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
[F4_YZ,~,~] = interparc(0.80, yy_fit3, zz_fit3,'spline');
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
[F3_XZ,~,~] = interparc(0.20, xxdata4,zzdata4,'spline'); % F3 is located from the right 

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
[F3_YZ,~,~] = interparc(0.80, yy_fit2, zz_fit2,'spline');
F3 = [F3_XZ(1) , F3_YZ(1), F3_YZ(2)];
% plot3(F3(1), F3(2), F3(3), 'ko');
% hold on;

predicted = [Fpz; Fp2; F8; T4; T6; O2; Oz; O1; T5; T3; F7; Fp1; Fz; Cz; Pz; C4; C3; F4; F3; P3; P4 ];
four_points = [F4; F3; P3; P4];

plot3(predicted(:,1), predicted(:,2), predicted(:,3), '*');
hold on;

for i = 1:1:length(predicted)
    text(predicted(i,1), predicted(i,2), predicted(i,3),string(i));
end

plot3(four_points(:,1), four_points(:,2), four_points(:,3), 'kd');

title('Predicted Electrode Locations');
xlabel('x');
ylabel('y');
zlabel('z');

static = readmatrix('brenda_static_001.csv');
first_row_static = static(9,:);

% The for loop starts at 3 as the first 2 columns of the csv files are
% not marker points. It steps up by 3 as each marker points has 3
% coordinates (x,y,z) so i is always 3,6,9 ...

static_markers = [];
for i = 3:3:length(first_row_static)
    disp(i)
    static_markers = [static_markers; first_row_static(i),first_row_static(i+2),first_row_static(i+1)];
end
hold on
plot3(static_markers(:,1), static_markers(:,2), static_markers(:,3), "*");

for i = 1:1:length(static_markers)
    text(static_markers(i,1), static_markers(i,2), static_markers(i,3),string(i));
end

Fpz_static = static_markers(6,:);
Fp2_static = static_markers(19,:);
F8_static = static_markers(8,:);
T4_static = static_markers(12,:);
T6_static = static_markers(9,:);
O2_static = static_markers(15,:);
Oz_static = static_markers(11,:);
O1_static = static_markers(10,:);
T5_static = static_markers(16,:);
T3_static = static_markers(2,:);
F7_static = static_markers(21,:);
Fp1_static = static_markers(1,:);
Cz_static = static_markers(18,:);
Pz_static = static_markers(4,:);
C4_static = static_markers(7,:);
C3_static = static_markers(14,:);
FZ_static = static_markers(20,:)
F4_static = static_markers(17,:);
F3_static = static_markers(6,:);
P3_static = static_markers(13,:);
P4_static = static_markers(3,:);

Fpz_error = norm(Fpz_static - Fpz)
Fp2_error = norm(Fp2_static - Fp2)
F8_error = norm(F8_static - F8)
T4_error = norm(T4_static- T4)
T6_error = norm(T6_static - T6)
O2_error = norm(O2_static - O2)
Oz_error =norm(Oz_static - Oz)
O1_error = norm(O1_static - O1)
T5_error = norm(T5_static - T5)
T3_error = norm(T3_static- T3)
F7_error = norm(F7_static- F7)
Fp1_error = norm(Fp1_static- Fp1)
Cz_error = norm(Cz_static- Cz)
Pz_error = norm(Pz_static - Pz)
C4_error = norm(C4_static - C4)
C3_error = norm(C3_static- C3)
FZ_error = norm(FZ_static- Fz)
F4_error = norm(F4_static- F4)
F3_error = norm(F3_static- F3)
P3_error = norm(P3_static- P3)
P4_error = norm(P4_static- P4)

error = [Fpz_error; Fp2_error; F8_error; T4_error; T6_error; O2_error; Oz_error; O1_error; T5_error; T3_error; F7_error; Fp1_error; Cz_error; ...
Pz_error; C4_error; C3_error; FZ_error; F4_error; F3_error; P3_error; P4_error];


