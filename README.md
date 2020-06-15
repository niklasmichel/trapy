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
 
 and produce figures and a neat .xlsx file for subsequent statistical analysis.
 ## Repository structure
 ```
README.md
LICENSE.txt
setup.py
trapy/__init__.py
trapy/tra.py
trapy/trial.py
tests/demo.py
tests/demo_data/TapeResponsAssay.xlsx
tests/demo_data/time_course_t100.png
tests/demo_data/time_course_t300.png
tests/demo_data/results.png
``` 
## Information
This improved tape response assay can quantify sensory-driven behaviour sensitively 
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
# Calculated Metrics from txt files in /trapy/tests/demo_data

print(experiment.data)
## prints dictionary with group : DataFrame of bout-time-data

print(experiment.metrics)
## prints DataFrame with relevant metrics per trial

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
## see figure below

experiment.to_excel()
# Writing sheet "All Trials Metrics" to excel file.
# Writing sheet for time courses of group "Group 1" to excel file.
# Writing sheet for time courses of group "Group 2" to excel file.
# Writing sheet for time courses of group "Group 3" to excel file.
# Writing sheet for time courses of group "Group 4" to excel file.
# All done; see /trapy/tests/demo_data/TapeResponseAssay.xlsx

```

![Bout-time plots created with trapy](https://github.com/niklasmichel/trapy/blob/master/tests/demo_data/results.png)

Future updates will add
 - TRA.plot_results(); shall create plots of relevant metrics 
 - background concerning the assay in research
 - methodological details
 - requirements.txt
 - docs/conf.py
 - error handling, e.g. for file naming issues
 - statistics functionality, if requested

\
Feel free to contact me about this package or the assay, see email at the top.
