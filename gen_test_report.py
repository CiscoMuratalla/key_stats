import os
import sys
import random
from pathlib import Path
import numpy as np
import pandas as pd
import glob
import datetime
import matplotlib.pyplot as plt

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
                          Output = ''
              )
   )

test_report.write_report(display_report = True)

test_report.write_csv('csv_file')

# create dataframe with all csv files in path then plot

path = os.getcwd()

df = pd.concat([pd.read_csv(f) for f in glob.glob(path + '/*.csv')])


# convert int to str in 'Result'
df['Result'] = df['Result'].apply(lambda x: 'Fail' if 0 <= x <= 5 else 'Success')

# Chart 1
df_plot = df.pivot_table('Execution_time', index = 'Facility', columns = 'Description')
df_plot.plot(kind='bar')
plt.title('Animal Speed by Facility')
plt.ylabel('seconds')
plt.tight_layout()

# Chart 2
df_avg_speed = df['Execution_time'].groupby(df['Description']).mean().sort_values(ascending=False)
df_avg_speed.plot(kind='barh')
plt.title('Animal Mean Speed')
plt.xlabel('seconds')
plt.tight_layout()

# Chart 3
animal_results = pd.crosstab(df['Result'],df['Description']).apply(lambda r: r/r.sum(), axis=0)
animal_results.unstack(level=0).plot(kind='bar', stacked=True)

# Chart 4
df_info = df.pivot_table('Execution_time', index = 'Facility', columns = 'Description')

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
