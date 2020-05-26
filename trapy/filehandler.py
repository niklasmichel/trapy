import os
import sys
import pandas as pd
from .trapy import Trial

def txt_file_path_list(path_to_folder='/'):
    """Returns sorted list of paths to ~.txt files found in specified folder."""
    filenames = os.listdir(path_to_folder)
    txt_files = []
    for file in filenames:
        if file[-3:] == 'txt':
            txt_files.append(os.path.join(path_to_folder, file))
        else:
            pass
    txt_files.sort()
    return txt_files

def instantiate(folder):
    """Crawls folder for text files and makes them instances of the Trial() Class.
    Returns a list of the created objects
    """
    trials = [Trial(path_to_trial) for path_to_trial in txt_file_path_list(folder)]
    sys.stdout.write('Calculated Metrics from txt files in ' + folder + '\n')
    return trials


def analyze_trials(folder, outputfile='TapeResponseAssay.xlsx'):
    """Crawls folder for txt files; instantiates them as Trial() objects,
    thereby analyzing various tape assay metrics;
    prints these metrics to an excel-file, specified with outputfile='TapeResponseAssay.xlsx'.
    Creates worksheets for all metrics, metrics per group and timecourse per group, respectively.
    """
    sys.stdout.write('Analyzing txt files in given folder...\n')
    trials = instantiate(folder)
    groups = {trial.group for trial in trials}
    writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')

    # Write each dataframe (all metrics, group metrics, group timecourse) to a different worksheet.

    df_metrics_all = pd.DataFrame({
        'Group': [trial.group for trial in trials],
        'Mouse': [trial.mouse for trial in trials],
        'Date': [trial.date for trial in trials],
        'Success': [trial.success for trial in trials],
        'Total bouts': [trial.total_bouts for trial in trials],
        'Total time': [trial.total_time for trial in trials],
        'Idle time': [trial.idle_time for trial in trials],
        'Bouts per minute': [trial.bouts_per_minute for trial in trials],
        # 'TIBI (touch induced behaviour index, BPM * (5 minutes - idle time))': [trial.tibi for trial in trials],
        'AUC (Area under the trial time course curve)': [trial.auc for trial in trials]
    })
    df_metrics_all.to_excel(writer, sheet_name='All Trials Metrics', index=False)
    sys.stdout.write('Writing sheet "All Trials Metrics" to {0}.\n'.format(outputfile))

    for group in groups:
        df_metrics = pd.DataFrame({
            'Group': [trial.group for trial in trials if trial.group == group],
            'Mouse': [trial.mouse for trial in trials if trial.group == group],
            'Date': [trial.date for trial in trials if trial.group == group],
            'Success': [trial.success for trial in trials if trial.group == group],
            'Total bouts': [trial.total_bouts for trial in trials if trial.group == group],
            'Total time': [trial.total_time for trial in trials if trial.group == group],
            'Idle time': [trial.idle_time for trial in trials if trial.group == group],
            'Bouts per minute': [trial.bouts_per_minute for trial in trials if trial.group == group],
            # 'TIBI (touch induced behaviour index, BPM * (5 minutes - idle time))': [trial.tibi for trial in trials if
            #                                                                        trial.group == group],
            'AUC (Area under the trial time course curve)': [trial.auc for trial in trials if trial.group == group]
        })
        df_metrics.to_excel(writer, sheet_name=str(group) + '_Metrics', index=False)
        sys.stdout.write('Writing sheet for metrics of group "{0}" to {1}.\n'.format(group, outputfile))

        df_timecourse = pd.DataFrame({trial.mouse: trial.timecourse300 for trial in trials if trial.group == group})
        df_timecourse['Mean'] = df_timecourse[[trial.mouse for trial in trials if trial.group == group]].mean(axis=1)
        df_timecourse['SD(n-1)'] = df_timecourse[[trial.mouse for trial in trials if trial.group == group]].std(axis=1, ddof=1)
        df_timecourse['n'] = df_timecourse[[trial.mouse for trial in trials if trial.group == group]].count(axis=1)
        cols = df_timecourse.columns.tolist()
        cols = cols[-3:] + cols[:-3]
        df_timecourse = df_timecourse[cols]
        df_timecourse.to_excel(writer,
                     sheet_name=str(group) + '_Time courses',
                     index=True)
        sys.stdout.write(
            'Writing sheet for time courses of group "{0}" to {1}.\n'.format(group, outputfile))

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    sys.stdout.write('All done; see {0}/{1}'.format(os.getcwd(), outputfile))


def analyze_trials_csv(folder):
    """Crawls folder for txt files; instantiates them as Trial() objects, thereby analyzing various tape assay metrics;
    prints these metrics to csv files.
    """
    sys.stdout.write('Analyzing txt files in given folder...\n')
    trials = instantiate(folder)
    groups = {trial.group for trial in trials}
    df_metrics_all = pd.DataFrame({
        'Group': [trial.group for trial in trials],
        'Mouse': [trial.mouse for trial in trials],
        'Date': [trial.date for trial in trials],
        'Success': [trial.success for trial in trials],
        'Total bouts': [trial.total_bouts for trial in trials],
        'Total time': [trial.total_time for trial in trials],
        'Idle time': [trial.idle_time for trial in trials],
        'Bouts per minute': [trial.bouts_per_minute for trial in trials],
        'TIBI (touch induced behaviour index, BPM * (5 minutes - idle time))': [trial.tibi for trial in trials],
        'AUC (Area under the trial time course curve)': [trial.auc for trial in trials]
    })
    outputfile = 'all_trials_metrics.csv'
    df_metrics_all.to_csv(outputfile, index=False, sep=';', decimal=',')
    sys.stdout.write('Writing ' + outputfile + '\n')

    for group in groups:
        df_metrics = pd.DataFrame({
            'Group': [trial.group for trial in trials if trial.group == group],
            'Mouse': [trial.mouse for trial in trials if trial.group == group],
            'Date': [trial.date for trial in trials if trial.group == group],
            'Success': [trial.success for trial in trials if trial.group == group],
            'Total bouts': [trial.total_bouts for trial in trials if trial.group == group],
            'Total time': [trial.total_time for trial in trials if trial.group == group],
            'Idle time': [trial.idle_time for trial in trials if trial.group == group],
            'Bouts per minute': [trial.bouts_per_minute for trial in trials if trial.group == group],
            'TIBI (touch induced behaviour index, BPM * (5 minutes - idle time))': [trial.tibi for trial in trials if
                                                                                    trial.group == group],
            'AUC (Area under the trial time course curve)': [trial.auc for trial in trials if trial.group == group]
        })
        outputfile = group + '_metrics.csv'
        df_metrics.to_csv(outputfile, index=False, sep=';', decimal=',')
        sys.stdout.write('Writing ' + outputfile + '\n')

        df_timecourse = pd.DataFrame({trial.mouse: trial.timecourse300 for trial in trials if trial.group == group})
        df_timecourse['Mean'] = df_timecourse[[trial.mouse for trial in trials if trial.group == group]].mean(axis=1)
        df_timecourse['SD(n-1)'] = df_timecourse[[trial.mouse for trial in trials if trial.group == group]].std(axis=1, ddof=1)
        df_timecourse['n'] = df_timecourse[[trial.mouse for trial in trials if trial.group == group]].count(axis=1)
        cols = df_timecourse.columns.tolist()
        cols = cols[-3:] + cols[:-3]
        df_timecourse = df_timecourse[cols]
        outputfile = group + '_time_courses.csv'
        df_timecourse.to_csv(outputfile, index=True, sep=';', decimal=',')
        sys.stdout.write('Writing ' + outputfile + '\n')

    sys.stdout.write('All done; see csv files in {0}'.format(os.getcwd()))




