import cdsapi

c = cdsapi.Client()

## land sea mask
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': 'land_sea_mask',
        'year': '1979',
        'month': '01',
        'day': '01',
        'time': '00:00',
        'area': [
            90, -180, -90,
            180,
        ],
    },
    'raw/lsm.nc')