import numpy as np
import random


def print_array(np_arr: np.ndarray):
    """打印矩阵"""
    for y in range(np_arr.shape[0]):
        for x in range(np_arr.shape[1]):
            # print(x, y)
            print(np_arr[y, x], "\t", end="")
        print()


def draw(img_back: np.ndarray, img_draw: np.ndarray, x: int, y: int) -> None:
    """
    L模式输入底图,写图,和坐标
    图像叠加,指定区域改写为新图片
    img_back shape: [x,y,1]
    img_draw shape: [x,y]
    """

    # 坐标位置加上大小
    x2: int = x + img_draw.shape[1]
    y2: int = y + img_draw.shape[0]

    # 提取底图书写区域
    img_back_draw = img_back[y:y2, x:x2][:, :, 0]

    # 写区域
    new_back = np.empty(
        (
            img_back_draw.shape[0],
            img_back_draw.shape[1],
        ), dtype=int
    ) * 255
    # new_back.shape [x,y]

    # 开始拼合
    # 底图和水印谁更小取谁
    for _y in range(img_draw.shape[0]):
        for _x in range(img_draw.shape[1]):
            if img_draw[_y, _x] < img_back_draw[_y, _x]:
                new_back[_y, _x] = img_draw[_y, _x]
            else:
                new_back[_y, _x] = img_back_draw[_y, _x]

    # 处理完毕，赋值回去
    img_back[y:y2, x:x2][:, :, 0] = new_back
    # img_back.shape [x,y,1]


def div_ceil(x: int, y: int) -> int:
    a, b = divmod(x, y)
    if b == 0:
        return a
    else:
        return a + 1


def all_draw(
    draw_img: np.ndarray,
    back_shape_x: int, back_shape_y: int,
    rand_x: int, rand_y: int,
    space_x: int, space_y: int
) -> np.ndarray:
    """完整密铺水印

    Args:
        draw_back (np.ndarray): 底图
        draw_img (np.ndarray): 水印
        rand_x (int): X方向上的随机数上限
        rand_y (int): Y方向上的随机数上限
        space_x (int): X方向上的基础间距
        space_y (int): Y方向上的基础间距

    Returns:
        np.ndarray: 叠加后的底图
    """

    # 网格间距
    draw_img_x_max: int = draw_img.shape[1] + space_x
    draw_img_y_max: int = draw_img.shape[0] + space_y

    # 错位坐标计算
    add_value: int = draw_img_y_max // 3

    # 设置为最大随机数 乘 可放下的数量向上取整
    draw_x_fre: int = div_ceil(back_shape_x, draw_img_x_max)
    draw_y_fre: int = div_ceil(back_shape_y, draw_img_y_max)

    # 计算绘制层大小
    draw_back_shape_x: int = (draw_x_fre * draw_img_x_max) + rand_x
    draw_back_shape_y: int = (draw_y_fre * draw_img_y_max) + rand_y + add_value

    # 创建白色底层
    draw_back = np.ones(
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

            rand_x_v = random.randint(0, rand_x)
            rand_y_v = random.randint(0, rand_y)

            # 隔行错位
            if x % 2 == 1:
                rand_y_v += add_value

            draw(
                draw_back,
                draw_img,
                x_value + rand_x_v,
                y_value + rand_y_v
            )
            print_array(draw_back)

    # 裁切回原来大小
    draw_back = draw_back[
        0:back_shape_y,
        0:back_shape_x,
    ]

    # draw_back.shape [x,y,1]
    return draw_back


if __name__ == '__main__':
    draw_img = np.array([[1, 2], [3, 4], [5, 6]])

    re_img = all_draw(draw_img, 9, 6, 0, 0, 0, 0)
    print(re_img.shape)
    # print_array(re_img)
