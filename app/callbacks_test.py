from bokeh.plotting import curdoc, figure
from bokeh.models import CustomJS

# プロットを作成
plot = figure(width=400, height=400)

# レイアウトにプロットを追加
curdoc().add_root(plot)

# カスタムコールバックを作成
callback = CustomJS(code="""
    // JavaScriptで変数を定義
    var js_variable = 42;

    // Bokehサーバーに変数を送信
""")

# カスタムコールバックをプロットに追加
plot.js_on_change('change', callback)

# コールバック関数を定義してPythonの変数にデータを格納する

def python_callback(attr, old, new): 

    python_variable = new
    print("Python variable:", python_variable)

# プロットにコールバック関数を追加
plot.on_change('change', python_callback)