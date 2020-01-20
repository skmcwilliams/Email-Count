import numpy as np
import pandas as pd
import sqlite3
from bokeh.io import show, output_file
from bokeh.plotting import figure

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

"""
#Check dataframe
print(df)
print(df.shape)
print(idx)
print(idy)

"""


#Create bar chart from dataframe
p = figure(x_range=idx, plot_width=1800,
           plot_height=500, title="Email Count by Organization",
           toolbar_location=None, tools="pan,reset,save,wheel_zoom")

p.vbar(x=idx, top=idy, width=1, color="#c9d9d3", legend_label=str(idy))

p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.legend.location = "top_center"
p.legend.orientation = "horizontal"

try: 
    show(p)
except Exception:
    traceback.print_exc()
print("View " + output_file + ' in browser')
cur.close()
