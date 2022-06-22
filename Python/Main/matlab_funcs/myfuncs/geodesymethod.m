%% This script 

clear;
clc;

%% Add the data and helperfuncs folder path
addpath('helperfuncs');
addpath("data_16_06");
addpath('myfuncs');

static_markers = load_static('16_6_2021_Jack_Allstatic.csv');
static_markers(8,:) = []; % remove the extra orientation marker on the nose

X = static_markers(:,1);
Y = static_markers(:,2);
Z = static_markers(:,3);

%% Do an ellipsoid fit
[ center, radii, evecs, v, chi2 ] = ellipsoid_fit([X, Y, Z]);
fprintf( 'Ellipsoid center: %.5g %.5g %.5g\n', center );
fprintf( 'Ellipsoid radii: %.5g %.5g %.5g\n', radii );
fprintf( 'Ellipsoid evecs:\n' );
fprintf( '%.5g %.5g %.5g\n%.5g %.5g %.5g\n%.5g %.5g %.5g\n', ...
    evecs(1), evecs(2), evecs(3), evecs(4), evecs(5), evecs(6), evecs(7), evecs(8), evecs(9) );
fprintf( 'Algebraic form:\n' );
fprintf( '%.5g ', v );
fprintf( '\nAverage deviation of the fit:2 %.5f\n', sqrt( chi2 / size( X, 1 ) ) );
fprintf( '\n' );

%% Draw the ellipsoid fit
mind = min( [ X Y Z] );
maxd = max( [ X Y Z  ] );
nsteps = 60;
step = ( maxd - mind ) / nsteps;
[ x, y, z ] = meshgrid( linspace( mind(1) - step(1), maxd(1) + step(1), nsteps ), linspace( mind(2) - step(2), maxd(2) + step(2), nsteps ), linspace( mind(3) - step(3), maxd(3) + step(3), nsteps ) );
Ellipsoid = v(1) *x.*x +   v(2) * y.*y + v(3) * z.*z + ...
          2*v(4) *x.*y + 2*v(5)*x.*z + 2*v(6) * y.*z + ...
          2*v(7) *x    + 2*v(8)*y    + 2*v(9) * z;
x = x - center(1); % shift the center of ellipsoid to 0 0 0
y = y - center(2);
z = z - center(3);

X = X - center(1); % shift the static points to the center too
Y = Y - center(2);
Z = Z - center(3);
shifted_static_markers = [X, Y, Z]

%% Plot the shifted static points
plot3(X, Y, Z, '*');
hold on;
axis equal;
set(gca,'DataAspectRatio',[1 1 1])

%% Plot the ellipsoid fit
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

for i = 1:1:length(projected_ellipsoid_points)
    text(projected_ellipsoid_points(i,1), projected_ellipsoid_points(i,2), projected_ellipsoid_points(i,3),string(i));
end

%% From here onwards, we will be using geographic library 
% https://www.mathworks.com/matlabcentral/fileexchange/50605-geographiclib
% Check out ^ for more info about the parameters used. The library is quite
% big but read thru contents.m and geodoc for a good understanding

%% These are the ellipsoid parameters
% taken from
% https://www.mathworks.com/matlabcentral/fileexchange/50605-geographiclib
% under functions -> geodoc
%   The parameters of the ellipsoid are specified by the optional ellipsoid
%   argument to the routines.  This is a two-element vector of the form
%   [a,e], where a is the equatorial radius, e is the eccentricity e =
%   sqrt(a^2-b^2)/a, and b is the polar semi-axis.  Typically, a and b are
%   measured in meters and the linear and area quantities returned by the
%   routines are then in meters and meters^2.  However, other units can be
%   employed.  If ellipsoid is omitted, then the WGS84 ellipsoid (more
%   precisely, the value returned by defaultellipsoid) is assumed [6378137,
%   0.0818191908426215] corresponding to a = 6378137 meters and a
%   flattening f = (a-b)/a = 1/298.257223563.  The flattening and
%   eccentricity are related by
%
%   e = sqrt(f * (2 - f))
%   f = e^2 / (1 + sqrt(1 - e^2))

a = 0.098266; 
b = 0.081527;
e = (a^2-b^2)/a % This is the actual formula but...
% e = (1 - (a^2 - b) )^1/2 % I dont remember where i got this from, but
% using this the results seems to be closer to the static points.... 

% The ellipsoid is specified as [a, e], where a = equatorial radius
% and e = eccentricity.  The eccentricity can be pure imaginary to
% denote a prolate ellipsoid.
ellipsoid = [0.098266, e];

% %% F4 top right
% left_pt = (projected_ellipsoid_points(14,:));
% right_pt = (projected_ellipsoid_points(4,:));
% up_pt = (projected_ellipsoid_points(5,:));
% down_pt = (projected_ellipsoid_points(12,:));
% all_matrix = [left_pt; right_pt; up_pt; down_pt];
% F4 = [0.0557295970291955,0.0204980558445656,0.0584305644824410];

% %% F3 top left
% left_pt = (projected_ellipsoid_points(18,:));
% right_pt = (projected_ellipsoid_points(14,:));
% up_pt = (projected_ellipsoid_points(9,:));
% down_pt = (projected_ellipsoid_points(20,:));
% all_matrix = [left_pt; right_pt; up_pt; down_pt];
% F3 = shifted_static_markers(6,:);

% %% P3 bottom LEFT
% left_pt = (projected_ellipsoid_points(10,:));
% right_pt = (projected_ellipsoid_points(15,:));
% up_pt = (projected_ellipsoid_points(20,:));
% down_pt = (projected_ellipsoid_points(2,:));
% all_matrix = [left_pt; right_pt; up_pt; down_pt];
% P3 = [projected_ellipsoid_points(11,:)];

% %% P4 bottom right
% left_pt = (projected_ellipsoid_points(10,:));
% right_pt = (projected_ellipsoid_points(19,:));
% up_pt = (projected_ellipsoid_points(12,:));
% down_pt = (projected_ellipsoid_points(21,:));
% all_matrix = [left_pt; right_pt; up_pt; down_pt];
% P4 = projected_ellipsoid_points(3,:);

% express the 4 points in latitude longitude
[left_lat, left_lon, h, M] = geocent_inv(left_pt(1), left_pt(2), left_pt(3), ellipsoid);
[right_lat, right_lon, h, M] = geocent_inv(right_pt(1), right_pt(2), right_pt(3), ellipsoid);
[up_lat, up_lon, h, M] = geocent_inv(up_pt(1), up_pt(2), up_pt(3), ellipsoid);
[down_lat, down_lon, h, M] = geocent_inv(down_pt(1), down_pt(2), down_pt(3), ellipsoid);

%% find the geodesic midpoint between the 2 points
[lat_ans, lon_ans, azi_ans, X, Y, Z] = geodesic_midpt(left_lat, left_lon, right_lat, right_lon, ellipsoid);
[lat_ans2, lon_ans2, azi_ans2, Xtwo, Ytwo, Ztwo] = geodesic_midpt(up_lat, up_lon, down_lat, down_lon, ellipsoid);

predicted1 = [X Y Z];
predicted2 = [Xtwo Ytwo Ztwo];

%% Finally find the mid point between those 2
[lat_final, lon_final, azi_final, Xfinal, Yfinal, Zfinal] = geodesic_midpt(lat_ans, lon_ans, lat_ans2, lon_ans2, ellipsoid);
FINAL = [Xfinal, Yfinal, Zfinal];
% diff = FINAL - F4;
% disp(norm(diff))
plot3(Xfinal, Yfinal, Zfinal, 'd');
% 
