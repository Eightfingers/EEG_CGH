% matlab_style = readmatrix('global_location.csv');
% python_style = readmatrix('python_transform.csv');
% python_style2 = readmatrix('python_transform2.csv');
% python_style3 = readmatrix('python_transform3.csv');

python_style3 = readmatrix('circum_python_transformtest2.csv');
actual = readmatrix('circum_untransformed.csv');
matlab_style = readmatrix('circum_transformed_spec_position.csv');

figure;
hold on;
plot3(python_style3(:,1), python_style3(:,2), python_style3(:,3), '*');
plot3(actual(:,1), actual(:,2), actual(:,3), 'd');
plot3(matlab_style(:,1), matlab_style(:,2), matlab_style(:,3), 'd');

% plot3(python_style2(:,1), python_style2(:,2), python_style2(:,3), 'd');
% plot3(python_style3(:,1), python_style3(:,2), python_style3(:,3), 'rd');

d = matlab_style - python_style;
d_offset = vecnorm(d, 2,2);
% 
% quat = quaternion([0.7071 0.7071 0 0]);
% eulerAnglesDegrees = eulerd(quat,'XYZ','point')
