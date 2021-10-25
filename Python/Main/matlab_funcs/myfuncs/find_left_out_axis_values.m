function axis_coordinate = find_left_out_axis_values(closest_predicted_array, target_dataset, ...
    queryaxis, axis1, axis2)
    
    axis_coordinate= [];
    
    for i = 1:1:length(closest_predicted_array) 
        xq = closest_predicted_array(i,1); 
        zq = interp1(target_dataset(:,axis1), target_dataset(:,queryaxis), xq, 'spline');
        axis_coordinate = [axis_coordinate; zq]; % append to the interpolate losest
    end
end