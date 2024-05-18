# Preparing ERA5 reanalysis data

## Downoload

To download the data, run the scripts `fetch_*`. To be able to do so, you need a python evironment with `numpy` and the `cdsapi` package.
To install the latter, see the documentation [here](https://cds.climate.copernicus.eu/api-how-to).

The scripts will download data of 500 hPa geopotential height and 2 meter temperature for each year with 3h resolution.

## Compute daily means

To compute daily meeans run the script `compute_daily_means.py`. To be able to do so, you need a python evironment with `numpy` and `xarray` packages.

## Preprocess

Follow the steps in the `preprocess.ipynb` notebook.

Preprocessing includes:
- Computing area integral over France for the temperature field
- Regridding the geopotential field onto the PlaSim grid
- Detrending to remove climate change signal