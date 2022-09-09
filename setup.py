from distutils.core import setup
from Cython.Build import cythonize

import numpy as np
setup(
    name="draw",
    ext_modules=cythonize(
        "draw.pyx",
        # compiler_directives={
        #     "cdivision": True,
        #     "embedsignature": True,
        #     "boundscheck": False,
        #     "wraparound": False
        # }
    ),
    include_dirs=[np.get_include()]
)
