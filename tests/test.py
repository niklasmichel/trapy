from trapy import TRA
from pathlib import Path

folder = str(Path.cwd()) + '/test_data'
experiment = TRA(folder)
# Calculated Metrics from txt files in /home/niklas/PycharmProjects/trapy/tests/test_data
print(experiment.data)
## prints dictionary of group : bout-time DataFrame
print(experiment.metrics)
## prints DataFrame of TRA metrics (bouts per minute, idle time, AUC, etc.)
experiment.plot_data()
# Saved time_courses_t300.png to /home/niklas/PycharmProjects/trapy/tests/test_data
experiment.plot_data(seconds=100)
# Saved time_courses_t100.png to /home/niklas/PycharmProjects/trapy/tests/test_data
experiment.to_excel()
# Writing sheet "All Trials Metrics" to excel file.
# Writing sheet for time courses of group "group_2" to excel file.
# Writing sheet for time courses of group "group_1" to excel file.
# All done; see /home/niklas/PycharmProjects/trapy/tests/test_data/TapeResponseAssay.xlsx