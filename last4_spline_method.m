addpath('myfuncs/');
addpath('helperfuncs/');
load('shake_6_9.mat');

% MATLAB XYZ convention
final_points = final_points.'
figure;
plot3(final_points(:,1), final_points(:,2), final_points(:,3), 'd');
title('Final points');

xlabel('X');
ylabel('Y');
zlabel('Z');

for i = 1:1:length(final_points)
    text(final_points(i,1), final_points(i,2), final_points(i,3),string(i));
end

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


%% P3 spline approximation
%% Find X
%% Extract out the X and Y values of spline points
spline_pts = [T5; Pz; T6];
x_vector = spline_pts(:,1);
z_vector = spline_pts(:,3);
[xxdata, zzdata] = splineplot(x_vector, z_vector);
[P3_XZ,~,~] = interparc(0.25, xxdata, zzdata,'spline');

% Visual XZ spline plot
figure;
plot(P3_XZ(1), P3_XZ(2) ,'d');
hold on;
plot(x_vector, z_vector, 'o');
plot(xxdata, zzdata);

% Find Y & Z
%% Extract out the Y and Z values of spline points
spline_pts2 = [O1; C3; Fp1];
y_spline = spline_pts2(:,2);
z_spline = spline_pts2(:,3);

[xx_fit2, yy_fit2] = splineplot(y_spline, z_spline);
[P3_YZ,~,~] = interparc(0.25, xx_fit2, yy_fit2,'spline');
P3 = [P3_XZ(1) , P3_YZ(1), P3_YZ(2)];

% Visual YZ spline plot
figure;
plot(P3_YZ(1), P3_YZ(2),'d');
hold on;
plot(y_spline, z_spline, 'o');
plot(xx_fit2, yy_fit2);

%% P4 spline approximation
% % Find X
spline_pts = [T5; Pz; T6];
x_vector = spline_pts(:,1);
z_vector = spline_pts(:,3);
[xxdata, zzdata] = splineplot(x_vector, z_vector);
[P4_XZ,~,~] = interparc(0.75, xxdata, zzdata,'spline');

% Visual XZ spline plot
figure;
plot(P4_XZ(1), P4_XZ(2) ,'d');
hold on;
plot(x_vector, z_vector, 'o');
plot(xxdata, zzdata);

% Find Y & Z
spline_pts3 = [O2; C4; Fp2];
y_spline = spline_pts3(:,2);
z_spline = spline_pts3(:,3);
[yy_fit3, zz_fit3] = splineplot(y_spline, z_spline);

[P4_YZ,~,~] = interparc(0.25, yy_fit3, zz_fit3,'spline');
P4 = [P4_XZ(1) , P4_YZ(1), P4_YZ(2)];

% Visual YZ spline plot
figure;
plot(P4_YZ(1), P4_YZ(2),'d');
hold on;
plot(y_spline, z_spline, 'o');
plot(yy_fit3, zz_fit3);

%% F4 spline approximation
% % Find X
spline_pts4 = [F7; Fz; F8];
x_spline = spline_pts4(:,1);
z_spline = spline_pts4(:,3);
[xxdata4, zzdata4] = splineplot(x_spline, z_spline);
[F4_XZ,~,~] = interparc(0.75, xxdata4,zzdata4,'spline'); % F4 is located from the right 

% Visual XZ spline plot
figure;
plot(F4_XZ(1), F4_XZ(2) ,'d'); % the predicted points
hold on;
plot(x_spline, z_spline, 'o'); % the points
plot(xxdata4, zzdata4); % spline

% Find Z Y Coordinate this spline3 is similar to the one used to find ZY of
% P4 however we find at the 75% position
y_spline = spline_pts3(:,2);
z_spline = spline_pts3(:,3);
[yy_fit3, zz_fit3] = splineplot(y_spline, z_spline);

[P4_YZ,~,~] = interparc(0.25, yy_fit3, zz_fit3,'spline');
P4 = [P4_XZ(1) , P4_YZ(1), P4_YZ(2)];

% Visual YZ spline plot
figure;
plot(P4_YZ(1), P4_YZ(2),'d');
hold on;
plot(y_spline, z_spline, 'o');
plot(yy_fit3, zz_fit3);


%% F3 spline approximation
% % Find X same spline approx as F4 to find x position
spline_pts4 = [F7; Fz; F8];
x_spline = spline_pts4(:,1);
z_spline = spline_pts4(:,3);
[xxdata4, zzdata4] = splineplot(x_spline, z_spline);
[F4_XZ,~,~] = interparc(0.25, xxdata4,zzdata4,'spline'); % F3 is located from the right 

% Visual XZ spline plot
figure;
plot(F4_XZ(1), F4_XZ(2) ,'d'); % the predicted points
hold on;
plot(x_spline, z_spline, 'o'); % the points
plot(xxdata4, zzdata4); % spline

% Find Z and Y
spline_pts2 = [O1; C3; Fp1];
y_spline = spline_pts2(:,2);
z_spline = spline_pts2(:,3);

[yy_fit2, zz_fit2] = splineplot(y_spline, z_spline);
[F3_YZ,~,~] = interparc(0.75, yy_fit2, zz_fit2,'spline');
F3 = [F3_YZ(1) , F3_YZ(1), F3_YZ(2)];

hold on;
plot(F3_YZ(1), F3_YZ(2), 'o');


% Fpz_static = static_points(1,:);
% Fp2_static = static_points(9,:);
% F8_static = static_points(18,:);
% T4_static = static_points(15,:);
% T6_static = static_points(5,:);
% O2_static = static_points(3,:);
% Oz_static = static_points(12,:);
% O1_static = static_points(6,:);
% T5_static = static_points(14,:);
% T3_static = static_points(20,:);
% F7_static = static_points(10,:);
% Fp1_static = static_points(21,:);
% Fz_static = static_points(7,:);
% Cz_static = static_points(16,:);
% Pz_static = static_points(11,:);
% C4_static = static_points(19,:);
% C3_static = static_points(17,:);
% 
% F4_static = static_points(4,:);
% 
% F3_static = static_points(2,:);
% 
% P3_static = static_points(8,:);
% 
% P4_static = static_points(13,:);
% 
% 
% Fpz_diff = norm(Fpz -Fpz_static);
% Fp2_diff = norm(Fp2 -Fp2_static);
% F8_diff = norm(F8 - F8_static);
% T4_diff = norm(T4 -T4_static);
% T6_diff = norm(T6 -T6_static);
% O2_diff = norm(O2 -O2_static);
% Oz_diff =norm(Oz -Oz_static);
% O1_diff = norm(O1 -O1_static);
% T5_diff = norm(T5 -T5_static);
% T3_diff = norm(T3 -T3_static);
% F7_diff = norm(F7 -F7_static);
% Fp1_diff = norm(Fp1 -Fp1_static);
% Fz_diff = norm(Fz -Fz_static);
% Cz_diff = norm(Cz -Cz_static);
% Pz_diff = norm(Pz -Pz_static);
% C4_diff = norm(C4 -C4_static);5
% C3_diff = norm(C3 -C3_static);
% 
% F4_diff = norm(F4 - F4_static)
% 
% F3_diff = norm(F3 - F3_static)
% 
% P3_diff = norm(P3 - P3_static)
% 
% P4_diff = norm(P4 - P4_static)

figure;
predicted = [Fpz; Fp2; F8; T4; T6; O2; Oz; O1; T5; T3; F7; Fp1; Fz; Cz; Pz; C4; C3; F4; F3; P3; P4 ];
hold on;
plot3(predicted(:,1), predicted(:,2), predicted(:,3), 'd');
plot3(F4(1), F4(2), F4(3), 'kd');
xlabel('x');
ylabel('y');
zlabel('z');
