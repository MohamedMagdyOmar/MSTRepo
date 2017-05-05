import netCDF4 as netcdf_helpers

dataset = netcdf_helpers.Dataset('testing.nc', 'r+')
dataset.variables['inputs'][:] =
x = 1