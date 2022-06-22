%%% This code would be the final code that is used to determine the 21 EEG
%%% locations. 
%% Add to path different folders containing data and code

%%% Circumference
addpath('..\..\Python\Main\matlab_funcs\helperfuncs\');
addpath('..\..\Python\Main\matlab_funcs\myfuncs\');

tic;
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

hold on;
plot3(new_markers_circum(:,1)-center1(1) , new_markers_circum(:,2)- center1(2), new_markers_circum(:,3) - center1(3), 'd');
plot3(new_markers_e2e(:,1), new_markers_e2e(:,2), new_markers_e2e(:,3), 'o');
plot3(new_markers_nziz(:,1), new_markers_nziz(:,2), new_markers_nziz(:,3), '*');


%% Ellipsoid Fitting
collated_data = [circumference_dataset; e2e_dataset; nziz_dataset];
X_circum = collated_data(:,1);
Y_circum = collated_data(:,2);
Z_circum = collated_data(:,3);
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

% for i = 1:1:length(projected_ellipsoid_points)
%     text(projected_ellipsoid_points(i,1), projected_ellipsoid_points(i,2), projected_ellipsoid_points(i,3),string(i));
% end

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
length_of_circum = length(circumference_dataset);
length_of_e2e = length(e2e_dataset);
length_of_nziz = length(nziz_dataset);
projpoints_circum = projected_ellipsoid_points(1:length_of_circum,:);
projpoints_e2e = projected_ellipsoid_points(length_of_circum +1:(length_of_circum + length_of_e2e) ,:);
projpoints_nziz = projected_ellipsoid_points((length_of_circum + length_of_e2e)+1:end , :);
[latcentre_top, loncentre_top, hcentre_top, ~] = geocent_inv(0,0,c,ellipsoid);
%% Extract Lat, Lon and h of the 3 individual datasets
%%% Circumference
latpoints_circum = latpoints(1:length_of_circum,:);
lonpoints_circum = lonpoints(1:length_of_circum,:);
hpoints_circum = h(1:length_of_circum,:);
%%% Ear to Ear
latpoints_e2e = latpoints(length_of_circum +1:(length_of_circum + length_of_e2e) ,:);
lonpoints_e2e = lonpoints(length_of_circum +1:(length_of_circum + length_of_e2e) ,:);
hpoints_e2e = h(length_of_circum +1:(length_of_circum + length_of_e2e) ,:);
%%% Nasion to Inion
latpoints_nziz = latpoints((length_of_circum + length_of_e2e)+1:end , :);
lonpoints_nziz = lonpoints((length_of_circum + length_of_e2e)+1:end , :);
hpoints_nziz = h((length_of_circum + length_of_e2e)+1:end , :);
%% Project all 3 datasets (Azimuthal Equidistant)
%%% Circumference
[x_new_top_circum, y_new_top_circum, azi, rk] = eqdazim_fwd(latcentre_top,loncentre_top, latpoints_circum, lonpoints_circum, ellipsoid);

%%% Ear to Ear
[x_new_top_e2e, y_new_top_e2e, azi, rk] = eqdazim_fwd(latcentre_top,loncentre_top, latpoints_e2e, lonpoints_e2e, ellipsoid);


%%% Nasion to Inion
[x_new_top_nziz, y_new_top_nziz, azi, rk] = eqdazim_fwd(latcentre_top,loncentre_top, latpoints_nziz, lonpoints_nziz, ellipsoid);

% % figure;
% hold on
scatter(x_new_top_circum,y_new_top_circum);
hold on
% scatter(x_new_top_e2e,y_new_top_e2e);
% hold on
% scatter(x_new_top_nziz,y_new_top_nziz);
% % legend('Circumference', 'Ear to Ear', 'Nasion to Inion');
% % title('Azimuthal Equidistant Projection');
% axis equal

%% 2D Geometerical Fitting
f1= figure('Name',' Circumference');
Ellipse=([x_new_top_circum, y_new_top_circum]);
[centre, a, b, alpha] = fitellipse(Ellipse,'linear');
hold on;
plotellipse(centre, a, b, alpha, 'b-');
f1 = gcf; %current figure handle
axesObjs = get(f1, 'Children');  %axes handles
dataObjs = get(axesObjs, 'Children'); %handles t
xdata_circum = get(dataObjs, 'XData'); 
ydata_circum = get(dataObjs, 'YData');
start_A = [x_new_top_circum, y_new_top_circum];

startpoint_2d_circum = [start_A(1,1) start_A(1,end)];
newmat_yx = [xdata_circum; ydata_circum];
trans_newmat_xy = newmat_yx.';
dist_startpoint_circum = sqrt(sum(bsxfun(@minus, trans_newmat_xy, startpoint_2d_circum).^2,2));
closest_startpoint_circum = trans_newmat_xy(find(dist_startpoint_circum==min(dist_startpoint_circum)),:);
[row_circum,~] = find(trans_newmat_xy==closest_startpoint_circum);
new_matrix_x_circum = [trans_newmat_xy(row_circum:2000,1); trans_newmat_xy(1:row_circum-1,1)].';
new_matrix_y_circum = [trans_newmat_xy(row_circum:2000,2); trans_newmat_xy(1:row_circum-1,2)].';

%%% Ear to Ear - The ear to ear tracking data is considered as a spline
spline_e2e = splinetest_e2e(y_new_top_e2e, x_new_top_e2e);
points = fnplt(spline_e2e);
ydata_e2e = points(1,:);
xdata_e2e = points(2,:);

start_B = [y_new_top_e2e, x_new_top_e2e];
startpoint_2d_e2e = [start_B(1,1) start_B(1,end)];
endpoint_2d_e2e = [start_B(end,1) start_B(end,end)];

newmat_yx = [ydata_e2e; xdata_e2e];
trans_newmat_yx = newmat_yx.';

dist_startpoint_e2e = sqrt(sum(bsxfun(@minus, trans_newmat_yx, startpoint_2d_e2e).^2,2));
closest_startpoint_e2e = trans_newmat_yx(find(dist_startpoint_e2e==min(dist_startpoint_e2e)),:);

dist_endpoint_e2e = sqrt(sum(bsxfun(@minus, trans_newmat_yx, endpoint_2d_e2e).^2,2));
closest_endpoint_e2e = trans_newmat_yx(find(dist_endpoint_e2e==min(dist_endpoint_e2e)),:);

[row_startpoint_e2e,~] = find(trans_newmat_yx==closest_startpoint_e2e);
[row_endpoint_e2e,~] = find(trans_newmat_yx==closest_endpoint_e2e);

new_matrix_y_e2e = (trans_newmat_yx(row_endpoint_e2e:row_startpoint_e2e,1)).';
new_matrix_x_e2e = (trans_newmat_yx(row_endpoint_e2e:row_startpoint_e2e,2)).';

%%% NZ-IZ - The NZIZ tracking data is considered as a spline 

spline_nziz = splinetest_e2e(x_new_top_nziz, y_new_top_nziz);
points = fnplt(spline_nziz);
xdata_nziz = points(1,:);
ydata_nziz = points(2,:);

start_C = [x_new_top_nziz, y_new_top_nziz];
startpoint_2d_nziz = [start_C(1,1) start_C(1,end)];
endpoint_2d_nziz = [start_C(end,1) start_C(end,end)];

newmat_xy_nziz = [xdata_nziz; ydata_nziz];
trans_newmat_xy_nziz = newmat_xy_nziz.';

dist_startpoint_nziz = sqrt(sum(bsxfun(@minus, trans_newmat_xy_nziz, startpoint_2d_nziz).^2,2));
closest_startpoint_nziz = trans_newmat_xy_nziz(find(dist_startpoint_nziz==min(dist_startpoint_nziz)),:);

dist_endpoint_nziz = sqrt(sum(bsxfun(@minus, trans_newmat_xy_nziz, endpoint_2d_nziz).^2,2));
closest_endpoint_nziz = trans_newmat_xy_nziz(find(dist_endpoint_nziz==min(dist_endpoint_nziz)),:);

[row_startpoint_nziz,~] = find(trans_newmat_xy_nziz==closest_startpoint_nziz);
[row_endpoint_nziz,~] = find(trans_newmat_xy_nziz==closest_endpoint_nziz);

new_matrix_x_nziz = (trans_newmat_xy_nziz(row_endpoint_nziz:row_startpoint_nziz,1)).';
new_matrix_y_nziz = (trans_newmat_xy_nziz(row_endpoint_nziz:row_startpoint_nziz,2)).';

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
%%% Ear to Ear
[pt13_e2e,~,~] = interparc(0,new_matrix_x_e2e,new_matrix_y_e2e,'spline');
[pt14_e2e,~,~] = interparc(0.1,new_matrix_x_e2e,new_matrix_y_e2e,'spline');
[pt15_e2e,~,~] = interparc(0.3,new_matrix_x_e2e,new_matrix_y_e2e,'spline');
[pt16_e2e,~,~] = interparc(0.5,new_matrix_x_e2e,new_matrix_y_e2e,'spline');
[pt17_e2e,~,~] = interparc(0.7,new_matrix_x_e2e,new_matrix_y_e2e,'spline');
[pt18_e2e,~,~] = interparc(0.9,new_matrix_x_e2e,new_matrix_y_e2e,'spline');
[pt19_e2e,~,~] = interparc(1,new_matrix_x_e2e,new_matrix_y_e2e,'spline');
%%% NZIZ 
[pt20_nziz,~,~] = interparc(0,new_matrix_x_nziz,new_matrix_y_nziz,'spline');
[pt21_nziz,~,~] = interparc(0.1,new_matrix_x_nziz,new_matrix_y_nziz,'spline');
[pt22_nziz,~,~] = interparc(0.3,new_matrix_x_nziz,new_matrix_y_nziz,'spline');
[pt23_nziz,~,~] = interparc(0.50,new_matrix_x_nziz,new_matrix_y_nziz,'spline');
[pt24_nziz,~,~] = interparc(0.7,new_matrix_x_nziz,new_matrix_y_nziz,'spline');
[pt25_nziz,~,~] = interparc(0.9,new_matrix_x_nziz,new_matrix_y_nziz,'spline');
[pt26_nziz,~,~] = interparc(1,new_matrix_x_nziz,new_matrix_y_nziz,'spline');

%% Collate Predicted Data Points
%%% Circuference
circum = [pt_circum.' pt1_circum.' pt2_circum.' pt3_circum.' pt4_circum.' pt5_circum.' pt6_circum.' pt7_circum.' pt8_circum.' pt9_circum.' pt10_circum.' pt11_circum.' ];
circum_x = circum(1,:);
circum_y = circum(end,:);
%%% Ear to Ear
e2e = [ pt15_e2e.' pt16_e2e.' pt17_e2e.' ];
e2e_x = e2e(1,:);
e2e_y = e2e(end,:);
%%% NZIZ
nziz = [ pt24_nziz.' pt22_nziz.' ];
nziz_x = nziz(1,:);
nziz_y = nziz(end,:);

% figure;
% hold on
% scatter(circum(1,:),circum(end,:));
% hold on
% scatter(e2e(1,:),e2e(end,:));
% hold on
% scatter(nziz(1,:),nziz(end,:));
%% Inverse Projection to Lat and Lon
%%% Circumference
[lat_inv_circum, lon_inv_circum, azi, rk] = eqdazim_inv(latcentre_top, loncentre_top, circum_x, circum_y, ellipsoid);
%%% Ear to Ear
[lat_inv_e2e, lon_inv_e2e, azi, rk] = eqdazim_inv(latcentre_top, loncentre_top, e2e_x, e2e_y, ellipsoid);
%%% Naion to Inion
[lat_inv_nziz, lon_inv_nziz, azi, rk] = eqdazim_inv(latcentre_top, loncentre_top, nziz_x, nziz_y, ellipsoid);

lat = [lat_inv_circum lat_inv_e2e lat_inv_nziz];
lon = [lon_inv_circum lon_inv_e2e lon_inv_nziz];

projected_ellipsoid_points = [lat; lon].';


% figure;
% axesm('MapProjection','eqdazim', 'Geoid',[a e_2],'Origin',[latcentre_top, loncentre_top 0]);
% scatterm(lat, lon);
% for i = 1:1:length(projected_ellipsoid_points)
%      textm(projected_ellipsoid_points(i,1), projected_ellipsoid_points(i,2),string(i));
% end
% title('Predicted Positions - Azimuthal Equidistant Projection')
%% Predict 4 points
%%% F4 top right
left_pt = (projected_ellipsoid_points(16,:));
right_pt = (projected_ellipsoid_points(11,:));
up_pt = (projected_ellipsoid_points(12,:));
down_pt = (projected_ellipsoid_points(13,:));
all_matrix = [left_pt; right_pt; up_pt; down_pt];

[lat_ans, lon_ans, azi_ans, X, Y, Z] = geodesic_midpt(left_pt(1,1), left_pt(1,end), right_pt(1,1), right_pt(1,end), ellipsoid);
[lat_ans2, lon_ans2, azi_ans2, Xtwo, Ytwo, Ztwo] = geodesic_midpt(up_pt(1,1), up_pt(1,end), down_pt(1,1), down_pt(1,end), ellipsoid);

predicted1 = [X Y Z];
predicted2 = [Xtwo Ytwo Ztwo];

[lat_final, lon_final, azi_final, Xfinal_F4, Yfinal_F4, Zfinal_F4] = geodesic_midpt(lat_ans, lon_ans, lat_ans2, lon_ans2, ellipsoid);
FINAL_F4 = [Xfinal_F4, Yfinal_F4, Zfinal_F4];

%%% F3 top left
left_pt = (projected_ellipsoid_points(3,:));
right_pt = (projected_ellipsoid_points(16,:));
up_pt = (projected_ellipsoid_points(2,:));
down_pt = (projected_ellipsoid_points(15,:));
all_matrix = [left_pt; right_pt; up_pt; down_pt];

[lat_ans, lon_ans, azi_ans, X, Y, Z] = geodesic_midpt(left_pt(1,1), left_pt(1,end), right_pt(1,1), right_pt(1,end), ellipsoid);
[lat_ans2, lon_ans2, azi_ans2, Xtwo, Ytwo, Ztwo] = geodesic_midpt(up_pt(1,1), up_pt(1,end), down_pt(1,1), down_pt(1,end), ellipsoid);

predicted1 = [X Y Z];
predicted2 = [Xtwo Ytwo Ztwo];

[lat_final, lon_final, azi_final, Xfinal_F3, Yfinal_F3, Zfinal_F3] = geodesic_midpt(lat_ans, lon_ans, lat_ans2, lon_ans2, ellipsoid);
FINAL_F3 = [Xfinal_F3, Yfinal_F3, Zfinal_F3];

%%% P3 bottom LEFT
left_pt = (projected_ellipsoid_points(5,:));
right_pt = (projected_ellipsoid_points(17,:));
up_pt = (projected_ellipsoid_points(15,:));
down_pt = (projected_ellipsoid_points(6,:));
all_matrix = [left_pt; right_pt; up_pt; down_pt];

[lat_ans, lon_ans, azi_ans, X, Y, Z] = geodesic_midpt(left_pt(1,1), left_pt(1,end), right_pt(1,1), right_pt(1,end), ellipsoid);
[lat_ans2, lon_ans2, azi_ans2, Xtwo, Ytwo, Ztwo] = geodesic_midpt(up_pt(1,1), up_pt(1,end), down_pt(1,1), down_pt(1,end), ellipsoid);

predicted1 = [X Y Z];
predicted2 = [Xtwo Ytwo Ztwo];

[lat_final, lon_final, azi_final, Xfinal_P3, Yfinal_P3, Zfinal_P3] = geodesic_midpt(lat_ans, lon_ans, lat_ans2, lon_ans2, ellipsoid);
FINAL_P3 = [Xfinal_P3, Yfinal_P3, Zfinal_P3];

% %% P4 bottom right
left_pt = (projected_ellipsoid_points(17,:));
right_pt = (projected_ellipsoid_points(9,:));
up_pt = (projected_ellipsoid_points(13,:));
down_pt = (projected_ellipsoid_points(8,:));
all_matrix = [left_pt; right_pt; up_pt; down_pt];

% [left_lat, left_lon, h, M] = geocent_inv(left_pt(1), left_pt(2), ellipsoid);
% [right_lat, right_lon, h, M] = geocent_inv(right_pt(1), right_pt(2), ellipsoid);
% [up_lat, up_lon, h, M] = geocent_inv(up_pt(1), up_pt(2),  ellipsoid);
% [down_lat, down_lon, h, M] = geocent_inv(down_pt(1), down_pt(2), ellipsoid);

[lat_ans, lon_ans, azi_ans, X, Y, Z] = geodesic_midpt(left_pt(1,1), left_pt(1,end), right_pt(1,1), right_pt(1,end), ellipsoid);
[lat_ans2, lon_ans2, azi_ans2, Xtwo, Ytwo, Ztwo] = geodesic_midpt(up_pt(1,1), up_pt(1,end), down_pt(1,1), down_pt(1,end), ellipsoid);

predicted1 = [X Y Z];
predicted2 = [Xtwo Ytwo Ztwo];

[lat_final, lon_final, azi_final, Xfinal_P4, Yfinal_P4 Zfinal_P4] = geodesic_midpt(lat_ans, lon_ans, lat_ans2, lon_ans2, ellipsoid);
FINAL = [Xfinal_P4, Yfinal_P4 Zfinal_P4];


[X, Y, Z] = geocent_fwd(lat, lon,0,ellipsoid);

pred_x = [X Xfinal_F4 Xfinal_F3 Xfinal_P3 Xfinal_P4];
pred_y = [Y Yfinal_F4 Yfinal_F3 Yfinal_P3 Yfinal_P4];
pred_z = [Z Zfinal_F4 Zfinal_F3 Zfinal_P3 Zfinal_P4];

pred = [pred_x; pred_y; pred_z].';

final_x = pred(:,1) + center1(1);
final_y = pred(:,2) + center1(2);
final_z = pred(:,3) + center1(3);

predicted = [final_x, final_y, final_z];

plot3(final_x, final_y, final_z, '*')';
hold on;

%% Compare to Static
% 
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
% plot3(final_x, final_y, final_z, 'd');
% hold on
% scatter3(static_x,static_y,static_z,'r*');
% title('Static vs Predicted - Ellipsoid Fit')
% legend('Predicted','Static')
% %% Labelling Static and PRedicted Points
% final_points = [final_x final_y final_z];
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
% error = [Fpz_diff; Fp2_diff; F8_diff; T4_diff; T6_diff; O2_diff; Oz_diff; O1_diff; T5_diff; T3_diff; F7_diff; Fp1_diff; Fz_diff; ...
% Cz_diff; Pz_diff; C4_diff; C3_diff; F4_diff; F3_diff; P3_diff; P4_diff];
% 
% 
% elapsedtime= toc;
% disp(elapsedtime);

