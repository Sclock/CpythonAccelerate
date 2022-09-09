from draw import draw_all
# from test_np import test_def
import numpy as np
from py_draw import all_draw
import time

# def print_array(np_arr: np.ndarray):
#     """打印矩阵"""
#     for y in range(np_arr.shape[0]):
#         for x in range(np_arr.shape[1]):
#             # print(x, y)
#             print(np_arr[y, x], "\t", end="")
#         print()

# draw_img = np.array([[1, 2], [3, 4], [5, 6]]).astype('uint8')

draw_img = np.ones(
    (
        500,
        300,
    )
).astype('uint8') * 0

s_t = time.time()
c_re_img = draw_all(draw_img, 2000, 2000, 0, 0, 0, 0)
print("cy", time.time() - s_t)


s_t = time.time()
p_re_img = all_draw(draw_img, 2000, 2000, 0, 0, 0, 0)
print("py", time.time() - s_t)


print((c_re_img == p_re_img).all())

print("end")
