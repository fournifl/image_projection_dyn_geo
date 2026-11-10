import numpy as np
import pandas as pd

from georef.operators import Georef

from img_proj.core.img import get_date



def read_cam_params_dynamic(dir_cparams, use_despiking, f_despiking, start=None, end=None):

    # initialize georef_params and date
    georef_params = []
    t_cparams = []

    # list of json camera parameters
    ls_cparams_all = sorted(dir_cparams.glob('*.json'))

    # filter list of camera parameters
    mask_filter = []
    for f in ls_cparams_all:
        date = get_date(f)
        t_cparams.append(date)
        if (start is None) and (end is None):
            mask_filter.append(True)
        else:
            if (date >= start) and (date <= end):
                mask_filter.append(True)
            else:
                mask_filter.append(False)
    ls_cparams = np.array(ls_cparams_all)[mask_filter]
    t_cparams = np.array(t_cparams)[mask_filter]

    # read camera parameters
    for f in ls_cparams:
        gp = Georef.from_param_file(f)
        georef_params.append(gp)

        # make gp light by removing distorsion map
        gp._undistort_map_x = None
        gp._undistort_map_y = None

    # use despiking of camera parameters if used camera parameters are raw (not smooth)
    if use_despiking:
        t_cparams, georef_params = apply_despiking(f_despiking, t_cparams, georef_params)


    # get distorsion maps only once as it does not change
    gp = Georef.from_param_file(f)
    undistort_map_x = gp._undistort_map_x
    undistort_map_y = gp._undistort_map_y


    return t_cparams, georef_params, [undistort_map_x, undistort_map_y]


def apply_despiking(f_despiking, t_cparams, georef_params):
    df = pd.read_csv(f_despiking, parse_dates=["raw_cparam_date"])
    df = df[df["raw_cparam_date"].isin(t_cparams)]
    valid = df['valid']
    t_cparams = t_cparams[valid]
    georef_params = np.array(georef_params)[valid]

    return t_cparams, georef_params