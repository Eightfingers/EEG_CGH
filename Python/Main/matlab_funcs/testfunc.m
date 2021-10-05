%%% This code would be the final code that is used to determine the 17 EEG
%%% locations. 
%% Add to path different folders containing data and code
%  addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept');
% addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\helperfuncs');
% addpath('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Code\MatlabSept\myfuncs');
% addpath ('C:\Users\Souganttika\OneDrive\Documents\MATLAB\Data\30_9_2021');

addpath('30_9_2021');
addpath('helperfuncs');
addpath('myfuncs');
%% Load the different wanded data
circumference = readmatrix('circum_shake_30_9_2023.csv');
ear2ear = readmatrix('ear2ear_shake_30_9_2024.csv');
nziz = readmatrix ('NZIZ_shake_30_9_2021.csv');
%% Run Function to give points
[predicted] = EEGpoints(circumference,ear2ear,nziz);