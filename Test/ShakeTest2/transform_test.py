from math import degrees
from scipy.spatial.transform import Rotation as R
import pandas as pd
import numpy as np

# In optitrack, the quaternion follows q=x*i+y*j+z*k+w; However, In matlab, the quaternion follows q=w+x*i+y*j+z*k
# in scipy its x y z w

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

df = pd.read_csv('spec_location.csv')
df2 = pd.read_csv('quaternion.csv')
df3 = pd.read_csv('specs_displacement.csv')
df4 = pd.read_csv('global_location.csv')

predicted_positions = df.loc[:,['x', 'y', 'z']].to_numpy()
# print("Predicted position")
# print(predicted_positions)
quaternion = df2.to_numpy()
specs_displacement = df3.loc[:,['x', 'y', 'z']].to_numpy()
correct_global_position = df4.loc[:,['x', 'y', 'z']].to_numpy() 

# print(predicted_positions.shape)
# print(quaternion.shape)
# print(specs_displacement.shape)
# print(quaternion)

global_positions = transform_spec_to_global_frame(predicted_positions, quaternion, specs_displacement)
# print(global_positions)
np.savetxt("python_transform.csv", global_positions,delimiter=',')
