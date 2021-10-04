function closest_predicted_array = find_closest_from_predicted_to_wanded(predicted, input_array)
    %UNTITLED Summary of this function goes here
    %   Detailed explanation goes here
    closest_predicted_array = [];
    for i = 1:1:length(predicted)
        eculidian_distacnes = sqrt(sum(bsxfun(@minus, input_array, predicted(:,i).').^2,2));
        closest_predicted = input_array(find(eculidian_distacnes==min(eculidian_distacnes)),:);
        closest_predicted_array = [closest_predicted_array; closest_predicted]; % append to the closest array
    end
end

