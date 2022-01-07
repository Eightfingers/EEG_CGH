function final_nziz_python = no_transform_get_nziz()

addpath('helperfuncs');
addpath('myfuncs');

%%% NZIZ
stylus_data = readmatrix('data_NZIZstylus_specs_frame')
step = 5; % used to take only every 2nd data
stylus_data = stylus_data(1:step:end,:); 
stylus_data = [stylus_data(:,1) stylus_data(:,3) stylus_data(:,2)]; 
% stylus_data = rmmissing(stylus_data);

%%% NZ-IZ
nziz_dataset =  stylus_data;
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

plot3(zeros(length(ydata_nziz), 1), ydata_nziz.', zdata_nziz.');

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
[pt25_nziz,~,~] = interparc(0.90,ydata_nziz,zdata_nziz,'spline');
[pt26_nziz,~,~] = interparc(1,ydata_nziz,zdata_nziz,'spline');

%% Collate Data Points
%%% NZIZ
nziz = [pt25_nziz.' pt24_nziz.' pt23_nziz.' pt22_nziz.' pt21_nziz.'];
% nziz = [pt26_nziz.' pt25_nziz.' pt24_nziz.' pt23_nziz.' pt22_nziz.' pt21_nziz.'];
% nziz = [pt21_nziz.' pt20_nziz.'];

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
nziz_dataset = unique(nziz_dataset, 'rows');
interpolate_closest_nziz = find_left_out_axis_values(closest_array_nziz, nziz_dataset, 1, 2, 1);

trans_intrapolate_closest_nziz = interpolate_closest_nziz.';

%% Reorganize the data

%%% NZIZ 
final_nziz_python = [trans_intrapolate_closest_nziz; nziz(1:1,:); nziz(2:2,:)];
final_nziz_python = final_nziz_python.';

% Y upwards convention for the GUI
final_nziz_python = [final_nziz_python(:,1), final_nziz_python(:,3), final_nziz_python(:,2)]; 
Fpz = final_nziz_python(1,:);
% final_nziz_python = final_nziz_python *1000; % convert m to mm
plot3(final_nziz_python(:,1), final_nziz_python(:,3), final_nziz_python(:,2), 'd', 'MarkerSize', 20);
hold on ;
% xlabel('x');
% ylabel("y");
% zlabel("z")

% 
% predicted_nziz = num2cell(final_nziz_python);
% nziz_label = {'Fpz' 'Fz' 'Cz' 'Pz' 'Oz'};
% final_nziz_label = [nziz_label;  predicted_nziz];

end

