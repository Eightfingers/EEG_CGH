function resultant_matrix = construct_matrix_transform_xyz(displacement_vector, rotation_vector)

%     disp(rotation_vector);
    Xrot = rotation_vector(1);
    Yrot = rotation_vector(2);
    Zrot = rotation_vector(3);
    d = [displacement_vector(1); displacement_vector(2); displacement_vector(3)]; % displacement vector
    v = [ 0, 0 ,0 1];
    
    rot_matrix = rotx(Xrot) * roty(Yrot) * rotz(Zrot);
%     disp("Rot matrix is ");
%     disp(rot_matrix);
    resultant_matrix = [rot_matrix, d];
    resultant_matrix = [resultant_matrix ; v];

end