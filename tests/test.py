from trapy import TRA
from pathlib import Path

folder = str(Path.cwd()) + '/test_data'
experiment = TRA(folder)
print(experiment.data)