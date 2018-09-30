# https://mp.weixin.qq.com/s/GAJMX6IwUWzMlz7PW71M1A
# matplotlib使用numpy进行数组运算,

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

fig = Figure()
# 在matplotlib中,整个图像为一个figure对象.在figure对象中包含一个或者多个Axes对象,
# 每一个Axes对象拥有一个自己左表系统的绘图区域
canvas = FigureCanvas(fig)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])  # ax为坐标轴
line, = ax.plot([0, 1], [0, 1])
ax.set_title('a straight line (00)')  # 设置标题
ax.set_xlabel('x value')  # Label为坐标轴标注
ax.set_ylabel('y value')
# Artist只是在程序逻辑上的绘图
canvas.print_figure('demo.jpg')  # canvas理解为绘图的物理(或者说硬件)实现

# 用plot绘制线，还是scatter绘制散点，它们依然是比较成熟的函数。matplotlib实际上提供了更大的自由度，
# 允许用户以更基础的方式来绘制图形，比如下面，我们绘制一个五边形。


import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.path import Path
import matplotlib.patches as patches

fig = Figure()
canvas = FigureCanvas(fig)

ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
verts = [[0., 0.], [0., 1.], [0.5, 1.5], [1., 1.], [1., 0.], [0., 0.]]  # 图中五个点
codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY, ]  # 线
path = Path(verts, codes)

patch = patches.PathPatch(path, facecolor='coral')
ax1.add_patch(patch)  # ax为坐标轴,patch对象添加到预先准备好的ax上，就完成了整个绘图。
ax1.set_xlim(-0.5, 2)
ax1.set_ylim(-0.5, 2)

canvas.print_figure('house.png')
