import numpy as np
import pandas as pd

def process_data(wait_file, include_matched=True):
    wait_data = pd.read_csv(wait_file, header=0)
    wait_data = wait_data[pd.notnull(wait_data["Waitlist Time (Days)"])]
    loc_wait = {}
    loc_wait_open = {}
    wait_avg = {}
    wait_avg_open = {}

    locs = wait_data["Location"]
    match = wait_data["Match Date"]
    remove = wait_data["Removal Date"]
    wait_time = wait_data["Waitlist Time (Days)"]

    for i in range(len(locs)):
        loc = locs[i]
        if not pd.isnull(loc):
            loc = loc.strip()
            if loc not in loc_wait:
    	        loc_wait[loc] = []
            loc_wait[loc].append(wait_time[i])
            if pd.isnull(match[i]) and pd.isnull(remove[i]):
                if loc not in loc_wait_open:
                    loc_wait_open[loc] = []
                loc_wait_open[loc].append(wait_time[i])

    for loc in loc_wait:
        wait_avg[loc] = (
            sum(loc_wait[loc]) / float(len(loc_wait[loc])), len(loc_wait[loc]))

    for loc in loc_wait_open:
        wait_avg_open[loc] = (
            sum(loc_wait_open[loc]) / float(len(loc_wait_open[loc])), len(loc_wait_open[loc]))

    if include_matched:
        return wait_avg
    else:
        return wait_avg_open

process_data("waitlist.csv")
