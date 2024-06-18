from bokeh.layouts import column
from bokeh.models import TextInput, ColumnDataSource
from bokeh.plotting import curdoc
from bokeh.plotting import figure
import xarray as xr
from bokeh.layouts import Row
from bokeh.events import SelectionGeometry
import numpy as np

text_input = TextInput(
    value="path/to/xarray",
    title="Please input file path of an xarray to be analysed",
    width=1000,
)
curdoc().add_root(column(text_input))


def data_plotter_callback(attr, old, new):
    print(new)
    print("loading.....")
    da = xr.open_dataarray(new)
    dictionary = {}
    dictionary["lon_cor"] = da.lon_cor.values
    dictionary["lat_cor"] = da.lat_cor.values
    dictionary["raw"] = da
    source.data = dictionary
    p1.scatter(x="lon_cor", y="lat_cor", source=source)
    print("loaded!!")


#    print("Python variable:", da.shape)


def box_select_callback(event):
    selected_indices = event.geometry
    x0, x1 = selected_indices["x0"], selected_indices["x1"]
    y0, y1 = selected_indices["y0"], selected_indices["y1"]
    print(x0, x1, y0, y1)
    if (x1 >= x0) & (y1 >= y0):
        source2.data["raw"] = source.data["raw"].where(
            (
                (source.data["raw"]["lon_cor"] >= x0)
                & (source.data["raw"]["lon_cor"] < x1)
            )
            & (
                (source.data["raw"]["lat_cor"] >= y0)
                & (source.data["raw"]["lat_cor"] < y1)
            )
        )
        print("(x1 >= x0) & (y1 >= y0)")

    elif (x1 < x0) & (y1 >= y0):
        source2.data["raw"] = source.data["raw"].where(
            (
                (source.data["raw"]["lon_cor"] < x0)
                & (source.data["raw"]["lon_cor"] >= x1)
            )
            & (
                (source.data["raw"]["lat_cor"] >= y0)
                & (source.data["raw"]["lat_cor"] < y1)
            )
        )
        print("(x1 < x0) & (y1 >= y0)")

    elif (x1 >= x0) & (y1 < y0):
        source2.data["raw"] = source.data["raw"].where(
            (
                (source.data["raw"]["lon_cor"] >= x0)
                & (source.data["raw"]["lon_cor"] < x1)
            )
            & (
                (source.data["raw"]["lat_cor"] < y0)
                & (source.data["raw"]["lat_cor"] >= y1)
            )
        )
        print("(x1 >= x0) & (y1 < y0)")

    elif (x1 < x0) & (y1 < y0):
        source2.data["raw"] = source.data["raw"].where(
            (
                (source.data["raw"]["lon_cor"] < x0)
                & (source.data["raw"]["lon_cor"] > x1)
            )
            & (
                (source.data["raw"]["lat_cor"] < y0)
                & (source.data["raw"]["lat_cor"] > y1)
            )
        )
        print("(x1 < x0) & (y1 < y0)")

    # print("Selected data:", source2.data)
    source3.data["channel"] = source2.data["raw"].ch.values
    source3.data["spectra_averaged"] = np.nanmean(source2.data["raw"].data, axis=0)
    print(source3.data["spectra_averaged"])
    p2.scatter(x="channel", y="spectra_averaged", source=source3)
    print("plot completed")


# プロットにコールバック関数を追加
source = ColumnDataSource(data=dict(length=[], width=[]))
source2 = ColumnDataSource(data=dict(length=[], width=[]))
source3 = ColumnDataSource(data=dict(length=[], width=[]))

source.data = {"lon_cor": [], "lat_cor": []}
source2.data = {}
source3.data = {}

p1 = figure(
    tools="pan,box_zoom,lasso_select,box_select,poly_select,tap,wheel_zoom,reset,save,zoom_in",
    title="Select data points",
    width=1000,
    height=800,
)


p2 = figure(
    tools="pan,box_zoom,lasso_select,box_select,wheel_zoom,reset,save,zoom_in",
    title="Averaged Spectra",
    width=1000,
    height=800,
)


# p1.scatter(x="lon_cor", y="lat_cor", source=source)
text_input.on_change("value", data_plotter_callback)
p1.on_event(SelectionGeometry, box_select_callback)


# p2.scatter(x="channel", y="spectra_averaged", source=source3)
layout = Row(p1, p2)
curdoc().add_root(layout)
