import difflib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

jobs = pd.read_csv("jobs.csv")
jobs["technologies"] = jobs["technologies"].str.lower()

tech = (
    jobs["technologies"]
    .str.split(",\s*", expand=True)
    .stack()
    .reset_index(level=1, drop=True)
    .rename("technology")
)
jobs_split = jobs.drop("technologies", axis=1).join(tech)

tech_group = {}
for technology in jobs_split["technology"].unique():
    similar_tech = difflib.get_close_matches(
        technology, tech_group.keys(), n=1, cutoff=0.8
    )
    if similar_tech:
        tech_group[similar_tech[0]] += jobs_split[
            jobs_split["technology"] == technology
        ].shape[0]
    else:
        tech_group[technology] = (
            jobs_split[jobs_split["technology"] == technology].shape[0]
        )

tech_count = pd.Series(tech_group)
tech_count.sort_values(ascending=False, inplace=True)

plt.figure(figsize=(10, 6))
tech_count.head(30).plot(kind="bar", color="skyblue")
plt.title("Top 30 Popular Technologies in Job Vacancies")
plt.xlabel("Technologies")
plt.ylabel("Count")
plt.xticks(rotation=90, ha="right")
plt.tight_layout()
plt.show()
