load("predicted_2dmidpoint.mat");
return

load("predicted_conformal.mat");

plot3(predicted(:,1), predicted(:,2), predicted(:,3), "*");
hold on;
plot3(predicted_midpoint(:,1), predicted_midpoint(:,2), predicted_midpoint(:,3), "d");