import numpy as np

array_1 = np.zeros((3,3)) # create 3 row and 3 column of 0 data
print(array_1)

split_numpy = [[-7.780206564624692,-4.6530515062161015,2.146812953367885,12.010116946558924,21.119039291946862],[33.050512877748204,-29.884857250910848,-90.12575028961946,-132.4126258060443,-141.56564718627573],[38.53238753156955,74.2785335686613,72.66872585040221,31.343370674894956,-28.110406259673592]]
split_numpy = np.array([split_numpy[0], split_numpy[1], split_numpy[2]])
split_numpy = np.transpose(split_numpy)
print(split_numpy)
split_numpy = np.array([split_numpy[:,0], split_numpy[:,2], split_numpy[:,1]])
print(split_numpy)

# # Insert array to the end of numpy
# np.append(array_1, tuple_1, axis = 0)

# print(array_1)