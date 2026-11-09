from img_proj.core import projection

def main(conf):

    projection.run(conf.dir_imgs,
                   conf.georef_type,
                   conf.start,
                   conf.end,
                   conf.f_cam_params_static,
                   conf.dir_cam_params_dynamic,
                   conf.pgrid,
                   conf.save_format,
                   conf.outdir
                  )