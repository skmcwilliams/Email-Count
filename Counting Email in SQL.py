import numpy as np
import pandas as pd
import sqlite3
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Turbo256
import traceback

#Form SQL connection
con = sqlite3.connect('emaildb.sqlite')
cur = con.cursor()

#set output filename and read sql file for vbar to be made later
output_file = 'EmailCount.html'
df = pd.read_sql_query('SELECT org,count FROM Counts', con)
df = df.dropna()
idx = df['org'].tolist()
idy = df['count'].tolist()
idy.sort()

#Check Dataframe 
"""
#Check dataframe
print(df)
print(df.shape)
print(idx)
print(idy)

"""

#Create vbar chart from dataframe
source = ColumnDataSource(data=dict(idx=idx, idy=idy, color=Turbo256))

p = figure(x_range=idx, plot_width=1900,
           plot_height=500, title="Email Count by Organization",
           toolbar_location="left", tools="pan,reset,save,wheel_zoom")

p.vbar(x='idx', top='idy', width=1, color="color", legend_field='idy',source=source)
p.line(x=idx, y=idy, color="Chartreuse", line_width=2)

p.x_range.range_padding = 0
p.xgrid.grid_line_color = None
p.legend.location = "top_center"
p.legend.orientation = "horizontal"
p.title.align = 'center'

try: 
    show(p)
except Exception:
    traceback.print_exc()
print('View file in browser')
cur.close()
