import numpy as np
import xarray as xr

def daily_mean(da:xr.DataArray):
    return da.resample(time='1D').mean().assign_coords({'time': da.time.resample(time='1D').mean()})

def process(file_prefix, years, destination):
    ds = []
    for year in years:
        print(year)
        da = xr.open_dataarray(f'{file_prefix}{year}.nc')
        ds.append(daily_mean(da))
        
    ds = xr.concat(ds, 'time')

    ds.to_netcdf(destination)


if __name__ == '__main__':
    years = np.arange(1940,2023)
    # t2m
    print('--- t2m ---')
    process('raw/t2m/t2m_0N-90N_MJJA_', years, 't2m_MJJA_fullres.nc')

    # zg
    print('--- zg ---')
    process('raw/zg/zg500_0N-90N_MJJA_', years, 'zg_MJJA_fullres.nc')