import numpy as np
import pandas as pd

def process_data(wait_file):
    wait_data = pd.read_csv(wait_file, header=0)
    wait_data = wait_data[pd.notnull(wait_data["Waitlist Time (Days)"])]
    loc_wait = {}
    wait_avg = {}
    wait_avg_open = {}

    locs = wait_data["Location"]
    match = wait_data["Match Date"]
    wait_time = wait_data["Waitlist Time (Days)"]

    for loc in range(len(locs)):
        if locs[loc] == locs[loc]:
            if locs[loc] not in loc_wait:
    	        loc_wait[locs[loc]] = []
            loc_wait[locs[loc]].append(wait_time[loc])

    for loc in loc_wait:
        if loc == loc:
            wait_avg[loc] = (sum(loc_wait[loc])/float(len(loc_wait[loc])), len(loc_wait[loc]))

    return wait_avg

process_data("waitlist.csv")



