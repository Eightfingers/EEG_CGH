addpath('helperfuncs');
addpath('myfuncs');
addpath('13_9_2021');

data = readmatrix('circum2_shake_005.csv');
specs = data(:,3:8); 
specs = rmmissing(specs);
wand= data(:,38:43); 
wand = rmmissing(wand);

%% Remove some rows and trimming
wand = wand(:, :); 
specs = specs(:, :);
rot_matrix = specs(:,1:3); % extract the rotation vector out

dis_matrix = specs(:,4:6); % extract the displacement vector out

dis_matrix = [dis_matrix(:,1), dis_matrix(:,3), dis_matrix(:,2)];

x_rot = rot_matrix(:,1);
y_rot = rot_matrix(:,3);
z_rot = rot_matrix(:,2);

%% Loop through all the data set
new_markers = [];

rot_matrix2 = rotx(-x_rot(1)) * roty(-y_rot(1)) * rotz(-z_rot(1));

for i = 1:1:length(wand)
    disp(i);
    rot_vector = [-x_rot(i), -y_rot(i), -z_rot(i)];
%     rot_vector = [-z_rot(i), -y_rot(i), -x_rot(i)];

    dis_vector = dis_matrix(i,:);
    transform_matrix = construct_matrix_transform_xyz(dis_vector, rot_vector);    
    
    wand_vector = [wand(i,4); ... % X,Y,Z 
              wand(i,6); ...
              wand(i,5); ...
               1];

    new_vector = inv(transform_matrix) * wand_vector;
    new_markers = [new_markers; new_vector.';];
end

plot3(new_markers(:,1), new_markers(:,2), new_markers(:,3), 'd');
hold on;
plot3(wand(:,4), wand(:, 6), wand(:,5),'*');
plot3(specs(:,4), specs(:, 6), specs(:,5),'o');
legend("Transformed", "Wand", "Specs");

plot3(wand(1,4), wand(1, 6), wand(1,5),'s', 'MarkerSize',10);
plot3(new_markers(1,1), new_markers(1, 2), new_markers(1,3),'s', 'MarkerSize',10);


xlabel("X");
ylabel("y");
zlabel("z");

return;