# TRApy - The Tape Response Assay Python Package for somatosensory research
by Niklas Michel, niklas.michel@gmail.com, https://www.linkedin.com/in/niklas-michel/
## Repository content
Python3 package to use time record txt-files produced with the Android app 
"Counter and Timer" by risinier 
(https://play.google.com/store/apps/details?id=com.risinier.counterandtimer)
to extract certain metrics, such as 
 - events per minute
 - area under the event-time-curve
 - no-event-time
 
 and produce a neat xlsx or csv files for subsequent statistical analysis.
 ## Repository structure
 ```
README.md
LICENSE.txt
setup.py
trapy/__init__.py
trapy/trapy.py
trapy/filehandler.py
tests/test.py
tests/TapeResponsAssay.xlsx
tests/all_trials_metrics.csv
tests/group_1_metrics.csv
tests/group_1_time_courses.csv
tests/group_2_metrics.csv
tests/group_2_time_courses.csv

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
Then, after installing this module locally,
use the following code to analyze all trials and create an excel file
for subsequent statistical analysis:
```python
import trapy

trapy.analyze_trials(folder, outputfile='TapeResponseAssay.xlsx')
```
Or, for creating csv files, use:
```python
import trapy

trapy.analyze_trials_csv(folder)
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
