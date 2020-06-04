# TRApy - The Tape Response Assay Python Module for Somatosensory Research
by Niklas Michel, niklas.michel@gmail.com, https://www.linkedin.com/in/niklas-michel/
## Repository content
Python3 module to use time record txt-files produced with the Android app 
"Counter and Timer" by risinier 
(https://play.google.com/store/apps/details?id=com.risinier.counterandtimer)
to extract certain metrics, such as 
 - events per minute
 - area under the event-time-curve
 - no-event-time
 
 and produce a neat .xlsx file for subsequent statistical analysis.
 ## Repository structure
 ```
README.md
LICENSE.txt
setup.py
trapy/__init__.py
trapy/tra.py
trapy/trial.py
tests/test.py
tests/test_data/TapeResponsAssay.xlsx
``` 
## Information
This improved tape response assay can quantify sensory-driven behaviour 
when researching hairy skin mechanosensation in rodents.\
\
Perform the assay and use the free Android app 
"Counter and Timer" by risinier 
(https://play.google.com/store/apps/details?id=com.risinier.counterandtimer) to
count tape-directed bouts. Make sure to add one last time stamp after 5 minutes, if the animal
did not manage to get the tape off after that maximal trial time. The code will recognize this as a non-successful
trial.\
\
Safe the records as 
"yymmddaa*g.txt" in one folder, where\
yy = year, e.g. "20"\
mm = month, e.g. "06"\
dd = day, e.g. "01"\
aa = animal number, e.g. "01"\
*g = group name, e.g. "WT", "treated" or "C57_injected_4_weeks"\
\
Install the trapy module by running the following in your terminal:
```
pip install git+https://github.com/niklasmichel/trapy
```
Then, use the following code to analyze all trials, inspect the data and results
and create an excel file for subsequent statistical analysis:
```python
from trapy import TRA

experiment = TRA(folder)
# Calculated Metrics from txt files in /home/niklas/PycharmProjects/trapy/tests/test_data
print(experiment.data)
# prints dictionary with group : DataFrame of bout-time-data
print(experiment.metrics)
# prints DataFrame with relevant metrics per trial
experiment.to_excel()
# Writing sheet "All Trials Metrics" to excel file.
# Writing sheet for time courses of group "group_1" to excel file.
# Writing sheet for time courses of group "group_2" to excel file.
# All done; see /home/niklas/PycharmProjects/trapy/tests/test_data/TapeResponseAssay.xlsx
```

Future updates will add 
 - background concerning the assay in research
 - methodological details
 - requirements.txt
 - docs/conf.py
 - error handling, e.g. for file naming issues
 - statistics or graphing functionality, if requested

\
Feel free to contact me about this package or the assay, see email at the top.
