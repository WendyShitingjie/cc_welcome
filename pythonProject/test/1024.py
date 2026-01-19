import turtle


def draw_text(text, font_size=14):
    # 设置字体和大小
    turtle.setup(1000, 300)  # 设置窗口大小
    turtle.speed(0)  # 绘制速度，0为最快
    font = ("Arial", font_size, "normal")
    turtle.pencolor("orange")  # 设置笔的颜色为橙色

    # 分割文本，逐字符绘制以适应不同长度的文本
    x_pos = -170  # 初始x坐标调整为负值，使文字更靠左
    y_pos = 50  # 初始y坐标

    for char in text:
        turtle.penup()  # 抬笔
        turtle.goto(x_pos, y_pos)
        turtle.pendown()  # 落笔
        turtle.write(char, align="center", font=font)

        # 更新x坐标以便绘制下一个字符
        x_pos += font_size * 1  # 减小字符间距，使排版更紧凑

    turtle.done()


# 调用函数绘制橙色文本
draw_text("午夜编程乐无边，咖妃作伴似神仙。"
          "祝程序yuan们时常灵感乍现，法力无边！！！")