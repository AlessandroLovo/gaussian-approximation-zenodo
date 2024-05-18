import numpy as np
import os
from pathlib import Path

import cdsapi

c = cdsapi.Client()


def retrieve(year, path='.', overwrite=False):
    folder = Path(path)
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    
    filename = f'{path}/zg500_25N-90N_MJJA_{year}.nc'
    
    if os.path.exists(filename):
        if not overwrite:
            print(f'{filename} already exists: skipping')
            return
        print(f'Overwriting {filename}')

    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': 'geopotential',
            'pressure_level': '500',
            'year': f'{year}',
            'month': [
                '05', '06', '07',
                '08',
            ],
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'time': [
                '00:00', '03:00', '06:00',
                '09:00', '12:00', '15:00',
                '18:00', '21:00',
            ],
            'area': [
                90, -180, 25,
                180,
            ],
        },
        filename)
    
if __name__ == '__main__':
    years = np.arange(1940,2023)

    for year in years:
        retrieve(year, path='raw/zg')