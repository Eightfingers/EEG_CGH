% matlab_style = readmatrix('global_location.csv');
% python_style = readmatrix('python_transform.csv');

python_style3 = readmatrix('circum_shake_transform_python.csv');
actual = readmatrix('circum_shake_untransformed_trace.csv');
matlab_style = readmatrix('circum_shake_transformed_trace_matlab.csv');

figure;
hold on;
plot3(python_style3(:,3), python_style3(:,2), python_style3(:,1), '*');
plot3(actual(:,1), actual(:,2), actual(:,3), 'd');
plot3(matlab_style(:,1), matlab_style(:,2), matlab_style(:,3), 'yd');


d = matlab_style - python_style;
d_offset = vecnorm(d, 2,2);
% 
% quat = quaternion([0.7071 0.7071 0 0]);
% eulerAnglesDegrees = eulerd(quat,'XYZ','point')
