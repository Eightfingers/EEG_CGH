function [lat_ans, lon_ans, azi_ans, X, Y, Z] = geodesic_midpt(lat_pt1, lon_pt1, lat_pt2, lon_pt2, ellipsoid)
   % This function takes 2 points on an ellipsoid surface defined by
   % geographiclib ellipsoid and return the mid point in terms of latittude
   % lotitude and azimuth angle, X, Y, Z
   
   % Find distance between the 2 points
   [s12, azi1, azi2] = geoddistance ...
      (lat_pt1, lon_pt1, lat_pt2, lon_pt2, ellipsoid)

   % From point 1 find the position that is halfway from point2
   [lat_ans, lon_ans, azi_ans] = geodreckon ...
       (lat_pt1, lon_pt1, s12/2, azi1, ellipsoid) % north south
   
   % Calculate XYZ form
   [X,Y,Z] = geocent_fwd(lat_ans, lon_ans, 0, ellipsoid);

end

