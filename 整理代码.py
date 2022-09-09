import numpy as np
import random


def draw(back_img: np.ndarray, draw_img: np.ndarray, y: int, x: int) -> np.ndarray:
    """
    L模式输入底图,写图,和坐标
    图像叠加,指定区域改写为新图片
    """

    # 坐标位置加上大小
    x2 = x + draw_img.shape[1]
    y2 = y + draw_img.shape[0]

    # 提取底图书写区域
    back_draw = back_img[y:y2, x:x2][:, :, 0]

    # 开始拼合
    # 底图和水印谁更小取谁
    back_draw_ed = np.clip(
        np.where(
            draw_img < back_draw,
            draw_img,
            back_draw
        ), 0, 255
    )

    # 处理完毕，赋值回去
    back_img[y:y2, x:x2][:, :, 0] = back_draw_ed
    return back_img


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
    draw_img_x_max = draw_img.shape[0] + space_x
    draw_img_y_max = draw_img.shape[1] + space_y

    # 设置为最大随机数 乘 可放下的数量向上取整
    draw_x_fre = div_ceil(back_shape_x, draw_img_x_max)
    draw_y_fre = div_ceil(back_shape_y, draw_img_y_max)

    # 计算绘制层大小
    draw_back_shape_x = (draw_x_fre * draw_img_x_max) + rand_x
    draw_back_shape_y = (draw_y_fre * draw_img_y_max) + rand_y

    # 创建白色底层
    draw_back = np.ones(
        (
            draw_back_shape_x,
            draw_back_shape_y,
            1
        ), dtype=int
    ) * 255

    # 错位坐标计算
    add_value = draw_img_x_max // 3

    for y in range(draw_y_fre):
        # 计算Y坐标
        y_value = (y+1) * draw_img_y_max

        for x in range(draw_x_fre):
            # 计算X坐标
            x_value = (x+1) * draw_img_x_max

            # 隔行错位
            if y % 2 == 1:
                x_value += add_value

            rand_x_v = random.randint(0, rand_x)
            rand_y_v = random.randint(0, rand_y)
            draw_back = draw(
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


draw_back = [[[255, 255, 255, 0], [255, 255, 255, 0]],
             [[255, 255, 255, 0], [255, 255, 255, 0]]]

draw_img = [[[255], [255]],
            [[255], [255]]]
