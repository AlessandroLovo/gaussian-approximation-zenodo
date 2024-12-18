# Code for the paper "Gaussian Framework and Optimal Projection of Weather Fields for Prediction of Extreme Events"

[![DOI](https://zenodo.org/badge/802543475.svg)](https://zenodo.org/doi/10.5281/zenodo.11400868)

[preprint](https://arxiv.org/abs/2405.20903)

## Data

Due to the very large size of the PlaSim dataset we used, we could not upload it, so we here provide directly the results of our analysis and the means to reproduce the figures of the paper.

For [ERA5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5) instead, the pipeline assumes you'll download the data and process it following the innstructions in this repository.

## Setup

To be able to run the notebooks in this repository, you need to clone the [Climate-Learning](https://github.com/georgemilosh/Climate-Learning) repository.

To do so, put yoursel in the same directory of this file and run

```bash
git clone --recursive https://github.com/georgemilosh/Climate-Learning.git
```

Most of the notebooks will use only the submodule [general_purpose](https://github.com/AlessandroLovo/general_purpose), but some need the full Climate-Learning framework

## Contents

- `gaus-approx/`
    - `PLASIM/` : analysis on PlaSim data
        - `composites/`
            - `composites.ipynb` : notebook for analyzing composite maps
            - `composite_map_T14_tau0_percent3_y8000-Z.npy` : composite map for geopotential at $p = 3%$ (used for figure 1)
            - `composite_maps_percent5_y8000.nc` : composite maps at different values of $T$ and $\tau$
            - `composite_maps_T1_percent5_y80-Z.nc` : composite maps at different values of $\tau$
            - `composite_maps_T14_tau0_y200-1000.nc` : composite maps at different values of $a$
            - `composite_maps_T14_tau0_y8000.nc` : composite maps at different values of $a$
            - `density_plot.nc` : time series to make the density plot
        - `committor/`
            - `committor.ipynb` : notebook for analyzing committor functions
            - `projection_patterns_T1_y80_epsilonbest_fold0-Z.nc` : projection patterns at different values of $\tau$
            - `projection_patterns_T14_tau0_y8000_fold4.nc` : projection patterns at different values of the regularization coefficient $\epsilon$
            - `projection_patterns_T14_y8000_epsilon1_fold0.nc` : projection patterns at different values of $\tau$
            - `Skill_percent5_y8000_epsilon1.nc` : skills of GA and CNN at different values of $T$ and $\tau$
            - `Skill_T14_tau0_percent5.nc` : skills of GA and CNN + condition number of $\Sigma_{XX}$ at different values of $\epsilon$ and number of years of training.
            - `Skill-CNN_T14_tau0_y8000.nc` : skill of CNN at different values of $a$
            - `Skill-GA_percent5_y80_epsilonbest-Z.nc` : skill of GA at different values of $T$ and $\tau$ (unsing only geopotential height as predictor)
            - `Skill-GA_percent5_y80_epsilonbest.nc` : skill of GA at different values of $T$ and $\tau$
            - `Skill-GA_T14_tau0_percent5_y8000_epsilon1-Z.nc` : skill of GA using only geopotential
            - `Skill-GA_T14_tau0_y8000.nc` : skill of GA at different values of $a$
            - `W.npz` : sparse matrix for computing the $H_2$ norm of projection patterns.
        - `comparison/`
            - `comparison.ipynb` : notebook to compare composite maps and optimal projection patterns
        - `mask.npy` : boolean mask that keeps soil moisture only over France
    - `ERA5/` : analysis on ERA5 reanalysis
        - `Data_ERA5/` : directory where to download the [ERA5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5) data
            - `README.md` : informations for data download
            - `preprocess.ipynb` : notebook for downloading and pre-processing the data. All instructions are in the notebook
            - `fetch_lsm.py` : script to retrieve the land-sea mask
            - `fetch_t2m.py` : script to retrieve the 2 m temperature field
            - `fetch_zg.py` : script to retrieve the 500 hPa geopotential field
            - `daily_mean.py` : script to compute daily means from the downloaded 3-hourly data.
        - `composites/` : analysis of composite maps
            - `composites-ERA5.ipynb` : notebook for analyzing composite maps, contains instructions.
            - `compute_composites_ERA5.py`: script to compute composite maps. Instructions in the previous notebook.
        - `committor/` : analysis of committor functions
            - `analysis.ipynb` : notebook to compute committor functions from the data. This is optional, as we provide the results as well.
            - `committor-ERA5.ipynb` : notebook for the analysis of the committor function
            - `spectral-decomposition.ipynb` : notebook for the EOF analysis of the optimal projection patterns
            - `projection_patterns_T1_epsilonbest_fold0.nc` : optimal projection patterns at different values of $\tau$
            - `Skill-CNN_T14_percent5.nc` : skills of the convolutional neural networks at different values of $\tau$
            - `Skill-comp_T14_percent5.nc` : skills of the composite map used as projection pattern at different values of $\tau$
            - `Skill-GA_percent5_epsilonbest.nc` : skills of the Gaussian committor at different values of $T$ and $\tau$
            - `W.npz` : sparse matrix to compute the $H_2$ norm
            - `config_T14_tau0_epsilon1.json` : config file for training the gaussian committor
        - `comparison/` : comparison of results of both composite maps and projection patterns from the committor function
            - `comparison-ERA5.ipynb` : notebook to compare composite maps and projection patterns
            - `composites_CESM.nc` : composite maps from CESM data. For the full dataset, check [Ragone and Bouchet 2021](https://onlinelibrary.wiley.com/doi/abs/10.1029/2020GL091197)
    - `cell_area.nc` : values of the area of each grid cell in the PlaSim grid (valid also for ERA5 since we regrid the data)
    - `land_sea_mask.nc` : land sea mask of the PlaSim grid (valid also for ERA5 since we regrid the data)
    - `lat.npy` : latitude values
    - `lon.npy` : longitude values


## Index by figure/table

In the following we show which notebook you need to run to reproduce any specific figure or table.

- Figure 1 : `ERA5/comparison/comparison-ERA5.ipynb`
- Figure 2 : `PLASIM/composites/composites.ipynb`
- Figure 3 : `PLASIM/composites/composites.ipynb`
- Figure 4 : `PLASIM/composites/composites.ipynb`
- Figure 5 : `PLASIM/committor/committor.ipynb`
- Figure 6 : `PLASIM/committor/committor.ipynb`
- Figure 7 : `PLASIM/comparison/comparison.ipynb`
- Figure 8 : `ERA5/composites/composites-ERA5.ipynb`
- Figure 9 : `ERA5/committor/committor-ERA5.ipynb`
- Figure 10 : `ERA5/committor/committor-ERA5.ipynb`
- Figure 11 : `ERA5/comparison/comparison-ERA5.ipynb`

- Table 1 : `PLASIM/committor/committor.ipynb`
- Table 2 : `PLASIM/composites/composites.ipynb`
- Table 3 : `PLASIM/composites/composites.ipynb`
- Table 4 : `PLASIM/committor/committor.ipynb`
- Table 5 : `ERA5/composites/composites-ERA5.ipynb`
- Table 6 : `PLASIM/committor/committor.ipynb`

- Figure S1 : `ERA5/Data_ERA5/preprocess.ipynb`
- Figure S2 : `ERA5/Data_ERA5/preprocess.ipynb`
- Figure S3 : `PLASIM/composites/composites.ipynb`
- Figure S4 : `PLASIM/composites/composites.ipynb`
- Figure S5 : `PLASIM/composites/composites.ipynb`
- Figure S6 : `ERA5/committor/spectral-decomposition.ipynb`
- Figure S7 : `ERA5/committor/spectral-decomposition.ipynb`
- Figure S8 : `PLASIM/committor/committor.ipynb`

- Table S1, S2, S3 : `PLASIM/composites/composites.ipynb`
- Table S4 : `ERA5/committor/committor-ERA5.ipynb`
