%%% This code would be the final code that is used to determine the 17 EEG
%%% locations. 
%% Add to path different folders containing data and code
addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept');
addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\helperfuncs');
addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\myfuncs');
% addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Data\16_7_2021');
addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\helperfuncs');
addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\helperfuncs\GeodeticToolbox')
addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\helperfuncs\New folder\geodetic')
%% Static Coordinates Extratcted
%%% Circumference
staticcircum = charliecircum003;
static_circum = [];
j = 1;
k = j +2 ;
while k <= length(staticcircum)
    static_circum(end+1, :) = [staticcircum(j:k)];
    j = j + 3;
    k = j + 2;
end 
static_circum_x = static_circum(:,1);
static_circum_y = static_circum(:,2);
static_circum_z = static_circum(:,3);
%%% Ear to Ear
statice2e = charlieear2ear004;
static_e2e = [];
j = 1;
k = j +2 ;
while k <= length(statice2e)
    static_e2e(end+1, :) = [statice2e(j:k)];
    j = j + 3;
    k = j + 2;
end 
static_e2e_x = static_e2e(:,1);
static_e2e_y = static_e2e(:,2);
static_e2e_z = static_e2e(:,3);
%%% Nasion to Inion
staticnziz = charlienziz002;
static_nziz = [];
j = 1;
k = j +2 ;
while k <= length(staticnziz)
    static_nziz(end+1, :) = [staticnziz(j:k)];
    j = j + 3;
    k = j + 2;
end 
static_nziz_x = static_nziz(:,1);
static_nziz_y = static_nziz(:,2);
static_nziz_z = static_nziz(:,3);

figure
hold on
scatter3(static_circum_x,static_circum_y,static_circum_z);
hold on
scatter3(static_e2e_x,static_e2e_y,static_e2e_z);
hold on
scatter3(static_nziz_x,static_nziz_y,static_nziz_z);
legend('Circumference','Ear to Ear','Nasion to Inion');
title('Static Points - Taken');
%% Ellipsoid Fitting
collated_data = [static_circum; static_e2e; static_nziz];
X_circum = collated_data(:,1);
Y_circum = collated_data(:,2);
Z_circum = collated_data(:,3);
% CART = [x,y,z];
[center, radii, evecs, v, chi2 ] = ellipsoid_fit_new( [X_circum Y_circum Z_circum],'');
fprintf( 'Ellipsoid center: %.5g %.5g %.5g\n', center );
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
x = x - center(1); % shift the center of ellipsoid to 0 0 0
y = y - center(2);
z = z - center(3);

X_circum = X_circum - center(1); % shift the static points to the center too
Y_circum = Y_circum - center(2);
Z_circum = Z_circum - center(3);
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
alpha(0.3);
axis equal;
camlight;
%% Project the static points to the 3D ellipsoid and plot them 
loop_step = 2;
points = surface.vertices;
projected_ellipsoid_points = shortest_pt2pt(shifted_static_markers, points,loop_step); % find the nearest point that lies on the ellipsoid from the static points
plot3(projected_ellipsoid_points(:,1),projected_ellipsoid_points(:,2),projected_ellipsoid_points(:,3),'d');

% for i = 1:1:length(projected_ellipsoid_points)
%     text(projected_ellipsoid_points(i,1), projected_ellipsoid_points(i,2), projected_ellipsoid_points(i,3),string(i));
% end

a = radii(1) ;
b = radii(2);
c = radii(3);
e = sqrt(a^2- b^2)/a;
e_2 = (1 - (a^2 - b) )^1/2;
% e_squ = e*e;
ellipsoid = [a, e_2];
%% Extract Projected points to x,y,z
proj_x = projected_ellipsoid_points(:,1);
proj_y = projected_ellipsoid_points(:,2);
proj_z = projected_ellipsoid_points(:,3);
%% Convert geocentric points to Geographic Coordinates
%%% Geocentric to Geographic 
[latpoints, lonpoints, h, ~] = geocent_inv(proj_x,proj_y,proj_z, ellipsoid);
%% Find Centre at the top of the head
length_of_circum = length(static_circum);
length_of_e2e = length(static_e2e);
length_of_nziz = length(static_nziz);
projpoints_circum = projected_ellipsoid_points(1:length_of_circum,:);
projpoints_e2e = projected_ellipsoid_points(length_of_circum +1:(length_of_circum + length_of_e2e) ,:);
projpoints_nziz = projected_ellipsoid_points((length_of_circum + length_of_e2e)+1:end , :);
% max_val_e2e = projpoints_e2e(4,:);
% max_val_nziz = projpoints_nziz(4,:);
% centre_top = (max_val_e2e(:)+max_val_nziz(:)).'/2;
% center_x= centre_top(1);
% center_y= centre_top(2);
% center_z= centre_top(3);
[latcentre_top, loncentre_top, hcentre_top, ~] = geocent_inv(0,c,0,ellipsoid);
% figure;
% scatter3(projpoints_e2e(:,1),projpoints_e2e(:,2),projpoints_e2e(:,end));
% hold on
% scatter3(projpoints_nziz(:,1),projpoints_nziz(:,2),projpoints_nziz(:,end));
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

figure;
hold on
scatter(x_new_top_circum,y_new_top_circum,'bd');
legend('Centre based projection', 'Top based projection');
title('Azimuthal Equidistant - Circumference');

%%% Ear to Ear
[x_new_top_e2e, y_new_top_e2e, azi, rk] = eqdazim_fwd(latcentre_top,loncentre_top, latpoints_e2e, lonpoints_e2e, ellipsoid);

figure;
scatter(x_new_top_e2e,y_new_top_e2e,'bd');
legend('Centre based projection', 'Top based projection');
title('Azimuthal Equidistant - Ear to Ear');

%%% Nasion to Inion
[x_new_top_nziz, y_new_top_nziz, azi, rk] = eqdazim_fwd(latcentre_top,loncentre_top, latpoints_nziz, lonpoints_nziz, ellipsoid);

figure;
hold on
scatter(x_new_top_nziz,y_new_top_nziz,'bd');
legend('Centre based projection', 'Top based projection');
title('Azimuthal Equidistant - Nasion to Inion');
%% 2D Geometerical Fitting
%%% Circumference
f1= figure('Name',' Circumference');
Ellipse=([x_new_top_circum, y_new_top_circum]);
[centre, a, b, alpha] = fitellipse(Ellipse,'linear');

plotellipse(centre, a, b, alpha, 'b-');
f1 = gcf; %current figure handle
axesObjs = get(f1, 'Children');  %axes handles
dataObjs = get(axesObjs, 'Children'); %handles t
xdata_circum = get(dataObjs, 'XData'); 
ydata_circum = get(dataObjs, 'YData');
start_A = [x_new_top_circum, y_new_top_circum];

startpoint_2d_circum = [start_A(5,1) start_A(5,end)];
newmat_xy = [xdata_circum; ydata_circum];
trans_newmat_xy = newmat_xy.';
dist_startpoint_circum = sqrt(sum(bsxfun(@minus, trans_newmat_xy, startpoint_2d_circum).^2,2));
closest_startpoint_circum = trans_newmat_xy(find(dist_startpoint_circum==min(dist_startpoint_circum)),:);
[row_circum,~] = find(trans_newmat_xy==closest_startpoint_circum);
new_matrix_x_circum = [trans_newmat_xy(row_circum:2000,1); trans_newmat_xy(1:row_circum-1,1)].';
new_matrix_y_circum = [trans_newmat_xy(row_circum:2000,2); trans_newmat_xy(1:row_circum-1,2)].';

%%% Ear to Ear - The ear to ear tracking data is considered as a spline in
%%% 2D space. The data points are orthogonally projected on the 2D XY plane
%%% and smoothing spline fitting is performed. The smoothing spline with is
%%% from the MATLAB curve fitting toolbox. Createfit2() is used here. The
%%% smoothing parameter used here is 0.999999481874551. 

% Spline fit & extracting out the numerical X, Z data. 
spline_e2e = splinetest_e2e(x_new_top_e2e, y_new_top_e2e);
points = fnplt(spline_e2e);
xdata_e2e = points(1,:);
ydata_e2e = points(2,:);
%% The least square fit of the plot has excess length that exceed the starting 
%% and ending position of the e2e dataset. Uncomment the code below to see it.
% fnplt(spline_e2e);
% hold on;
% plot(e2e_x, e2e_z, 'o');

%% We fix this by finding the point on the fitted line that is closest to the actual e2e dataset.
%% And making the fitted line start and end nearest to the e2e starting and ending dataset.
% Get the starting and ending position of e2e dataset
start_B = [x_new_top_e2e, y_new_top_e2e];
startpoint_2d_e2e = [start_B(1,1) start_B(1,end)];
endpoint_2d_e2e = [start_B(end,1) start_B(end,end)];

newmat_xy = [xdata_e2e; ydata_e2e];
trans_newmat_xy = newmat_xy.';

dist_startpoint_e2e = sqrt(sum(bsxfun(@minus, trans_newmat_xy, startpoint_2d_e2e).^2,2));
closest_startpoint_e2e = trans_newmat_xy(find(dist_startpoint_e2e==min(dist_startpoint_e2e)),:);

dist_endpoint_e2e = sqrt(sum(bsxfun(@minus, trans_newmat_xy, endpoint_2d_e2e).^2,2));
closest_endpoint_e2e = trans_newmat_xy(find(dist_endpoint_e2e==min(dist_endpoint_e2e)),:);

[row_startpoint_e2e,~] = find(trans_newmat_xy(:,1)==closest_startpoint_e2e(:,1));
[row_endpoint_e2e,~] = find(trans_newmat_xy(:,1)==closest_endpoint_e2e(:,1));

new_matrix_x_e2e = (trans_newmat_xy(row_startpoint_e2e:row_endpoint_e2e,1)).';
new_matrix_y_e2e = (trans_newmat_xy(row_startpoint_e2e:row_endpoint_e2e,2)).';

%%% Nasion to Inion
nziz_dataset = [x_new_top_nziz, y_new_top_nziz];
size_of_nziz = size(nziz_dataset);
lengthof_nziz = size_of_nziz(:,1);
split_nziz =  lengthof_nziz/2;
split_nziz_round = round(split_nziz);

x_split_back = x_new_top_nziz(split_nziz_round+1 :lengthof_nziz);
y_split_back = y_new_top_nziz(split_nziz_round+1 :lengthof_nziz);
nziz_back = spline_nziz_back(x_split_back,y_split_back);

points = fnplt(nziz_back,'-',2);
xdata_nziz_back = points(1,:);
ydata_nziz_back = points(2,:);

x_split_front = x_new_top_nziz(1 :split_nziz_round );
y_split_front = y_new_top_nziz(1 :split_nziz_round );
nziz_front = spline_nziz_front(y_split_front,x_split_front);

points = fnplt(nziz_front,'-',2);
ydata_nziz_front = points(1,:);
xdata_nziz_front = points(2,:);

%% Combine them back togather
ydata_nziz = [ydata_nziz_back ydata_nziz_front];
xdata_nziz = [xdata_nziz_back xdata_nziz_front];
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
%%% Nasion to Inion
[pt20_nziz,~,~] = interparc(0,xdata_nziz,ydata_nziz,'spline');
[pt21_nziz,~,~] = interparc(0.1,xdata_nziz,ydata_nziz,'spline');
[pt22_nziz,~,~] = interparc(0.30,xdata_nziz,ydata_nziz,'spline');
[pt23_nziz,~,~] = interparc(0.50,xdata_nziz,ydata_nziz,'spline');
[pt24_nziz,~,~] = interparc(0.70,xdata_nziz,ydata_nziz,'spline');
[pt25_nziz,~,~] = interparc(0.90,xdata_nziz,ydata_nziz,'spline');
[pt26_nziz,~,~] = interparc(1,xdata_nziz,ydata_nziz,'spline');
%% Collate Predicted Data Points
%%% Circuference
circum = [pt_circum.' pt1_circum.' pt2_circum.' pt3_circum.' pt4_circum.' pt5_circum.' pt6_circum.' pt7_circum.' pt8_circum.' pt9_circum.' pt10_circum.' pt11_circum.' ];
circum_x = circum(1,:);
circum_y = circum(end,:);
%%% Ear to Ear
e2e = [pt14_e2e.' pt15_e2e.' pt16_e2e.' pt17_e2e.' pt18_e2e.'];
e2e_x = e2e(1,:);
e2e_y = e2e(end,:);
%%% Nasion to Inion
nziz = [pt25_nziz.' pt24_nziz.' pt23_nziz.' pt22_nziz.' pt21_nziz.'];
nziz_x = nziz(1,:);
nziz_y = nziz(end,:);

figure;
hold on
scatter(circum(1,:),circum(end,:));
% hold on
% scatter(e2e(1,:),e2e(end,:));
hold on
scatter(nziz(1,:),nziz(end,:));
%% Inverse Projection to Lat and Lon
%%% Circumference
[lat_inv_circum, lon_inv_circum, azi, rk] = eqdazim_inv(latcentre_top, loncentre_top, circum_x, circum_y, ellipsoid);
%%% Ear to Ear
[lat_inv_e2e, lon_inv_e2e, azi, rk] = eqdazim_inv(latcentre_top, loncentre_top, e2e_x, e2e_y, ellipsoid);
%%% Naion to Inion
[lat_inv_nziz, lon_inv_nziz, azi, rk] = eqdazim_inv(latcentre_top, loncentre_top, nziz_x, nziz_y, ellipsoid);

figure;
axesm('MapProjection','eqdazim', 'Geoid',[a e_2],'Origin',[latcentre_top, loncentre_top 0]);
scatterm(lat_inv_circum, lon_inv_circum);
% hold on
% scatterm(lat_inv_e2e, lon_inv_e2e);
hold on
scatterm(lat_inv_nziz, lon_inv_nziz);
title('Predicted Positions - Azimuthal Equidistant Projection')

%% Inverse to geocentric coordinates
[X_circum, Y_circum, Z_circum] = geocent_fwd(lat_inv_circum, lon_inv_circum,0,ellipsoid);
% [X_e2e, Y_e2e, Z_e2e] = geocent_fwd(lat_inv_e2e, lon_inv_e2e,0,ellipsoid);
[X_nziz, Y_nziz, Z_nziz] = geocent_fwd(lat_inv_nziz, lon_inv_nziz,0,ellipsoid);

%% Compare to static
static_circum_x = static_circum(:,1)- center(1);
static_circum_y = static_circum(:,2)- center(2);
static_circum_z = static_circum(:,3)- center(3);

static_e2e_x = static_e2e(:,1)- center(1);
static_e2e_y = static_e2e(:,2)- center(2);
static_e2e_z = static_e2e(:,3)- center(3);

static_nziz_x = static_nziz(:,1)- center(1);
static_nziz_y = static_nziz(:,2)- center(2);
static_nziz_z = static_nziz(:,3)- center(3);

figure;
scatter3(X_circum,Y_circum,Z_circum);
% hold on 
% scatter3(X_e2e,Y_e2e,Z_e2e);
hold on
scatter3(X_nziz,Y_nziz,Z_nziz);
hold on
scatter3(static_circum_x,static_circum_y,static_circum_z);
hold on
scatter3(static_e2e_x,static_e2e_y,static_e2e_z);
hold on
scatter3(static_nziz_x,static_nziz_y,static_nziz_z);
legend('Cirumference-Predicted', 'E2E - Predicted','NzIz -Predicted','Circumference-Static','E2E - Static','NzIz-Static');
title('Predicted Positions vs Static Positions (Arbitary Ellipsoid)')