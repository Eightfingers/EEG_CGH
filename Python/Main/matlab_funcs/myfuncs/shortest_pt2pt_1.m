function [projected_surface_point] = shortest_pt2pt_1(from_points,target_points,loop_step)
% Takes in 2 array of points, from points and target points.
% Returns, in order of the from points, points on the target points that
% are closest to the from points via euclidian distance

shortest_length = 10; % random arbitary number
projected_surface_point = [];

for j = 1
    static_coord = from_points(j,:);  
    for j = 1:loop_step:length(target_points) %% Loop through all the vertices with loop_step step amount
        euclidian_dist = norm(target_points(j,:) - static_coord); %% Find the euclidian distance between them
        if euclidian_dist < shortest_length
            shortest_length = euclidian_dist;
            vertex = target_points(j,:);
        end
    end
    shortest_length = 10; % reset
    projected_surface_point = [projected_surface_point; vertex];
end

end

