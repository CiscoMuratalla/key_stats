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

df_plot = df.pivot_table('Execution_time', index = 'Facility', columns = 'Description')

df_plot.plot(kind='bar')
plt.ylabel('seconds')
plt.tight_layout()

plt.savefig(os.fspath('stats.png'))

os.startfile(Path('stats.png'))
