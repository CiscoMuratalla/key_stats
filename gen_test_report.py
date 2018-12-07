import os
import sys
import random
from pathlib import Path
import numpy as np
import pandas as pd
import glob
import datetime
import matplotlib.pyplot as plt
import plotly as py
py.tools.set_credentials_file(username = 'ciscomuratalla', api_key = 'gDxJPZBcIwMITdr6dMnb')
#py.tools.get_embed('https://plot.ly/~ciscomuratalla/66')
import cufflinks as cf
import webbrowser

# NEW TASK
# Focused charts based on Description then Facility
# result ratio failed and succeeded
# mean of excecution time
# interactive html page that allows for -
# selection discrete Description or Facility

#
# update PYTHONPATH
#
sys.path.append(os.getcwd())

from test_output import Test_Output, Test_record

desc_choices = ('Cat', 'Dog', 'Pig', 'Horse', 'Mule')

info_choices = ('Red', 'Blue', 'Purple', 'Brown', 'Maroon')

facil_choices = ('Kitchen', 'Shower', 'Room', 'Den', 'Patio')

test_report = Test_Output()

test_report.init_report('Test_Report')

for i in range(300):
    test_report.add_report_record(
              Test_record(
                          Facility = random.choice(facil_choices),
                          Test_group = int(random.random() * 10**3),
                          Test_number = i,
                          Description = random.choice(desc_choices),
                          Result = random.choice((0,8)),
                          Execution_time = int(random.random() * 10**3),
                          Information = random.choice(info_choices),
              )
   )

test_report.write_report(display_report = True)

test_report.write_csv('csv_file')

# create dataframe with all csv files in path then plot

path = os.getcwd()

files = glob.glob('*.csv')
list_of_dfs = [pd.read_csv(filename) for filename in files]
# for df, filename in zip(list_of_dfs, files):
#     df['filename'] = filename

# concatenate list of csv files into one dataframe
combined_df = pd.concat(list_of_dfs, ignore_index=True)

# convert Execution_time from seconds to minutes
combined_df['Execution_time'] = (combined_df['Execution_time']/60).round(1)

# rename columns
combined_df.rename(columns = {'Execution_time' : 'Minutes_elapsed'}, inplace = True)

# df = pd.concat([pd.read_csv(f) for f in glob.glob(path + '/*.csv')])

# convert int to str in 'Result'
combined_df['Result'] = combined_df['Result'].apply(lambda x: 'Fail' if 0 <= x <= 5 else 'Success')

# Chart 1
df_plot = combined_df.pivot_table('Minutes_elapsed', index = 'Facility', columns = 'Description')
df_plot.plot(kind='bar')
plt.title('Animal Speed by Facility')
plt.ylabel('seconds')
plt.tight_layout()

# Chart 2
df_avg_speed = combined_df['Minutes_elapsed'].groupby(combined_df['Description']).mean().sort_values(ascending=False)
df_avg_speed.plot(kind='barh')
plt.title('Animal Mean Speed')
plt.xlabel('seconds')
plt.tight_layout()

# Chart 3
animal_results = pd.crosstab(combined_df['Result'],combined_df['Description']).apply(lambda r: r/r.sum(), axis=0)
animal_results.unstack(level=0).plot(kind='bar', stacked=True)

# Chart 4
df_info = combined_df.pivot_table('Minutes_elapsed', index = 'Facility', columns = 'Description')

# subplot
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10,10))
df_plot.plot(kind='bar', ax=ax1)
df_avg_speed.plot(kind='barh', ax=ax2)
animal_results.unstack(level=0).plot(kind='bar', stacked=True, ax=ax3)
df_info.plot(ax=ax4)
plt.tight_layout()

plt.savefig(os.fspath('stats.png'))

# open file in either Windows or Mac
def open_file():
    file = 'stats.png'
    if os.name == 'nt':
        os.startfile(Path(file))
    else:
        os.system('start '+ (Path + file))

open_file()

# drop unnecessary columns
simple = combined_df.drop(['Test_group', 'Test_number', 'Information', 'Output', 'Result'], axis =1)

# create pivot table dataframe
s = pd.pivot_table(simple, index = 'Description', columns = 'Facility', values = 'Minutes_elapsed')

# plot dataframe
s.iplot(yTitle = 'Minutes', title = 'Minutes Elapsed', mode = 'lines+markers')

# open plot
url = 'https://plot.ly/~ciscomuratalla/66'
webbrowser.open(url)
