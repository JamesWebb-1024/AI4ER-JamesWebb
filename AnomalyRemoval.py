import netCDF4
import numpy as np
import numpy.ma as ma

filename = 'Switzerland_01.nc'

data = netCDF4.Dataset(filename)
var = np.array(data['iop_apig'])


def maskarray(array):
    # Takes in an array, generates a mask so that any values of 0 are ignored.
    # By taking a large negative exponential of each element of the array, any 0 becomes a 1 and any nonzero becomes
    # a 0. Since values of 1 in the mask cause their corresponding value to be ignored, this means that only nonzero
    # values remain unmasked. We also take the absolute value of the array to avoid negative numbers ruining things.
    Mask = np.exp((-100000000 * (np.abs(np.array(array)))))
    return ma.masked_array(np.array(array), mask=Mask)


# This takes in an array and removes all values further than 4SD from the mean values. 0s are ignored when calculating
# mean and SD. The mask is removed before the array is returned.
def removeoutliers(array):
    counter = 0
    old_mean = 1000000
    old_std = 1000000
    while True:
        # Update mean and std
        array = maskarray(array)
        temp_mean = np.mean(array)
        temp_std = np.std(array)

        # Check to see if they've changed
        if old_mean == temp_mean and old_std == temp_std:
            break
        # print('Current boundary:' + str(temp_mean + 4 * temp_std) + str(temp_mean - 4 * temp_std))

        # Find the indexes of the outliers
        upperbound = np.where(array > (temp_mean + 4 * temp_std))
        lowerbound = np.where(array < (temp_mean - 4 * temp_std))

        # Loop over and set these outliers to 0
        for i in range(0, upperbound[1].shape[0]):
            counter += 1
            array[upperbound[0][i], upperbound[1][i]] = 0

        for i in range(0, lowerbound[1].shape[0]):
            counter += 1
            array[lowerbound[0][i], lowerbound[1][i]] = 0

        old_mean = temp_mean
        old_std = temp_std

    # print(str(counter) + 'outliers removed')
    return array.data

