import sys
from pathlib import Path
import traceback
from typing import Annotated, Literal
from datetime import datetime
import yaml
from pydantic import BaseModel
import typer

from img_proj.cli import project

app = typer.Typer(no_args_is_help=True)


class ProjectionGrid(BaseModel):
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    res: float
    z: float

class AppConfig(BaseModel):
    cam_id: int
    dir_imgs: Path
    georef_type: Literal["static", "dynamic"]
    f_cam_params_static: Path
    dir_cam_params_dynamic: Path
    start: datetime
    end: datetime
    pgrid: ProjectionGrid
    save_format: str
    outdir: Path



def load_config(path: str) -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)  # validation automatique

@app.command()
def main(
    input_yaml: Annotated[
        Path,
        typer.Argument(
            exists=True,
            dir_okay=True,
            help="Input yaml file containing parameters",
        ),
    ],
):
    # load configuration file
    conf = load_config(input_yaml)

    # check input parameters
    if not conf.dir_imgs.is_dir():
        raise typer.Exit("Directory of images to be projected does not exist")
    if conf.georef_type == 'dynamic':
        if not conf.dir_cam_params_dynamic.is_dir():
            raise typer.Exit("Directory of dynamic camera parameters does not exist")

    # create output directory
    conf.outdir.mkdir(parents=True, exist_ok=True)

    # project images
    print('project images')
    project.main(conf)


if __name__ == "__main__":
    app()
