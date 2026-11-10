from img_proj.core import projection

def main(conf):

    projection.run(conf.dir_imgs,
                   conf.georef_type,
                   conf.start,
                   conf.end,
                   conf.f_cam_params_static,
                   conf.cam_params_dynamic.dir,
                   conf.cam_params_dynamic.use_despiking,
                   conf.cam_params_dynamic.f_despiking,
                   conf.pgrid,
                   conf.save_format,
                   conf.outdir
                  )