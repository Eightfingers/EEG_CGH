# Configs 

class AppConfigs():
    mode_idle = "Idle"
    mode_show_trace = "Trace"
    mode_show_NZIZ = "NZIZ"
    mode_show_21 = "Predicted"
    mode_attach_electrode = "Electrode"

    # tightly couple with matlab code ..    
    error_idx0_dct = {[0]:"Error in estimating trace as an ellipse"}
    error_idx1_dct = {[1]:"Error in smoothing the ear2ear trace as a spline!"}
    error_idx2_dct = {[2]:"Error in fixing the ear2ear data set!"}
    error_idx3_dct = {[3]:"Error in circum interparc!"}
    error_idx4_dct = {[4]:"Error in ear2ear interparc!"}
    error_idx5_dct = {[5]:"Error in NZIZ interparc!"}
    error_idx6_dct = {[6]:"Error in finding shortest euclidian distance for circumference!"}
    error_idx7_dct = {[7]:"Error in finding shortest euclidian distance for ear2ear"}
    error_idx8_dct = {[8]:"Error in finding shortest euclidian distance for NZIZ"}
    error_idx9_dct = {[9]:"Error in finding shortest left axis value for circumference"}
    error_idx10_dct = {[10]:"Error in finding shortest left axis value for ear to ear"}
    error_idx11_dct = {[11]:"Error in finding shortest left axis value for NZIZ"}
