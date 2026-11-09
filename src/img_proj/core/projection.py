from pathlib import Path
from datetime import datetime

from georef.operators import ProjectionGrid, Projector, Georef

from img_proj.core import img
from img_proj.core.cam_params import read_cam_params_dynamic

def run(dir_imgs: Path, georef_type: 'str', start:datetime, end:datetime, f_cam_params_static: Path,
        dir_cam_params_dynamic: Path, pgrid: ProjectionGrid, save_format: str, odir: Path):
    '''
    Project images in 'dir_imgs' using the projection grid 'pgrid' and either static or dynamic georef.
    '''


    # list images to be projected
    ls = img.ls_period(dir_imgs, start, end)

    # projection grid
    projection_grid = ProjectionGrid(pgrid.xmin, pgrid.xmax, pgrid.res, pgrid.ymin, pgrid.ymax, pgrid.res, pgrid.z)

    # read static or dynamic camera parameters
    if georef_type == 'static':
        gp = Georef.from_param_file(f_cam_params_static)
    else:
        t_cparams, georef_params, [undistort_map_x, undistort_map_y] = read_cam_params_dynamic(
            dir_cam_params_dynamic, start, end)

    # projector static
    projector = Projector(gp, projection_grid)


    # project images
    for i, f in enumerate(ls):

        # read im
        im = img.read_jpeg(f)

        # projector
        if georef_type == 'dynamic':
            # gp = georef_params[i]
            # gp._undistort_map_x = undistort_map[0]
            # gp._undistort_map_y = undistort_map[1]
            # projector = Projector(gp, projection_grid)
            print('')

        # project image
        # im_proj = projector.project_image(im)
        # if return_imgs_proj:
        #     imgs_proj.append(im_proj.img_proj)

        # save to file
        f_png = odir / ('P_' + f.stem + save_format)
        # projector.to_png(f_png)








    return


