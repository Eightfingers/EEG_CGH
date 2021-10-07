%%% This code would be the final code that is used to determine the 17 EEG
%%% locations. 
%% Add to path different folders containing data and code
%  addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept');
% addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\helperfuncs');
% addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\myfuncs');
% addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Data\30_9_2021');

addpath('30_9_2021');
addpath('helperfuncs');
addpath('myfuncs');

%% Load the different wanded data
circumference = readmatrix('data_NZIZstylus.csv');

circum_quat = readmatrix('quat_circum_shake_30_9_2023.csv');

circum_wand = circumference(:,3:8); 
circum_wand = rmmissing(circum_wand);

circum_specs= circumference(:,34:39); 
circum_specs = rmmissing(circum_specs);

rot_matrix_circum = circum_specs(:,1:3); % extract the rotation vector out
dis_matrix_circum = circum_specs(:,4:6); % extract the displacement vector out
dis_matrix_circum = [dis_matrix_circum(:,1), dis_matrix_circum(:,3), dis_matrix_circum(:,2)];

x_rot_circum = rot_matrix_circum(:,1);
y_rot_circum = rot_matrix_circum(:,3);
z_rot_circum = rot_matrix_circum(:,2);

quaternions = circum_quat(:,35:38);
quaternions = [quaternions(:,4), quaternions(:,1), quaternions(:,2), quaternions(:,3)];
quaternions = rmmissing(quaternions);


new_markers_circum = [];
% Matrix rotation
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

plot3(new_markers_circum(:,1), new_markers_circum(:,2), new_markers_circum(:,3), 'd');
hold on;

% Quaternion way
new_markers_circum2 = [];
for i = 1:1:length(circum_wand)
    
    disp(i);
    quat_vector = quaternion(quaternions(i,:));
    RPY1 = eulerd(quat_vector,'XYZ', 'frame' );
    rot_vector_circum = [RPY1(1), RPY1(3), RPY1(2)];
    dis_vector_circum = dis_matrix_circum(i,:);
    wand_vector_circum = [circum_wand(i,4); ... % X,Y,Z 
              circum_wand(i,6); ...
              circum_wand(i,5); ...
               1];
    transform_matrix_circum = construct_matrix_transform_xyz(dis_vector_circum, rot_vector_circum);    
    new_vector_circum = inv(transform_matrix_circum) * wand_vector_circum;
    new_markers_circum2 = [new_markers_circum; new_vector_circum.';];

end

plot3(new_markers_circum2(:,1), new_markers_circum2(:,2), new_markers_circum2(:,3), 'o', 'MarkerSize',10);

