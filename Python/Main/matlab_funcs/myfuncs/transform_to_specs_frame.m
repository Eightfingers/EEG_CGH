%% Kinda confusing, bring out pen and paper to be more clear
function [new_markers] = transform_to_specs_frame(stylus_data, quaternion_extracted_data, displacement_matrix)
    new_markers = [];
    indx_to_remove = [];
    prev_data = [0,0,0];
    threshold = 0.05; % 5cm
    % Take the martrix with the smallest length
    array_length = min([length(stylus_data), length(quaternion_extracted_data), length(displacement_matrix)]);

    %% Take care of displacement first
    for i = 1:1:array_length
        if i == 1
            new_vector = stylus_data(i,:) - displacement_matrix(i,:);
        elseif i == 2
            prev_data = new_markers;
            new_vector = stylus_data(i,:) - displacement_matrix(i,:);
            if norm(new_vector - prev_data) > threshold
                indx_to_remove = [indx_to_remove; i];
            end
        else
            prev_data = new_markers(i-1,:);
%             change_in_displacement = 
            new_vector = stylus_data(i,:) - displacement_matrix(i,:);
            if norm(new_vector - prev_data) > threshold
                indx_to_remove = [indx_to_remove; i];
            end
        end
        new_markers = [new_markers; new_vector;];
    end
    new_markers(indx_to_remove,:) = []; % remove those outliers

    %% Take care of quaternion next
    quaternion_extracted_data(indx_to_remove,:) = [];
    Q2 = quaternion_extracted_data;
    Q1 = quaternion_extracted_data(1,:);
%     Q12 = quaternion from BODY1->BODY2
%     Q12 = conj(Q1) .* Q2;  % <- quaternion conjugate and quaternion multiply
    
    inv_quaternion = quatinv(Q2);
    new_markers = quatrotate(inv_quaternion, new_markers); % rotate them to original position

end
