from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid
from bokeh.models.glyphs import VBar
from bokeh.io import curdoc, save
import numpy as np
import pandas as pd
import sqlite3



#Form SQL connection and create table
con = sqlite3.connect('emaildb.sqlite')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('''CREATE TABLE Counts (org TEXT, count INTEGER)''')

#pull from .txt file containing emails
fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    line = line.split('@')
    organization = line[1]
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (organization,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (organization,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (organization,))
    con.commit()

#https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 20'

#print top 20 email senders to terminal and create bar chart
for row in cur.execute(sqlstr):
    """Check output data
    #print(str(row[0]), row[1])"""

#set output filename and read sql file for vbar to be made later
output_file = 'EmailCount.html'
df = pd.read_sql_query('SELECT * FROM Counts', con)
"""Check dataframe
print(df.head())"""

#Create bar chart from dataframe
x = df[['org']]
y = df[['count']]
source = ColumnDataSource(dict(x=x,top=y,))
plot = Plot( title= None, plot_width=300, plot_height=300, min_border=0, toolbar_location=None)

glyph = VBar(x='org', top="top", bottom=0, width=0.5, fill_color="#b3de69")
plot.add_glyph(source, glyph)

xaxis = LinearAxis()
plot.add_layout(xaxis, 'below')

yaxis = LinearAxis()
plot.add_layout(yaxis, 'left')

plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

curdoc().add_root(plot)

save(plot)
print('Open ' + output_file + ' to view Bar Chart' )
    
cur.close()