import os
import sys
import random
import numpy as np
import pandas as pd
import glob
import time
import matplotlib.pyplot as plt
import webbrowser

#
# update PYTHONPATH
#
sys.path.append(os.getcwd())

from test_output import Test_Output, Test_record

facil_choices = (
    "Kitchen",
    "Shower",
    "Room",
    "Den",
    "Patio",
    "Sauna",
    "Dog House",
    "Abuelita's Studio",
    "Dining Room",
    "Coat Room",
    "Closet",
    "Home Gym",
    "Club House",
    "Tree House",
    "Avery",
)
desc_choices = (
    "Iguana",
    "Mariposa",
    "Chupacabra",
    "Rana",
    "Aardvark",
    "Tiburon",
    "Weasle",
    "Culebra",
    "Cat",
    "Dog",
    "Pig",
    "Horse",
    "Mule",
)

test_report = Test_Output()

test_report.init_report("Test_Report")

for i in range(300):
    test_report.add_report_record(
        Test_record(
            Facility=random.choice(facil_choices),
            Description=random.choice(desc_choices),
            Result=random.choice((int(0), int(8))),
            Minutes_elapsed=int(random.random() * 10 ** 2),
            Time_stamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        )
    )

test_report.write_report(display_report=True)

test_report.write_csv("csv_file")

combined_df = pd.concat(
    [pd.read_csv(f) for f in glob.glob("C:/Users/Cisco/key_stats/*.csv")],
    ignore_index=True,
)

# Chart 1
df_plot = combined_df.pivot_table(
    "Minutes_elapsed", index="Facility", columns="Description"
)
df_plot.plot(kind="bar")
plt.title("Animal Speed by Facility")
plt.ylabel("seconds")
plt.tight_layout()

# Chart 2
df_avg_speed = (
    combined_df["Minutes_elapsed"]
    .groupby(combined_df["Description"])
    .mean()
    .sort_values(ascending=False)
)
df_avg_speed.plot(kind="barh")
plt.title("Animal Mean Speed")
plt.xlabel("seconds")
plt.tight_layout()

# Chart 3
animal_results = pd.crosstab(combined_df["Result"], combined_df["Description"]).apply(
    lambda r: r / r.sum(), axis=0
)
animal_results.unstack(level=0).plot(kind="bar", stacked=True)

# Chart 4
df_info = combined_df.pivot_table(
    "Minutes_elapsed", index="Facility", columns="Description"
)

# subplot
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
df_plot.plot(kind="bar", ax=ax1)
df_avg_speed.plot(kind="barh", ax=ax2)
animal_results.unstack(level=0).plot(kind="bar", stacked=True, ax=ax3)
df_info.plot(ax=ax4)
plt.tight_layout()

plt.savefig(os.fspath("stats.png"))

# open file in either Windows or Mac
def open_file():
    file = "stats.png"
    if os.name == "nt":
        os.startfile(Path(file))
    else:
        os.system("start " + (Path + file))


open_file()
