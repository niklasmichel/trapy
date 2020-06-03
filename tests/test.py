from trapy import TRA
from pathlib import Path

folder = str(Path.cwd()) + '/test_data'
experiment = TRA(folder)
experiment.to_excel()

# /home/niklas/anaconda3/bin/python /home/niklas/PycharmProjects/trapy/tests/test.py
# Calculated Metrics from txt files in /home/niklas/PycharmProjects/trapy/tests/test_data
# Analyzing txt files in given folder...
# Writing sheet "All Trials Metrics" to /home/niklas/PycharmProjects/trapy/tests/test_data/TapeResponseAssay.xlsx.
# Writing sheet for time courses of group "group_1" to /home/niklas/PycharmProjects/trapy/tests/test_data/TapeResponseAssay.xlsx.
# Writing sheet for time courses of group "group_2" to /home/niklas/PycharmProjects/trapy/tests/test_data/TapeResponseAssay.xlsx.
# All done; see /home/niklas/PycharmProjects/trapy/tests/test_data/TapeResponseAssay.xlsx
# Process finished with exit code 0