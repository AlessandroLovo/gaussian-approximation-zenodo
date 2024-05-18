# %%
# import stuff
import numpy as np
import sys
from pathlib import Path
import scipy.special as ss

# log to stdout
import logging
logging.getLogger().level = logging.INFO
logging.getLogger().handlers = [logging.StreamHandler(sys.stdout)]

sys.path.append('../../../Climate-Learning')

# print(sys.path)

import PLASIM.Learn2_new as ln
ut = ln.ut
ef = ln.ef
tf = ln.tf
keras = ln.keras

ut.indentation_sep = '  '

import general_purpose.cartopy_plots as cplt
import general_purpose.uplotlib as uplt

# %%
# define eta function and norm

def eta(x):
    return np.sqrt(2/np.pi)*np.exp(-x**2)/ss.erfc(x)

def l2(x):
    return np.sqrt(np.sum(x**2))

# %%
# set parameters
time_start = 31
time_end = 123

root_folder = 'ERA5/y83'
Path(root_folder).mkdir(exist_ok=True, parents=True)


Ts = [1,3,7,14,30]
taus = -np.arange(0,31)
percents = [50,25,10,5,3,2,1]

reshaper = None

# %%
# load the data
fields = ln.load_data(dataset_years=83, Model='ERA5', mylocal="../",
                      fields=['zg500'], area_integral_override={"zg500": "Data_ERA5/ANO_t2m_France.nc"},
                     )

t2m = fields['zg500'] # this is the geopotential field, but thanks to area_integral_override, it will contain the area integral of the temperature field
t2m.A = None # this way assign_labels will save A in the field

# save lon, lat
np.save(f'{root_folder}/lon.npy', t2m.field.lon.data)
np.save(f'{root_folder}/lat.npy', t2m.field.lat.data)

# %%
# loop

for T in Ts:
    logging.info(f'{T = }')
    folder = f'{root_folder}/T{T}'
    Path(folder).mkdir(exist_ok=True, parents=True)
    Y = ln.assign_labels(t2m, time_start=time_start, time_end=time_end, T=T)
    A = t2m.to_numpy(t2m.A)
    logging.debug(f'{A.shape = }')
    np.save(f'{folder}/A.npy', A)

    #flatten A
    A = A.reshape(-1)
    logging.debug(f'{A.shape = }')
    A_mean = np.mean(A)
    logging.debug(f'{A_mean = }')
    Sigma_AA = np.mean((A - A_mean)**2)
    np.save(f'{folder}/Sigma_AA.npy', Sigma_AA)
    
    for tau in taus:
    # for tau in range(0,T//2 + 1):
        logging.info(f'  {tau = }')
        subfolder = f'{folder}/tau{-tau}'
        Path(subfolder).mkdir(exist_ok=True, parents=True)

        # prepare the data
        X = ln.make_X(fields, time_start=time_start, time_end=time_end, T=T, tau=tau)
        logging.debug(f'{X.shape = }')

        # flatten time axis
        X = X.reshape((X.shape[0]*X.shape[1], *X.shape[2:]))
        logging.debug(f'{X.shape = }')

        # compute mean and std of X
        X_mean = np.mean(X, axis=0)
        X_std = np.std(X, axis=0)
        np.save(f'{subfolder}/X_mean.npy', X_mean)
        np.save(f'{subfolder}/X_std.npy', X_std)

        if reshaper is None:
            reshaper = ut.Reshaper(X_std != 0)

        # reshape X
        X = reshaper.reshape(X)
        X_mean = reshaper.reshape(X_mean)
        X_std = reshaper.reshape(X_std)
        logging.debug(f'{X.shape = }, {X_mean.shape = }, {X_std.shape = }')

        # normalize X
        X = (X - X_mean)/X_std

        # compute the correlation map
        Sigma_XA = np.mean(X.T*A, axis=1)
        logging.debug(f'{Sigma_XA.shape = }')
        np.save(f'{subfolder}/Sigma_XA.npy', reshaper.inv_reshape(Sigma_XA))

        # compute composites over the data
        for percent in percents:
            logging.info(f'    {percent = }')
            ssfolder = f'{subfolder}/percent{percent}'
            Path(ssfolder).mkdir(exist_ok=True, parents=True)

            Y, threshold = ln.ef.is_over_threshold(A, None, percent=percent)
            np.save(f'{ssfolder}/Y.npy', Y.reshape((t2m.years, -1)))
            np.save(f'{ssfolder}/threshold.npy', np.array([threshold]))

            X_heat = X[Y]
            X_comp = np.mean(X_heat, axis=0)
            X_comp_std = np.std(X_heat, axis=0)
            logging.debug(f'{X_comp.shape = }, {X_comp_std.shape = }')
            np.save(f'{ssfolder}/X_comp.npy', reshaper.inv_reshape(X_comp))
            np.save(f'{ssfolder}/X_comp_std.npy', reshaper.inv_reshape(X_comp_std))

            # compute gaussian composite
            X_comp_GA = Sigma_XA*eta(threshold/np.sqrt(2*Sigma_AA))/np.sqrt(Sigma_AA)
            logging.debug(f'{X_comp_GA.shape = }')
            np.save(f'{ssfolder}/X_comp_GA.npy', reshaper.inv_reshape(X_comp_GA))

            comp_error = X_comp_GA - X_comp

            norm_ratio = l2(comp_error)/l2(X_comp)
            logging.info(f'    {norm_ratio = }')
            np.save(f'{ssfolder}/norm_ratio.npy', np.array([norm_ratio]))
        
# %%
