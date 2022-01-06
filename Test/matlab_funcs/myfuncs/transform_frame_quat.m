function [new_markers] = transform_frame_quat(stylus_data, quaternion_extracted_data, displacement_matrix)
%Transform the stylus data into the specs frame
    new_markers = [];   
    for i = 1:1:length(stylus_data)
    %     disp(i);
        quat_vector = quaternion(quaternion_extracted_data(i,:));
        RPY1 = eulerd(quat_vector,'XYZ', 'frame' );
        rot_vector = [-RPY1(1), -RPY1(2), -RPY1(3)];
        dis_vector = displacement_matrix(i,:);
        stylus_vector = [stylus_data(i,1); ... % X,Y,Z 
                  stylus_data(i,2); ...
                  stylus_data(i,3); ...
                   1];
        transform_matrix = construct_matrix_transform_xyz(dis_vector, rot_vector);    
        new_vector = inv(transform_matrix) * stylus_vector;
        new_markers = [new_markers; new_vector.';];

    end
end

