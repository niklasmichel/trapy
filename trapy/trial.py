import ntpath
import pandas as pd
import numpy as np
from sklearn import metrics
import math


class Trial:
    """Class to hold all relevant info of a single tape response assay trial."""
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.trial_name = ntpath.basename(path_to_file)
        self.date = self.trial_name[:6]
        self.mouse = self.trial_name[6:8]
        self.group = self.trial_name[8:-4]
        self.boutlist = create_boutlist(self.path_to_file)
        self.idle_time = idle_time(self.boutlist)
        self.total_bouts = total_bouts(self.boutlist)
        self.total_time = total_time(self.boutlist)
        self.bouts_per_minute = bouts_per_minute(self.boutlist)
        self.success = trial_success(self.boutlist)
        self.auc = area_under_the_curve(self.boutlist)
        self.tibi = tape_induced_behaviour_index(self.boutlist)
        self.timecourse300 = bout_time_curve_300(self.boutlist)
        self.timecourse = bout_time_curve(self.boutlist)
        self.auctimecourse300 = auc_time_curve300(self.timecourse300)


def create_boutlist(path_to_file):
    """Converts csv ouput of timer app to a list of times of bouts in seconds; 
    300 is added at the end if mouse did not get tape off in time.
    """
    df = pd.read_csv(path_to_file, sep=" ", header=None)
    boutlist = []
    bouts_after_300s = 0  # bouts after 5 minute trial time are not relevant for statistics

    for index, row in df.iterrows():
        hours = int(row[1].replace('h', ''))
        minutes = int(row[2].replace('m', ''))
        seconds = int(row[3].replace('s', ''))
        milliseconds = float(int(row[4].replace('ms', '')))  # milliseconds are given as 1 second / 100 here
        seconds_total = hours * 3600 + minutes * 60 + seconds + milliseconds * 0.01

        if seconds_total < 300:
            boutlist.append(seconds_total)  # len(boutlist) is total bout count now
        else:
            bouts_after_300s += 1

    if bouts_after_300s > 0:
        boutlist.append(300)

        # len(boutlist)-1 is total bout count for full trials now, 
    # the 300 in the end signifies that mouse didn't get tape off in time
    # keep in mind that 'full trials' (5 min, no 'success') have total bouts
    # of len(boutlist)-1, while successful trials have len(boutlist) total bouts!!

    return boutlist


def idle_time(boutlist, idle_threshold=15):
    """Takes list of times of bouts in seconds, returns idle time in seconds, 
    i.e. time spent without bout for longer than idle_threshold in seconds.
    """
    idle_time = 0
    for i in range(0, len(boutlist) - 2):
        inter_bout_time = boutlist[i + 1] - boutlist[i]
        if inter_bout_time > idle_threshold:
            idle_time += inter_bout_time
    return idle_time


def total_bouts(boutlist):
    """Takes list of times of bouts in seconds, returns number of total tape-directed bouts performed.
    Takes into account, that a 300 at the end signifies a full trial (ending time), not an actual bout.
    """
    if boutlist[-1] == 300:
        total_bouts = len(boutlist) - 1
    else:
        total_bouts = len(boutlist)
    return total_bouts


def total_time(boutlist):
    """Takes list of times of bouts in seconds, returns it's last item representing the total trial time."""
    total_time = boutlist[-1]
    return total_time


def bouts_per_minute(boutlist):
    """Takes list of times of bouts in seconds, returns bpm = total_bouts / total_time."""
    bpm = (total_bouts(boutlist) / total_time(boutlist)) * 60
    return bpm


def tape_induced_behaviour_index(boutlist):
    """Takes list of times of bouts in seconds, returns tibi = BPM * (5 - idle_time / 60).
    This measure is supposed to unite activity, inactivity and success in one KPI.
    """
    tibi = bouts_per_minute(boutlist) * (5 - idle_time(boutlist) / 60)
    return tibi


def trial_success(boutlist):
    """Takes list of times of bouts in seconds, 
    returns bool of whether the mouse managed to get the tape off in time.
    """
    if boutlist[-1] == 300:
        success = False
    else:
        success = True
    return success


def area_under_the_curve(boutlist):
    """Takes list of times of bouts in seconds, returns the area under the curve. Utilises the trapezoidal rule."""
    auc = metrics.auc(boutlist, range(0, len(boutlist)))
    return auc


def bout_time_curve_300(boutlist):
    """Takes list of times of bouts in seconds, converts it to list of bout counts per second over 300 seconds.
    Returned list will always have 301 items, that can be NaN if trial has ended before the 300 second mark.
    """
    timecourse = []
    for i in range(0, 301):
        if i < math.ceil(boutlist[-1]) + 1:
            counter = 0
            for time in boutlist:
                if time <= i:
                    counter += 1
        else:
            counter = np.nan

        timecourse.append(counter)
    return timecourse


def bout_time_curve(boutlist):
    """Takes list of times of bouts in seconds,
    converts it to list of bout counts per second over trial time in seconds.
    """
    timecourse = []
    for i in range(0, math.ceil(boutlist[-1]) + 1):
        counter = 0
        for time in boutlist:
            if time <= i:
                counter += 1
            if counter > total_bouts(boutlist):
                counter = np.nan
        if i == 300:
            counter = total_bouts(boutlist)
        timecourse.append(counter)
    return timecourse

def auc_time_curve300(timecourse300):
    l = []
    for i in range(1,len(timecourse300), 1):
        ys = [timecourse300[i-1], timecourse300[i]]
        l.append(0.5 * np.sum(ys))  # trapezoidal rule
    return l
