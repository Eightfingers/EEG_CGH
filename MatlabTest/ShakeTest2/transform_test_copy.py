from math import degrees
from scipy.spatial.transform import Rotation as R
import pandas as pd
import numpy as np

# In optitrack, the quaternion follows q=x*i+y*j+z*k+w; However, In matlab, the quaternion follows q=w+x*i+y*j+z*k
# in scipy its x y z w
# look into qt axis and rotation convention

def transform_spec_to_global_frame(series, specs_rotation, specs_position):
    print(specs_rotation)
    specs_rotation[:,[3,0]] = specs_rotation[:, [0, 3]] 
    #specs_rotation[:,[2,1]] = specs_rotation[:, [1, 2]] 
    r = R.from_quat(specs_rotation) # rotate the orientation

    # print(specs_rotation)
    # r_inv = r.inv()
    # r_euler = r.as_euler('xyz',degrees=True)
    #print("The SPECS rotation is ..", specs_rotation)
    # print("The Specs position is ..", specs_position)
    new_predicted_positions = r.apply(series)
    new_predicted_positions = new_predicted_positions + specs_position # now add the displaced amount
    # print("Main: The specs position is",specs_position)
    return new_predicted_positions

def transform_global_to_spec_frame(series, specs_rotation, specs_position):
    specs_rotation[:,[3,0]] = specs_rotation[:, [0, 3]]
    specs_rotation[:,[2,1]] = specs_rotation[:, [1, 2]]
    r = R.from_quat(specs_rotation) # rotate the orientation
    r_inver = r.inv()

    new_predicted_positions = r_inver.apply(series)
    new_predicted_positions = new_predicted_positions - specs_position 
    return new_predicted_positions

df1 = pd.read_csv('circum_shake_specs_displacement_matrix.csv')
df2 = pd.read_csv('circum_shaker_quaternion.csv')
df3 = pd.read_csv('circum_shake_untransformed_trace.csv')

specs_displacement = df1.to_numpy()
quaternion = df2.to_numpy()
circum_untransformed = df3.to_numpy()

specs_positions = transform_global_to_spec_frame(circum_untransformed, quaternion, specs_displacement)
np.savetxt("circum_shake_transform_python.csv", specs_positions, delimiter=',')
