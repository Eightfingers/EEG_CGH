% function final_nziz_label = get_nziz( nziz ,nziz_spec)
%%% This code would be the final code that is used to determine the 17 EEG
%%% locations. 
%% Add to path different folders containing data and code
%  addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept');
% addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\helperfuncs');
% addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\myfuncs');
% addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Data\30_9_2021');
function final_nziz_python = get_nziz()
% addpath('6_10_2021');
addpath('helperfuncs');
addpath('myfuncs');
% addpath('C:\Users\65914\Documents\GitHub\EEG_CGH\EEG_CGH\Python\Main\RecordedData');
addpath('C:\Users\65859\Desktop\eeg_cgh_main\Python\Main\RecordedData');
% addpath('Main/RecordedData');

%%% NZIZ
stylus_data = readmatrix('data_NZIZstylus');
quaternion_extracted = readmatrix('rotation_data_NZIZspecs'); % extract the rotation vector out
quaternion_extracted = [quaternion_extracted(:,4), quaternion_extracted(:,1), quaternion_extracted(:,2), quaternion_extracted(:,3)];
dis_matrix_nziz = readmatrix('data_NZIZspecs.csv'); % extract the displacement vector out

% plot3(stylus_data(:,1), stylus_data(:,3), stylus_data(:,2), '*');
hold on ;

% Quaternion way
new_markers_nziz = [];
rotation_matrix = [];
% disp("Doing quaternion");
for i = 1:1:length(stylus_data)
    
%     disp(i);
    quat_vector = quaternion(quaternion_extracted(i,:));
    RPY1 = eulerd(quat_vector,'XYZ', 'frame' );
    rot_vector_nziz = [-RPY1(1), -RPY1(3), -RPY1(2)];
    rotation_matrix = [rotation_matrix; rot_vector_nziz ];
    
    dis_vector_circum = dis_matrix_nziz(i,:);
    wand_vector_circum = [stylus_data(i,1); ... % X,Y,Z 
              stylus_data(i,3); ...
              stylus_data(i,2); ...
               1];
    transform_matrix_circum = construct_matrix_transform_xyz(dis_vector_circum, rot_vector_nziz);    
    new_vector_nziz = inv(transform_matrix_circum) * wand_vector_circum;
    new_markers_nziz = [new_markers_nziz; new_vector_nziz.';];

end

% plot3(new_markers_nziz(:,1), new_markers_nziz(:,2), new_markers_nziz(:,3), 'o', 'MarkerSize',10);

%%% NZ-IZ
nziz_dataset =  new_markers_nziz;
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
interpolate_closest_nziz = find_left_out_axis_values(closest_array_nziz, A3, nziz_dataset, 1, 2, 1);
trans_intrapolate_closest_nziz = interpolate_closest_nziz.';

%% Reorganize the data

%%% NZIZ 
final_nziz_python = [trans_intrapolate_closest_nziz; nziz(1:1,:); nziz(2:2,:)];
final_nziz_python = final_nziz_python.';
final_nziz_python = [final_nziz_python(:,1), final_nziz_python(:,3), final_nziz_python(:,2)];


% final_nziz_python = final_nziz_python *1000; % convert m to mm
% plot3(final_nziz_python(1,:), final_nziz_python(2,:), final_nziz_python(3,:), 'd');
% hold on ;
% 
% predicted_nziz = num2cell(final_nziz_python);
% nziz_label = {'Fpz' 'Fz' 'Cz' 'Pz' 'Oz'};
% final_nziz_label = [nziz_label;  predicted_nziz];

end

