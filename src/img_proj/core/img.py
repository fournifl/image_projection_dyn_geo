from dateutil import parser

import numpy as np
import turbojpeg as tjpeg
jpeg = tjpeg.TurboJPEG()


def is_jpeg(buffer: bytes) -> bool:
    """Check if last two bytes of the file buffer are equal to b'\xff\xd9'"""
    return buffer[-2:] == b"\xff\xd9"

def get_date(fn):
    ymd = fn.stem.split('_')[-3]
    h = fn.stem.split('_')[-2]
    mn = fn.stem.split('_')[-1]
    date = f'{ymd[0:4]}-{ymd[4:6]}-{ymd[6:8]} {h}:{mn}'
    date = parser.parse(date)
    return date

def ls_period(dir, start, end, extension='*.jp*g'):
    ls = sorted(dir.glob(extension))
    t_im = [get_date(f) for f in ls]
    inds = [i for i, dt in enumerate(t_im) if start <= dt <= end]
    return np.array(t_im)[inds], np.array(ls)[inds]


def read_jpeg(fname, pixel_format=tjpeg.TJPF_BGR) -> np.ndarray:
    fname = fname
    with fname.open("rb") as fp:
        buffer = fp.read()

    if not is_jpeg(buffer=buffer):
        raise ValueError(f"JPEG File '{fname}' is corrupted")
    im = jpeg.decode(buffer, pixel_format)

    return im