from libc.stdint cimport uint8_t

import numpy as np
cimport numpy as np

cpdef np.ndarray[uint8_t, ndim=3] test_def(np.ndarray[uint8_t, ndim=2] draw_img):
    # cdef np.ndarray[long, ndim=3] draw_back = draw_img
    print type(draw_img)
    print draw_img

    return draw_img
    # return draw_back