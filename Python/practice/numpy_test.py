import numpy as np


deleted_data = np.array([])
data_set = np.array([[0.05,0.05,0.05], [0.09,0.09,0.09], [0.01,0.01,0.01]])
threshold = 0.01
sample_data = np.array([[0.049,0.049,0.045]])

# Check if the optitrack markers are near any electrode positions
# If they are change their colour to green and remove the position of that electrode from the series
# Remove the position of that electrode from the series.

for sample in sample_data:
    for data in data_set:
        magnitude_difference = np.absolute(np.linalg.norm(sample-data))
        print(magnitude_difference)
        if magnitude_difference < threshold:
            print("The sample ", sample, " is in the threshold range of the data set")
            # Remove this data set accordingly
            index = np.where(data_set == data) 
            print
            data_set = np.delete(data_set, index)
            deleted_data = np.append(deleted_data, np.array(data))

print("The dataset now is ", data_set)
print("The deleted data are ", deleted_data)