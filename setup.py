from distutils.core import setup
from Cython.Build import cythonize

import numpy as np
setup(
    name="draw",
    ext_modules=cythonize("draw.pyx"),
    include_dirs=[np.get_include()]
)
