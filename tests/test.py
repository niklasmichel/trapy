import trapy
from pathlib import Path

folder = str(Path.cwd()) + '/test_data'

#trapy.analyze_trials(folder)

# output:
#
# /home/niklas/anaconda3/bin/python /home/niklas/PycharmProjects/trapy/tests/test.py
# Analyzing txt files in given folder...
# Calculated Metrics from txt files in /home/niklas/PycharmProjects/trapy/tests/test_data
# Writing sheet "All Trials Metrics" to TapeResponseAssay.xlsx.
# Writing sheet for metrics of group "group_1" to TapeResponseAssay.xlsx.
# Writing sheet for time courses of group "group_1" to TapeResponseAssay.xlsx.
# Writing sheet for metrics of group "group_2" to TapeResponseAssay.xlsx.
# Writing sheet for time courses of group "group_2" to TapeResponseAssay.xlsx.
# All done; see /home/niklas/PycharmProjects/trapy/tests/TapeResponseAssay.xlsx

trapy.analyze_trials_csv(folder)

# output:
#
# /home/niklas/anaconda3/bin/python /home/niklas/PycharmProjects/trapy/tests/test.py
# Analyzing txt files in given folder...
# Calculated Metrics from txt files in /home/niklas/PycharmProjects/trapy/tests/test_data
# Writing all_trials_metrics.csv
# Writing group_1_metrics.csv
# Writing group_1_time_courses.csv
# Writing group_2_metrics.csv
# Writing group_2_time_courses.csv
# All done; see csv files in /home/niklas/PycharmProjects/trapy/tests