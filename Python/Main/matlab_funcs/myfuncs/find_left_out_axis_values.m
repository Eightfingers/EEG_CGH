function axis_coordinate = find_left_out_axis_values(closest_predicted_array, input_array, target_dataset, ...
    queryaxis, axis1, axis2)
    
    axis_coordinate= [];
    
    for i = 1:1:length(closest_predicted_array) 
%         distances_circum_1 = sqrt(sum(bsxfun(@minus, input_array,closest_predicted_array(i,:) ).^2,2));
%         [~, ascendIdx] = sort(distances_circum_1);
%         ascendIdx(ascendIdx==closest_predicted_array(i,:)) = [];  %remove the pt point
%         disp(ANearest_circum);
        xq = closest_predicted_array(i,queryaxis); % z value
        
%         xq = closest_predicted_array(:,1);
        zq = interp1(target_dataset(:,axis1), target_dataset(:,axis2), xq, 'cubic');
% %         disp(zq);   
        axis_coordinate = [axis_coordinate; zq]; % append to the interpolate losest
    end
    disp("FUNCTION e");
end

% function axis_coordinate = find_left_out_axis_values(closest_predicted_array, input_array, target_dataset, ...
%     queryaxis, axis1, axis2)
% 
%     axis_coordinate= [];
% 
%     for i = 1:1:length(closest_predicted_array) 
%         distances_circum_1 = sqrt(sum(bsxfun(@minus, input_array,closest_predicted_array(i,:) ).^2,2));
%         n = 4; 
%         [~, ascendIdx] = sort(distances_circum_1); 
%         ascendIdx(ascendIdx==closest_predicted_array(i,:)) = [];  %remove the pt point
%         ANearest_circum = target_dataset(ascendIdx(1:n),:);  % 4 nearest points in 3D 
% 
%         xq = closest_predicted_array(i,queryaxis); % z value 
%         zq = interp1(ANearest_circum(:,axis1), ANearest_circum(:,axis2), xq, 'linear');
% 
%         axis_coordinate = [axis_coordinate; zq]; % append to the interpolate losest
%     end
% end

