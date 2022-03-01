% addpath('C:\Users\65914\Documents\GitHub\EEG_CGH\EEG_CGH\Python\Main\matlab_funcs\helperfuncs\');
% addpath('C:\Users\65914\Documents\GitHub\EEG_CGH\EEG_CGH\Python\Main\matlab_funcs\myfuncs
addpath('C:\Users\65859\Desktop\eeg_cgh_main\Python\Main\matlab_funcs\myfuncs');
addpath('C:\Users\65859\Desktop\eeg_cgh_main\Python\Main\matlab_funcs\helperfuncs\');
addpath('DataTests\21_10_2021');

%% Load the different wanded data
%% Load the different wanded data
%%% Circumference
%%% Ear to Ear
ear2ear = readmatrix('error_ear2ear.csv');
e2e_wand = ear2ear(:,3:9); 
e2e_wand = rmmissing(e2e_wand);
e2e_wand = e2e_wand(1:5:end, :);
e2e_wand = [e2e_wand(:,5), e2e_wand(:,7),e2e_wand(:,6)];
% hold on
% scatter3(e2e_wand(:,5), e2e_wand(:,6),e2e_wand(:,7));

%%% Ear to Ear
e2e_dataset= e2e_wand;
e2e_dataset = rmmissing(e2e_dataset);
e2e_x = e2e_dataset(:,1);
e2e_y = e2e_dataset(:,2);
e2e_z = e2e_dataset(:,3);
hold on
scatter3(e2e_x,e2e_y,e2e_z);

xlabel('x')';
ylabel('y')';
zlabel('z')';

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

% find start point
dist_startpoint_e2e = sqrt(sum(bsxfun(@minus, trans_newmat_xz, startpoint_2d_e2e).^2,2));
closest_startpoint_e2e = trans_newmat_xz(find(dist_startpoint_e2e==min(dist_startpoint_e2e)),:);

% find end point
dist_endpoint_e2e = sqrt(sum(bsxfun(@minus, trans_newmat_xz, endpoint_2d_e2e).^2,2));
closest_endpoint_e2e = trans_newmat_xz(find(dist_endpoint_e2e==min(dist_endpoint_e2e)),:);

[row_startpoint_e2e,~] = find(trans_newmat_xz==closest_startpoint_e2e);
[row_endpoint_e2e,~] = find(trans_newmat_xz==closest_endpoint_e2e);

if row_startpoint_e2e > 50
    new_matrix_x_e2e = [trans_newmat_xz(row_endpoint_e2e:row_startpoint_e2e,1)].';
    new_matrix_z_e2e = [trans_newmat_xz(row_endpoint_e2e:row_startpoint_e2e,2)].';
else
    % Swapped for some reason
    new_matrix_x_e2e = [trans_newmat_xz(row_startpoint_e2e:row_endpoint_e2e,1)].';
    new_matrix_z_e2e = [trans_newmat_xz(row_startpoint_e2e:row_endpoint_e2e,2)].';
end

%%% Ear to Ear
[pt13_e2e,~,~] = interparc(0,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt14_e2e,~,~] = interparc(0.1,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt15_e2e,~,~] = interparc(0.3,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt16_e2e,~,~] = interparc(0.5,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt17_e2e,~,~] = interparc(0.7,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt18_e2e,~,~] = interparc(0.9,new_matrix_x_e2e,new_matrix_z_e2e,'spline');
[pt19_e2e,~,~] = interparc(1,new_matrix_x_e2e,new_matrix_z_e2e,'spline');

ear2ear = [pt14_e2e.' pt15_e2e.' pt16_e2e.' pt17_e2e.' pt18_e2e.'];

%%% Ear to Ear
A2 = [e2e_x e2e_z];
[closest_array_e2e] = find_closest_from_predicted_to_wanded(ear2ear, A2);

%%% Ear to Ear - The ear to ear is orthogonally projected in the XY
%%% plane and the Z values need to be found. 
%%% If A(:,1)==closest(:,1) and A(:2)==closest(:,2). Then we need to extract
%%% that particular entire row and specifically its Z value (3rd column)
% unique_e2e_dataset = unique(e2e_dataset, 'rows');
% closest_array_e2e = unique(closest_array_e2e , 'rows');
interpolate_closest_e2e = find_left_out_axis_values(closest_array_e2e, e2e_dataset, 2, 1, 1);
trans_intrapolate_closest_e2e = interpolate_closest_e2e.';
final_e2e = [ear2ear(1:1,:);trans_intrapolate_closest_e2e;ear2ear(2:2,:)];
% scatter3(final_e2e(1:1,:),final_e2e(2:2,:),final_e2e(3:3,:)); 
convert_final_e2e = num2cell(final_e2e);
e2e_label = {'T4' 'C4' 'Cz' 'C3' 'T3'};
final_e2e_label = [e2e_label;  convert_final_e2e];

transposed_final_e2e = final_e2e.';

plot3(transposed_final_e2e(:,1), transposed_final_e2e(:,2), transposed_final_e2e(:,3), '*');

