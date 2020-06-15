from trapy import TRA
from pathlib import Path

folder = str(Path.cwd()) + '/demo_data'
experiment = TRA(folder)
# Calculated Metrics from txt files in /trapy/tests/demo_data

print(experiment.data)
## prints dictionary of group : bout-time DataFrame

print(experiment.metrics)
## prints DataFrame of TRA metrics (bouts per minute, idle time, AUC, etc.)

experiment.plot_data()
# Saved time_courses_t300.png to /trapy/tests/demo_data

experiment.plot_data(seconds=100)
# Saved time_courses_t100.png to /trapy/tests/demo_data

experiment.plot_results()
# AUC Group 1: n = 10, 14751.123214285715 ± 316.33616666025017 (SD)
# AUC Group 2: n = 9, 11700.694444444445 ± 580.1222640701194 (SD)
# AUC Group 3: n = 10, 11214.319246031746 ± 204.69887557751363 (SD)
# AUC Group 4: n = 10, 10186.444444444445 ± 409.2312525401201 (SD)
# Saved results.png to /trapy/tests/demo_data

experiment.to_excel()
# Writing sheet "All Trials Metrics" to excel file.
# Writing sheet for time courses of group "Group 1" to excel file.
# Writing sheet for time courses of group "Group 2" to excel file.
# Writing sheet for time courses of group "Group 3" to excel file.
# Writing sheet for time courses of group "Group 4" to excel file.
# All done; see /trapy/tests/demo_data/TapeResponseAssay.xlsx
