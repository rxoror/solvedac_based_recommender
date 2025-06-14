# 차트 처리 코드

import plotly.express as px
import pandas as pd

TAG8 = ["math", "implementation", "greedy", "string", "data_structures", "graphs", "dp", "geometry"]

def make_tag_df(data):
    return pd.DataFrame({
          "tag": TAG8, 
          "performance": data
    })

def make_figure(data):
    return px.line_polar(make_tag_df(data), r="performance", theta="tag", line_close=True)