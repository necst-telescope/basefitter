from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

# サンプルデータ
x = list(range(10))
y = [i**2 for i in x]

source = ColumnDataSource(data=dict(x=x, y=y))

# 左側の図
left_plot = figure(width=400, height=400, title="左の図")
left_plot.circle("x", "y", size=10, source=source)

# 右側の図
right_plot = figure(width=400, height=400, title="右の図")
right_plot.circle("x", "y", size=10, source=source)


# Pythonコールバック関数
def update_right_plot(attr, old, new):
    right_plot.x_range.start = left_plot.x_range.start
    right_plot.x_range.end = left_plot.x_range.end
    right_plot.y_range.start = left_plot.y_range.start
    right_plot.y_range.end = left_plot.y_range.end


# 左の図の範囲変更を監視
left_plot.x_range.on_change("start", update_right_plot)
left_plot.x_range.on_change("end", update_right_plot)
left_plot.y_range.on_change("start", update_right_plot)
left_plot.y_range.on_change("end", update_right_plot)

# 並べて表示
layout = row(left_plot, right_plot)
curdoc().add_root(layout)
