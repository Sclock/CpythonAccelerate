# cython: language_level=3
# cython: cdivision=True
import cython
from libc.stdint cimport uint8_t
from libc.stdlib cimport rand

import numpy as np
cimport numpy as np


np.import_array()

# ctypedef np.uint8_t dtype_t
ctypedef np.long dtype_t

cdef void draw(uint8_t[:,:,::1] img_back, uint8_t[:,:] img_draw, int x, int y):
    # 作业大小
    cdef int draw_region_x = <int>img_draw.shape[1]
    cdef int draw_region_y = <int>img_draw.shape[0]

    # 坐标位置加上大小
    cdef int x2 = x + draw_region_x
    cdef int y2 = y + draw_region_y

    cdef uint8_t[:,:] img_back_draw = img_back[y:y2, x:x2][:,:,0]

    # 写区域
    cdef np.ndarray[dtype_t, ndim=2] new_back = np.empty(
        (
            draw_region_y,
            draw_region_x,
        ), dtype=int
    ) * 255

    # 开始拼合
    # 底图和水印谁更小取谁
    for _y in range(draw_region_y):
        for _x in range(draw_region_x):
            if img_draw[_y, _x] < img_back_draw[_y, _x]:
                new_back[_y, _x] = img_draw[_y, _x]
            else:
                new_back[_y, _x] = img_back_draw[_y, _x]

    img_back[y:y2, x:x2][:,:,0] = new_back

@cython.cdivision(True)
cdef inline int div_ceil(int a, int b):
    if not a%b:
        return a/b
    else:
        return a/b+1

@cython.cdivision(True)
cdef inline int randint(int a):
    return rand() % a


cpdef np.ndarray[dtype_t, ndim=3] draw_all(uint8_t[:,:]  draw_img, int back_shape_x, int back_shape_y, int rand_x, int rand_y , int space_x, int space_y):
    
    # 网格间距
    cdef int draw_img_x_max = <int>draw_img.shape[1] + space_x
    cdef int draw_img_y_max = <int> draw_img.shape[0] + space_y

    # 错位坐标计算
    cdef int add_value = draw_img_x_max // 3

    # 设置为最大随机数 乘 可放下的数量向上取整
    cdef int draw_x_fre = div_ceil(back_shape_x, draw_img_x_max)
    cdef int draw_y_fre = div_ceil(back_shape_y, draw_img_y_max)

    # 计算绘制层大小
    cdef int draw_back_shape_x = (draw_x_fre * draw_img_x_max) + rand_x
    cdef int draw_back_shape_y = (draw_y_fre * draw_img_y_max) + rand_y + add_value

    # 创建白色底层
    cdef np.ndarray[long, ndim=3] draw_back = np.ones(
        (
            draw_back_shape_y,
            draw_back_shape_x,
            1
        ), dtype=int
    ) * 255


    for y in range(draw_y_fre):
        # 计算Y坐标
        y_value = y * draw_img_y_max

        for x in range(draw_x_fre):
            # 计算X坐标
            x_value = x * draw_img_x_max

            rand_x_v = randint(rand_x)  # 改成C的rand来加速
            rand_y_v = randint(rand_y)

            # 隔行错位
            if x % 2 == 1:
                rand_y_v += add_value

            draw(
                draw_back,
                draw_img,
                x_value + rand_x_v,
                y_value + rand_y_v
            )

    # 裁切回原来大小
    draw_back = draw_back[
                0:back_shape_y,
                0:back_shape_x,
                ]

    return draw_back
