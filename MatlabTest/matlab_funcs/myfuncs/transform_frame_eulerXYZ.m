function [new_markers] = transform_frame_eulerXYZ(stylus_data, rot_vector_matrix, displacement_matrix)
%Transform the stylus data into the specs frame
    new_markers = [];   
    for i = 1:1:length(stylus_data)
        disp(i);
        rot_vector = [-rot_vector_matrix(i,1), -rot_vector_matrix(i,2), -rot_vector_matrix(i,3)];
    %     rot_vector = [-z_rot(i), -y_rot(i), -x_rot(i)];

        dis_vector = displacement_matrix(i,:);
        transform_matrix = construct_matrix_transform_xyz(dis_vector, rot_vector);    

        wand_vector = [stylus_data(i,1); ... % X,Y,Z 
                  stylus_data(i,2); ...
                  stylus_data(i,3); ...
                   1];

        new_vector = inv(transform_matrix) * wand_vector;
        new_markers = [new_markers; new_vector.';];
    end
end

