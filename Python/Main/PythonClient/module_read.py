from inspect import getmembers, isfunction

from NatNetClient import NatNetClient
# print(getmembers(NatNetClient, isfunction))

functions_list = [o for o in getmembers(NatNetClient) if isfunction(o[1])]
print(functions_list)