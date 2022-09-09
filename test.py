import draw
import numpy as np


def print_array(np_arr: np.ndarray):
    """打印矩阵"""
    for y in range(np_arr.shape[0]):
        for x in range(np_arr.shape[1]):
            # print(x, y)
            print(np_arr[y, x], "\t", end="")
        print()


draw_img = np.array([[1, 2], [3, 4], [5, 6]], dtype=np.uint8)
print(draw_img.dtype)

re_img = draw.draw_all(draw_img, 9, 6, 0, 0, 0, 0)

print_array(re_img)

print("end")
