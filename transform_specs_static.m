%% This script transforms static points to w.r.t specs frame

addpath('../test_codes/helperfuncs');
addpath('../test_codes/myfuncs');
addpath('8_9_2021');

data2 = readmatrix('static_specs_001.csv');
specs = data2(:,3:8); 
markers = data2(:,26:100); 
first_row = markers(8,:);
first_row_rot = specs(8,1:3);
first_row_displacement = specs(8,4:6);
specs = rmmissing(specs);

static_markers = [];
% The for loop starts at 3 as the first 2 columns of the csv files are
% not marker points. It steps up by 3 as each marker points has 3
% coordinates (x,y,z) so i is always 3,6,9 ...

for i = 1:3:length(first_row)
    disp(i)
    static_markers = [static_markers; first_row(i),first_row(i+2),first_row(i+1)];
end

plot3(static_markers(:,1), static_markers(:,2), static_markers(:,3), '*');

%% before transform;
Xrot = first_row_rot(1);
Yrot = first_row_rot(3);
Zrot = first_row_rot(2);
new_markers = [];

for i = 1:1:length(static_markers)
    d = first_row_displacement; % displacement vector
    v = [ 0, 0 ,0 1];
    rot_matrix = [-Xrot, -Yrot, -Zrot];
    transform_matrix = construct_matrix_transform_xyz(d, rot_matrix);    
    marker = [static_markers(i,1); ... % X,Y,Z 
              static_markers(i,2); ...
              static_markers(i,3); ...
               1];
           
    new_vector = inv(transform_matrix) * marker;
    new_markers = [new_markers; new_vector.';];

end

%% Need 2 manuall remove the spectacle markers
plot3(new_markers(:,1), new_markers(:,2), new_markers(:,3),'ko');
hold on;
