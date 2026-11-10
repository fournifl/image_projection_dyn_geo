from pathlib import Path
from datetime import datetime
import numpy as np

from georef.operators import ProjectionGrid, Projector, Georef

from img_proj.core import img
from img_proj.core.cam_params import read_cam_params_dynamic

def run(dir_imgs: Path,
        georef_type: 'str',
        start:datetime,
        end:datetime,
        f_cam_params_static: Path,
        dir_cam_params_dynamic: Path,
        use_despiking: bool,
        f_despiking: Path,
        pgrid: ProjectionGrid,
        save_format: str,
        odir: Path):
    '''
    Project images in 'dir_imgs' using the projection grid 'pgrid' and either static or dynamic georef.
    '''


    # list images to be projected
    t_im, ls = img.ls_period(dir_imgs, start, end)

    # projection grid
    projection_grid = ProjectionGrid(pgrid.xmin, pgrid.xmax, pgrid.res, pgrid.ymin, pgrid.ymax, pgrid.res, pgrid.z)

    # save projection grid
    np.savez_compressed(odir / 'coords_projected_grid.npz', grid_x=projection_grid.xx, grid_y=projection_grid.yy)

    # read static or dynamic camera parameters
    if georef_type == 'static':
        gp = Georef.from_param_file(f_cam_params_static)
        # projector static
        projector_static = Projector(gp, projection_grid)
    else:
        t_cparams, georef_params, [undistort_map_x, undistort_map_y] = read_cam_params_dynamic(
            dir_cam_params_dynamic, use_despiking, f_despiking, start, end)

    # keep concomitant dates between images and camera parameters
    if georef_type == 'dynamic':
        common, idx_tim, idx_cparams = np.intersect1d(t_im, t_cparams, return_indices=True)
        ls = ls[idx_tim]
        georef_params = np.array(georef_params)[idx_cparams]

    # project images
    for i, f in enumerate(ls):

        # read im
        im = img.read_jpeg(f)

        # projector
        if georef_type == 'static':
            projector = projector_static

        elif georef_type == 'dynamic':
            gp = georef_params[i]
            gp._undistort_map_x = undistort_map_x
            gp._undistort_map_y = undistort_map_y
            projector = Projector(gp, projection_grid)

        # project image
        projector.project_image(im)

        # save to file
        f_png = odir / ('P_' + f.stem + save_format)
        projector.to_png(f_png)

    return


