%%% This code would be the final code that is used to determine the 17 EEG
%%% locations. 
%% Add to path different folders containing data and code
% function [predicted] = notransform_conformal2Dmidpoint()
tic;

%%% Circumference
addpath('..\..\Python\Main\matlab_funcs\helperfuncs\');
addpath('..\..\Python\Main\matlab_funcs\myfuncs\');
% addpath('NotWorking\');
step = 5; % used to take only every 2nd data

%%% NZIZ
new_markers_nziz = readmatrix('data_NZIZstylus')
step = 5; % used to take only every 2nd data
new_markers_nziz = new_markers_nziz(1:step:end,:); 
new_markers_nziz = [new_markers_nziz(:,1) new_markers_nziz(:,3) new_markers_nziz(:,2)]; 

%%% Ear to Ear
new_markers_e2e = readmatrix('data_EarToEarstylus')
step = 5; % used to take only every 2nd data
new_markers_e2e = new_markers_e2e(1:step:end,:); 
new_markers_e2e = [new_markers_e2e(:,1) new_markers_e2e(:,3) new_markers_e2e(:,2)]; 

%%% Circum
new_markers_circum = readmatrix('data_CIRCUMstylus')
step = 5; % used to take only every 2nd data
new_markers_circum = new_markers_circum(1:step:end,:); 
new_markers_circum = [new_markers_circum(:,1) new_markers_circum(:,3) new_markers_circum(:,2)]; 

plot3(new_markers_circum(:,1), new_markers_circum(:,2), new_markers_circum(:,3), 'd');
hold on;
plot3(new_markers_e2e(:,1), new_markers_e2e(:,2), new_markers_e2e(:,3), 'o');
plot3(new_markers_nziz(:,1), new_markers_nziz(:,2), new_markers_nziz(:,3), '*');


%%% Circumferene
circumference_dataset= new_markers_circum;
circumference_dataset = rmmissing(circumference_dataset);
% circumference_x = circumference_dataset(:,1);
% circumference_y = circumference_dataset(:,2);
% circumference_z = circumference_dataset(:,3);
%%% Ear to Ear
e2e_dataset= new_markers_e2e;
e2e_dataset = rmmissing(e2e_dataset);
% e2e_x = e2e_dataset(:,1);
% e2e_y = e2e_dataset(:,2);
% e2e_z = e2e_dataset(:,3);
%%% NZ-IZ
nziz_dataset =  new_markers_nziz;
nziz_dataset = rmmissing(nziz_dataset);
% nziz_x = nziz_dataset(:,1);
% nziz_y = nziz_dataset(:,2);
% nziz_z = nziz_dataset(:,3);

%% Ellipsoid Fitting
collated_data = [circumference_dataset; e2e_dataset; nziz_dataset];
X_circum = collated_data(:,1);
Y_circum = collated_data(:,2);
Z_circum = collated_data(:,3);
% CART = [x,y,z];
[center1, radii, ~, v, chi2 ] = ellipsoid_fit_new( [X_circum Y_circum Z_circum],'' );
fprintf( 'Ellipsoid center: %.5g %.5g %.5g\n', center1 );
fprintf( 'Ellipsoid radii: %.5g %.5g %.5g\n', radii );
%% Draw Ellipsoid Fit
mind = min( [ X_circum Y_circum Z_circum] );
maxd = max( [ X_circum Y_circum Z_circum  ] );
nsteps = 60;
step = ( maxd - mind ) / nsteps;
[ x, y, z ] = meshgrid( linspace( mind(1) - step(1), maxd(1) + step(1), nsteps ), linspace( mind(2) - step(2), maxd(2) + step(2), nsteps ), linspace( mind(3) - step(3), maxd(3) + step(3), nsteps ) );
Ellipsoid = v(1) *x.*x +   v(2) * y.*y + v(3) * z.*z + ...
          2*v(4) *x.*y + 2*v(5)*x.*z + 2*v(6) * y.*z + ...
          2*v(7) *x    + 2*v(8)*y    + 2*v(9) * z;
%% Shift Points to (0,0,0) Centre
x = x - center1(1); % shift the center of ellipsoid to 0 0 0
y = y - center1(2);
z = z - center1(3);

X_circum = X_circum - center1(1); % shift the static points to the center too
Y_circum = Y_circum - center1(2);
Z_circum = Z_circum - center1(3);
shifted_static_markers = [X_circum, Y_circum, Z_circum];
%% Plot Shifted Points
plot3(X_circum, Y_circum, Z_circum, 'r*');
hold on;
axis equal
set(gca,'DataAspectRatio',[1 1 1])
%% Plot Ellipsoid Fit
surface = isosurface( x, y, z, Ellipsoid, -v(10) );
p = patch( surface );
set( p, 'FaceColor', 'g', 'EdgeColor', 'none');
% alpha(0.3);
axis equal;
camlight;
%% Project the static points to the 3D ellipsoid and plot them 
loop_step = 2;
points = surface.vertices;
projected_ellipsoid_points = shortest_pt2pt(shifted_static_markers, points,loop_step); % find the nearest point that lies on the ellipsoid from the static points
% plot3(projected_ellipsoid_points(:,1),projected_ellipsoid_points(:,2),projected_ellipsoid_points(:,3),'d');
% 
% % for i = 1:1:length(projected_ellipsoid_points)
% %     text(projected_ellipsoid_points(i,1), projected_ellipsoid_points(i,2), projected_ellipsoid_points(i,3),string(i));
% % end

a = radii(1) ;
b = radii(2);
c = radii(3);
e = sqrt(a^2- b^2)/a;
e_2 = (1 - (a^2 - b) )^1/2;
ellipsoid = [a, e_2];
%% Extract Projected points to x,y,z
proj_x = projected_ellipsoid_points(:,1);
proj_y = projected_ellipsoid_points(:,2);
proj_z = projected_ellipsoid_points(:,3);
%% Convert geocentric points to Geographic Coordinates
%%% Geocentric to Geographic 
[latpoints, lonpoints, h, ~] = geocent_inv(proj_x,proj_y,proj_z, ellipsoid);
%% Find Centre at the top of the head
[latcentre_top, loncentre_top, hcentre_top, ~] = geocent_inv(0,0,c,ellipsoid);
%% Extract Lat, Lon and h of the circumference datasets
%%% Circumference
length_of_circum = length(circumference_dataset);
projpoints_circum = projected_ellipsoid_points(1:length_of_circum,:);
latpoints_circum = latpoints(1:length_of_circum,:);
lonpoints_circum = lonpoints(1:length_of_circum,:);
hpoints_circum = h(1:length_of_circum,:);
%% Project all  circumference datasets (Azimuthal Equidistant)
%%% Circumference
[x_new_top_circum, y_new_top_circum, azi, rk] = eqdazim_fwd(latcentre_top,loncentre_top, latpoints_circum, lonpoints_circum, ellipsoid);
% figure;
% scatter(x_new_top_circum,y_new_top_circum,'bd');
% legend('Circumference');
% title('Azimuthal Equidistant Projection');
% axis equal
%% 2D Geometerical Fitting
f1= figure('Name',' Circumference');
Ellipse=([x_new_top_circum, y_new_top_circum]);
plot(x_new_top_circum, y_new_top_circum,'*')';
[centre, a, b, alpha] = fitellipse(Ellipse,'linear');
plotellipse(centre, a, b, alpha, 'b-');
f1 = gcf; %current figure handle
axesObjs = get(f1, 'Children');  %axes handles
dataObjs = get(axesObjs, 'Children'); %handles t
xdata_circum = get(dataObjs, 'XData'); 
ydata_circum = get(dataObjs, 'YData');
start_A = [x_new_top_circum, y_new_top_circum];
startpoint_2d_circum = [start_A(1,1) start_A(1,end)];
newmat_xy = [xdata_circum; ydata_circum];
trans_newmat_xy = newmat_xy.';
dist_startpoint_circum = sqrt(sum(bsxfun(@minus, trans_newmat_xy, startpoint_2d_circum).^2,2));
closest_startpoint_circum = trans_newmat_xy(find(dist_startpoint_circum==min(dist_startpoint_circum)),:);
[row_circum,~] = find(trans_newmat_xy==closest_startpoint_circum);
new_matrix_x_circum = [trans_newmat_xy(row_circum:2000,1); trans_newmat_xy(1:row_circum-1,1)].';
new_matrix_y_circum = [trans_newmat_xy(row_circum:2000,2); trans_newmat_xy(1:row_circum-1,2)].';
%% Predicting EEG Positions in 2D
%%% Circumference - 13 positions (first and last being the same)
[pt_circum,~,~] = interparc(0,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt1_circum,~,~] = interparc(0.05,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt2_circum,~,~] = interparc(0.15,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt3_circum,~,~] = interparc(0.25,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt4_circum,~,~] = interparc(0.35,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt5_circum,~,~] = interparc(0.45,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt6_circum,~,~] = interparc(0.50,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt7_circum,~,~] = interparc(0.55,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt8_circum,~,~] = interparc(0.65,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt9_circum,~,~] = interparc(0.75,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt10_circum,~,~] = interparc(0.85,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt11_circum,~,~] = interparc(0.95,new_matrix_x_circum , new_matrix_y_circum,'linear');
[pt12_circum,~,~] = interparc(1,new_matrix_x_circum , new_matrix_y_circum,'linear');
%% Collate Predicted Data Points
%%% Circuference
circum = [pt_circum.' pt1_circum.' pt2_circum.' pt3_circum.' pt4_circum.' pt5_circum.' pt6_circum.' pt7_circum.' pt8_circum.' pt9_circum.' pt10_circum.' pt11_circum.' ];
circum_x = circum(1,:);
circum_y = circum(end,:);
circum = circum.';
% figure;
% scatter(circum(:,1),circum(:,end));
% for i = 1:1:length(circum)
%     text(circum(i,1), circum(i,2),string(i));
% end
%% Find other points using circumference points
Cz = [(circum(1,1)+ circum(7,1))/2 , (circum(1,end)+ circum(7,end))/2];
Pz = [(Cz(1,1)+ circum(7,1))/2 , (Cz(1,end)+ circum(7,end))/2];
Fz = [(Cz(1,1)+ circum(1,1))/2 , (Cz(1,end)+ circum(1,end))/2];

C3 = [(circum(2,1)+ circum(6,1))/2 , (circum(2,end)+ circum(6,end))/2];
P3 = [(C3(1,1)+ circum(6,1))/2 , (C3(1,end)+ circum(6,end))/2];
F3 = [(C3(1,1)+ circum(2,1))/2 , (C3(1,end)+ circum(2,end))/2];

C4 = [(circum(12,1)+ circum(8,1))/2 , (circum(12,end)+ circum(8,end))/2];
P4 = [(C4(1,1)+ circum(8,1))/2 , (C4(1,end)+ circum(8,end))/2];
F4 = [(C4(1,1)+ circum(12,1))/2 , (C4(1,end)+ circum(12,end))/2];

Cz_1 = [(circum(4,1)+ circum(10,1))/2 , (circum(4,end)+ circum(10,end))/2];
C3_1 = [(Cz_1(1,1)+ circum(4,1))/2 , (Cz_1(1,end)+ circum(4,end))/2];
C4_1 = [(Cz_1(1,1)+ circum(10,1))/2 , (Cz_1(1,end)+ circum(10,end))/2];

Fz_1 = [(circum(3,1)+ circum(11,1))/2 , (circum(3,end)+ circum(11,end))/2];
F3_1 = [(Fz_1(1,1)+ circum(3,1))/2 , (Fz_1(1,end)+ circum(3,end))/2];
F4_1 = [(Fz_1(1,1)+ circum(11,1))/2 , (Fz_1(1,end)+ circum(11,end))/2];

Pz_1 = [(circum(5,1)+ circum(9,1))/2 , (circum(5,end)+ circum(9,end))/2];
P3_1 = [(Pz_1(1,1)+ circum(5,1))/2 , (Pz_1(1,end)+ circum(5,end))/2];
P4_1 = [(Pz_1(1,1)+ circum(9,1))/2 , (Pz_1(1,end)+ circum(9,end))/2];

%% Find midpoint

Cz = [(Cz(1,1)+ Cz_1(1,1))/2 , (Cz(1,end)+ Cz_1(1,end))/2];
Pz = [(Pz(1,1)+ Pz_1(1,1))/2 , (Pz(1,end)+ Pz_1(1,end))/2];
Fz = [(Fz(1,1)+ Fz_1(1,1))/2 , (Fz(1,end)+ Fz_1(1,end))/2];

C3 = [(C3(1,1)+ C3_1(1,1))/2 , (C3(1,end)+ C3_1(1,end))/2];
P3 = [(P3(1,1)+ P3_1(1,1))/2 , (P3(1,end)+ P3_1(1,end))/2];
F3 = [(F3(1,1)+ F3_1(1,1))/2 , (F3(1,end)+ F3_1(1,end))/2];

C4 = [(C4(1,1)+ C4_1(1,1))/2 , (C4(1,end)+ C4_1(1,end))/2];
P4 = [(P4(1,1)+ P4_1(1,1))/2 , (P4(1,end)+ P4_1(1,end))/2];
F4 = [(F4(1,1)+ F4_1(1,1))/2 , (F4(1,end)+ F4_1(1,end))/2];

all_points = [circum; Cz; Pz ;Fz; C3; P3; F3; C4; P4; F4];
all_points_x = all_points(:,1);
all_points_y = all_points(:,end);

predicted = all_points;

%% Inverse Projection to Lat and Lon
%%% Circumference
[lat_inv_pred, lon_inv_pred, azi, rk] = eqdazim_inv(latcentre_top, loncentre_top, all_points_x, all_points_y, ellipsoid);
% figure;
% axesm('MapProjection','eqdazim', 'Geoid',[a e_2],'Origin',[latcentre_top, loncentre_top 0]);
% scatterm(lat_inv_pred, lon_inv_pred);
%% Inverse to geocentric coordinates
[X, Y, Z] = geocent_fwd(lat_inv_pred, lon_inv_pred,0,ellipsoid);

X = X + center1(1);
Y = Y + center1(2);
Z = Z + center1(3);

predicted = [X,Y,Z];
figure;
% scatter3(X,Y,Z);
hold on;
plot3(X,Y,Z, 'd');


%% Compare to Static
% first_row_static = static(9,:);
% 
% % The for loop starts at 3 as the first 2 columns of the csv files are
% % not marker points. It steps up by 3 as each marker points has 3
% % coordinates (x,y,z) so i is always 3,6,9 ...
% 
% static_new = [];
% for i = 3:3:length(first_row_static)
%     disp(i)
%     static_new = [static_new; first_row_static(i),first_row_static(i+2),first_row_static(i+1)];
% end
% 
% % static_new = static_new *R;
% 
% static_x = static_new(:,1)- center1(1);
% static_y = static_new(:,2)- center1(2);
% static_z = static_new(:,3)- center1(3);
% 
% 
% static_new = [static_x static_y static_z];
% 
% figure;
% plot3(X,Y,Z,'d');
% hold on
% scatter3(static_x,static_y,static_z,'r*');
% title('Static vs Predicted - Ellipsoid Fit')
% legend('Predicted','Static')

% %% Labelling Static and PRedicted Points
% final_points = [X Y Z];
% % figure;
% % plot3(final_points(:,1), final_points(:,2), final_points(:,3), 'd');
% % title('Final points');
% % for i = 1:1:length(final_points)
% %     text(final_points(i,1), final_points(i,2), final_points(i,3),string(i));
% % end
% 
% %%% Labelling of points - Predicted
% Fpz = final_points(1,:);
% Fp2 = final_points(12,:);
% F8 = final_points(11,:);
% T4 = final_points(10,:);
% T6 = final_points(9,:);
% O2 = final_points(8,:);
% Oz = final_points(7,:);
% O1 = final_points(6,:);
% T5 = final_points(5,:);
% T3 = final_points(4,:);
% F7 = final_points(3,:);
% Fp1 = final_points(2,:);
% Fz = final_points(16,:);
% Cz = final_points(14,:);
% Pz = final_points(17,:);
% C4 = final_points(13,:);
% C3 = final_points(15,:);
% F4 = final_points(18,:);
% F3 = final_points(19,:);
% P4 = final_points(21,:);
% P3 = final_points(20,:);
% %%% Static
% figure;
% scatter3(static_new(:,1), static_new(:,2),static_new(:,3));
% title('Static Points')
% for i = 1:1:length(static_new)
%     text(static_new(i,1), static_new(i,2), static_new(i,3),string(i));
% end
% 
% %%% Labelling of points - Static
% Fpz_static = static_new(14,:);
% Fp2_static = static_new(10,:);
% F8_static = static_new(5,:);
% T4_static = static_new(3,:);
% T6_static = static_new(4,:);
% O2_static = static_new(9,:);
% Oz_static = static_new(1,:);
% O1_static = static_new(2,:);
% T5_static = static_new(18,:);
% T3_static = static_new(21,:);
% F7_static = static_new(20,:);
% Fp1_static = static_new(15,:);
% Fz_static = static_new(13,:);
% Cz_static = static_new(12,:);
% Pz_static = static_new(11,:);
% C4_static = static_new(6,:);
% C3_static = static_new(19,:);
% F4_static = static_new(8,:);
% F3_static = static_new(17,:);
% P4_static = static_new(7,:);
% P3_static = static_new(16,:);
% 
% %% Euclidean Error
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
% C4_diff = norm(C4 -C4_static);
% C3_diff = norm(C3 -C3_static);
% F4_diff = norm(F4 - F4_static);
% F3_diff = norm(F3 - F3_static);
% P3_diff = norm(P3 - P3_static);
% P4_diff = norm(P4 - P4_static);
% 
% 
% error = [Fpz_diff; Fp2_diff; F8_diff; T4_diff; T6_diff; O2_diff; Oz_diff; O1_diff; T5_diff; T3_diff; F7_diff; Fp1_diff; Fz_diff; ...
% Cz_diff; Pz_diff; C4_diff; C3_diff; F4_diff; F3_diff; P3_diff; P4_diff];
% 
% elapsedtime_2=toc;
% disp(elapsedtime_2);

% end













