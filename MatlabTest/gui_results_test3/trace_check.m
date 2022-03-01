addpath('C:\Users\65914\Documents\GitHub\EEG_CGH\EEG_CGH\Python\Main\matlab_funcs\helperfuncs\');
addpath('C:\Users\65914\Documents\GitHub\EEG_CGH\EEG_CGH\Python\Main\matlab_funcs\myfuncs');
addpath('10_1_2022\Data Taken In optitrack\in metres')

%%% Optirack
%% Load the different wanded data
circumference = readmatrix('CIRCUM_10_1_2023.csv');
ear2ear = readmatrix('Ear2Ear_10_1_2024.csv');       
nziz = readmatrix ('NZIZ_10_1_2022.csv');

%% Doing NZIZ
stylus_data = nziz(:,3:9); 
stylus_data = rmmissing(stylus_data);
specs_data = nziz(:,35:41); 
specs_data = rmmissing(specs_data);

stylus_dis_matrix = stylus_data(:,5:7); % stylus displacement
specs_dis_matrix = specs_data(:,5:7); % extract the displacement vector out
specs_dis_matrix = rmmissing(specs_dis_matrix);
specs_quaternion_extracted = specs_data(:,1:4);
specs_quaternion_extracted = rmmissing(specs_quaternion_extracted);

% flipping of axis
stylus_dis_matrix = [stylus_dis_matrix(:,1), stylus_dis_matrix(:,3), stylus_dis_matrix(:,2)];
nziz_trace = stylus_dis_matrix;
specs_dis_matrix = [specs_dis_matrix(:,1), specs_dis_matrix(:,3), specs_dis_matrix(:,2)];
specs_quaternion_extracted = [specs_quaternion_extracted(:,4), specs_quaternion_extracted(:,1), specs_quaternion_extracted(:,2), specs_quaternion_extracted(:,3)];

% quaternion_extracted = quaternion_extracted(1:step:end,:);
% dis_matrix_ear2ear = dis_matrix_ear2ear(1:step:end,:);

% Transform w.r.t to specs frame
new_markers_nziz = transform_frame_quat(stylus_dis_matrix, specs_quaternion_extracted, specs_dis_matrix);

%% Doing Ear to Ear 
stylus_data = ear2ear(:,3:9); 
stylus_data = rmmissing(stylus_data);
specs_data = ear2ear(:,35:41); 
specs_data = rmmissing(specs_data);

stylus_dis_matrix = stylus_data(:,5:7); % stylus displacement
specs_dis_matrix = specs_data(:,5:7); % extract the displacement vector out
specs_dis_matrix = rmmissing(specs_dis_matrix);
specs_quaternion_extracted = specs_data(:,1:4);
specs_quaternion_extracted = rmmissing(specs_quaternion_extracted);

% flipping of axis
stylus_dis_matrix = [stylus_dis_matrix(:,1), stylus_dis_matrix(:,3), stylus_dis_matrix(:,2)];
specs_dis_matrix = [specs_dis_matrix(:,1), specs_dis_matrix(:,3), specs_dis_matrix(:,2)];
ear2ear_trace = stylus_dis_matrix;
specs_quaternion_extracted = [specs_quaternion_extracted(:,4), specs_quaternion_extracted(:,1), specs_quaternion_extracted(:,2), specs_quaternion_extracted(:,3)];

% quaternion_extracted = quaternion_extracted(1:step:end,:);
% dis_matrix_ear2ear = dis_matrix_ear2ear(1:step:end,:);

% Transform w.r.t to specs frame
new_markers_e2e = transform_frame_quat(stylus_dis_matrix, specs_quaternion_extracted, specs_dis_matrix);

%% Doing circumference 
stylus_data = circumference(:,3:9); 
stylus_data = rmmissing(stylus_data);
specs_data = circumference(:,35:41); 
specs_data = rmmissing(specs_data);

stylus_dis_matrix = stylus_data(:,5:7); % stylus displacement
specs_dis_matrix = specs_data(:,5:7); % extract the displacement vector out
specs_dis_matrix = rmmissing(specs_dis_matrix);
specs_quaternion_extracted = specs_data(:,1:4);
specs_quaternion_extracted = rmmissing(specs_quaternion_extracted);

% flipping of axis
stylus_dis_matrix = [stylus_dis_matrix(:,1), stylus_dis_matrix(:,3), stylus_dis_matrix(:,2)];
specs_dis_matrix = [specs_dis_matrix(:,1), specs_dis_matrix(:,3), specs_dis_matrix(:,2)];
circumference_trace = stylus_dis_matrix;
specs_quaternion_extracted = [specs_quaternion_extracted(:,4), specs_quaternion_extracted(:,1), specs_quaternion_extracted(:,2), specs_quaternion_extracted(:,3)];

% quaternion_extracted = quaternion_extracted(1:step:end,:);
% dis_matrix_ear2ear = dis_matrix_ear2ear(1:step:end,:);

% Transform w.r.t to specs frame
new_markers_circum = transform_frame_quat(stylus_dis_matrix, specs_quaternion_extracted, specs_dis_matrix);

plot3(new_markers_circum(:,1), new_markers_circum(:,2), new_markers_circum(:,3), '*');
hold on;
plot3(stylus_dis_matrix(:,1), stylus_dis_matrix(:,2), stylus_dis_matrix(:,3), 'd');
legend('Transformed trace', 'original');

return;
%%% GUI

%% Circumferencegi
stylus_data = readmatrix('data_CIRCUMstylus');
stylus_data = [stylus_data(:,1) stylus_data(:,3) stylus_data(:,2)]; 
stylus_data = rmmissing(stylus_data);
GUI_circum_trace = stylus_data;
plot3(GUI_circum_trace(:,1), GUI_circum_trace(:,2), GUI_circum_trace(:,3), 'd');

% stylus_data = stylus_data(1:step:end,:); 

quaternion_extracted = readmatrix('rotation_data_CIRCUMspecs.csv'); % extract the rotation vector out
quaternion_extracted = [quaternion_extracted(:,4), quaternion_extracted(:,1), quaternion_extracted(:,3), quaternion_extracted(:,2)];
% quaternion_extracted = quaternion_extracted(1:step:end,:);

dis_matrix_circum = readmatrix('data_CIRCUMspecs.csv'); % extract the displacement vector out
% dis_matrix_circum = dis_matrix_circum(1:step:end,:); 

%% Run Function to give spec frame points
% Quaternion way
new_markers_circum = [];
new_markers_circum = transform_frame_quat(stylus_data, quaternion_extracted, dis_matrix_circum);

%%% Ear to Ear
stylus_data = readmatrix('data_EarToEarstylus');
stylus_data = [stylus_data(:,1) stylus_data(:,3) stylus_data(:,2)]; 
stylus_data = rmmissing(stylus_data);
GUI_ear2ear_trace = stylus_data;
plot3(GUI_ear2ear_trace(:,1), GUI_ear2ear_trace(:,2), GUI_ear2ear_trace(:,3), 'd');
% stylus_data = stylus_data(1:step:end,:); 

quaternion_extracted = readmatrix('rotation_data_EarToEarspecs'); % extract the rotation vector out
quaternion_extracted = [quaternion_extracted(:,4), quaternion_extracted(:,1), quaternion_extracted(:,3), quaternion_extracted(:,2)];
% quaternion_extracted = quaternion_extracted(1:step:end,:);

dis_matrix_ear2ear = readmatrix('data_EarToEarspecs.csv'); % extract the displacement vector out
% dis_matrix_ear2ear = dis_matrix_ear2ear(1:step:end,:);

%% Run Function to give points
% Quaternion way
new_markers_e2e = [];
new_markers_e2e = transform_frame_quat(stylus_data, quaternion_extracted, dis_matrix_circum);

%%% NZIZ
stylus_data = readmatrix('data_NZIZstylus');
stylus_data = [stylus_data(:,1) stylus_data(:,3) stylus_data(:,2)]; 
stylus_data = rmmissing(stylus_data);
GUI_nziz_trace = stylus_data;
plot3(GUI_ear2ear_trace(:,1), GUI_ear2ear_trace(:,2), GUI_ear2ear_trace(:,3), 'd');

% stylus_data = stylus_data(1:step:end,:);

quaternion_extracted = readmatrix('rotation_data_NZIZspecs'); % extract the rotation vector out
quaternion_extracted = [quaternion_extracted(:,4), quaternion_extracted(:,1), quaternion_extracted(:,3), quaternion_extracted(:,2)];
% quaternion_extracted = quaternion_extracted(1:step:end,:);

dis_matrix_nziz = readmatrix('data_NZIZspecs.csv'); % extract the displacement vector out
% dis_matrix_nziz = dis_matrix_nziz(1:step:end,:); 

%% Run Function to give points
% Quaternion way
new_markers_nziz = [];
new_markers_nziz = transform_frame_quat(stylus_data, quaternion_extracted, dis_matrix_circum);

%%% Circumferene
circumference_dataset= new_markers_circum;

%%% Ear to Ear
e2e_dataset= new_markers_e2e;

%%% NZ-IZ
nziz_dataset =  new_markers_nziz;
