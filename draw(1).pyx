# cython: language_level=3
# cython: cdivision=True
import cython
from libc.stdint cimport uint8_t

import random
import numpy as np
cimport numpy as np


np.import_array()

ctypedef np.uint8_t dtype_t

cdef void draw(uint8_t[:,:,::1] back_img, uint8_t[:,:,::1] draw_img, int y, int x):
    cdef int x2 = x+<int>draw_img.shape[1]
    cdef int y2 = y+<int>draw_img.shape[0]
    cdef uint8_t[:,:] back_draw = back_img[y:y2, x:x2][:,:,0]
    cdef np.ndarray[dtype_t, ndim=3] back_draw_ed = np.clip(np.where(draw_img<back_img, draw_img, back_img), 0, 255)
    back_img[y:y2, x:x2][:,:,0] = back_draw_ed

@cython.cdivision(True)
cdef inline int div_ceil(int a, int b):
    if not a%b:
        return a/b
    else:
        return a/b+1




cpdef np.ndarray[dtype_t, ndim=3] draw_all(uint8_t[:,:,::1]  draw_img, int back_shape_x, int back_shape_y, int rand_x, int rand_y , int space_x, int space_y):
    cdef int draw_img_x_max = <int>draw_img.shape[0] + space_x
    cdef int draw_img_y_max = <int> draw_img.shape[1] + space_y

    # 设置为最大随机数 乘 可放下的数量向上取整
    cdef int draw_x_fre = div_ceil(back_shape_x, draw_img_x_max)
    cdef int draw_y_fre = div_ceil(back_shape_y, draw_img_y_max)

    # 计算绘制层大小
    cdef int draw_back_shape_x = (draw_x_fre * draw_img_x_max) + rand_x
    cdef int draw_back_shape_y = (draw_y_fre * draw_img_y_max) + rand_y

    # 创建白色底层
    cdef np.ndarray[dtype_t, ndim=3] draw_back = np.ones(
        (
            draw_back_shape_x,
            draw_back_shape_y,
            1
        ), dtype=int
    ) * 255

    # 错位坐标计算
    cdef int add_value = draw_img_x_max // 3
    cdef int x, y, x_value, y_value,rand_x_v ,rand_y_v
    for y in range(draw_y_fre):
        # 计算Y坐标
        y_value = (y + 1) * draw_img_y_max

        for x in range(draw_x_fre):
            # 计算X坐标
            x_value = (x + 1) * draw_img_x_max

            # 隔行错位
            if y % 2 == 1:
                x_value += add_value
            rand_x_v = random.randint(0, rand_x)  # 改成C的rand来加速
            rand_y_v = random.randint(0, rand_y)
            draw(
                draw_back,
                draw_img,
                x_value + rand_x_v,
                y_value + rand_y_v
            )

    # 裁切回原来大小
    draw_back = draw_back[
                0:back_shape_x,
                0:back_shape_y,
                ]

    return draw_back