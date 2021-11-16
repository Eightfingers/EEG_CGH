function closest_predicted_array = find_closest_from_predicted_to_wanded(predicted, input_array)
    
    % Assume the missing axis is all zeroes
    new_predicted = [predicted(:,1), predicted(:,2), zeros(length(predicted), 1)];
    
    for i = 1:1:length(predicted)
        % Compute the distance of each of the stylus data to each of the predicted
        % point
        v1 = repmat(predicted(i,:),size(input_array,1),1); 
        a = v1 - v2;
        b = pt - v2;
        d = sqrt(sum(cross(a,b,2).^2,2)) ./ sqrt(sum(a.^2,2));
            
        eculidian_distacnes = sqrt();
        closest_predicted = input_array(find(eculidian_distacnes==min(eculidian_distacnes)),:);
        closest_predicted_array = [closest_predicted_array; closest_predicted]; % append to the closest array
    end
end

