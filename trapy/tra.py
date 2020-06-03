import os
import sys
import pandas as pd
from .trial import Trial


def instantiate(folder):
    """Crawls folder for text files and makes them instances of the Trial() Class.
    Returns a list of the created objects
    """
    trials = [Trial(path_to_trial) for path_to_trial in txt_file_path_list(folder)]
    sys.stdout.write('Calculated Metrics from txt files in ' + folder + '\n')
    return trials


def txt_file_path_list(folder):
    """Returns sorted list of paths to ~.txt files found in specified folder."""
    filenames = os.listdir(folder)
    txt_files = []
    for file in filenames:
        if file[-3:] == 'txt':
            txt_files.append(os.path.join(folder, file))
        else:
            pass
    txt_files.sort()
    return txt_files

class TRA:
    """Tape Response Assay class. Specify path to txt files when initiating.
    Attributes:
        .folder     - specified path
        .trials     - list of trial objects
        .groups     - set of experimental groups
        .dates      - set of dates of trials
        .mice       - set of mouse numbers
    Methods:
        .to_excel() - writes metrics and time courses to
                      'TapeResponseAssay.xlsx'
    """

    def __init__(self, folder='/'):
        self.folder = folder
        self.trials = instantiate(self.folder)
        self.groups = set(trial.group for trial in self.trials)
        self.dates = set(trial.date for trial in self.trials)
        self.mice = set(trial.mouse for trial in self.trials)



    def to_excel(self):
        """Crawls folder for txt files; instantiates them as Trial() objects,
        thereby analyzing various tape assay metrics;
        prints these metrics to 'TapeResponseAssay.xlsx'.
        Creates worksheets for all metrics and timecourse per group, respectively.
        """
        sys.stdout.write('Analyzing txt files in given folder...\n')
        # trials = instantiate(folder)
        # groups = {trial.group for trial in trials}
        outputfile = os.path.join(self.folder, 'TapeResponseAssay.xlsx')
        writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')

        # Write each dataframe (all metrics, group metrics, group timecourse) to a different worksheet.

        df_metrics_all = pd.DataFrame({
            'Group': [trial.group for trial in self.trials],
            'Mouse': [trial.mouse for trial in self.trials],
            'Date': [trial.date for trial in self.trials],
            'Success': [trial.success for trial in self.trials],
            'Total bouts': [trial.total_bouts for trial in self.trials],
            'Total time': [trial.total_time for trial in self.trials],
            'Idle time': [trial.idle_time for trial in self.trials],
            'Bouts per minute': [trial.bouts_per_minute for trial in self.trials],
            # 'TIBI (touch induced behaviour index, BPM * (5 minutes - idle time))': [trial.tibi for trial in trials],
            'AUC (Area under the trial time course curve)': [trial.auc for trial in self.trials]
        })
        df_metrics_all.to_excel(writer, sheet_name='All Trials Metrics', index=False)
        sys.stdout.write(f'Writing sheet "All Trials Metrics" to {outputfile}.\n')

        for group in self.groups:
            # df_metrics = pd.DataFrame({
            #     'Group': [trial.group for trial in self.trials if trial.group == group],
            #     'Mouse': [trial.mouse for trial in self.trials if trial.group == group],
            #     'Date': [trial.date for trial in self.trials if trial.group == group],
            #     'Success': [trial.success for trial in self.trials if trial.group == group],
            #     'Total bouts': [trial.total_bouts for trial in self.trials if trial.group == group],
            #     'Total time': [trial.total_time for trial in self.trials if trial.group == group],
            #     'Idle time': [trial.idle_time for trial in self.trials if trial.group == group],
            #     'Bouts per minute': [trial.bouts_per_minute for trial in self.trials if trial.group == group],
            #     # 'TIBI (touch induced behaviour index, BPM * (5 minutes - idle time))': [trial.tibi for trial in trials if
            #     #                                                                        trial.group == group],
            #     'AUC (Area under the trial time course curve)': [trial.auc for trial in self.trials if
            #                                                      trial.group == group]
            # })
            # df_metrics.to_excel(writer, sheet_name=str(group) + '_Metrics', index=False)
            # sys.stdout.write('Writing sheet for metrics of group "{0}" to {1}.\n'.format(group, outputfile))

            df_timecourse = pd.DataFrame({trial.mouse: trial.timecourse300 for trial in self.trials
                                          if trial.group == group})
            df_timecourse['Mean'] = df_timecourse[[trial.mouse for trial in self.trials
                                                   if trial.group == group]].mean(axis=1)
            df_timecourse['SD(n-1)'] = df_timecourse[[trial.mouse for trial in self.trials
                                                      if trial.group == group]].std(axis=1, ddof=1)
            df_timecourse['n'] = df_timecourse[[trial.mouse for trial in self.trials
                                                if trial.group == group]].count(axis=1)
            cols = df_timecourse.columns.tolist()
            cols = cols[-3:] + cols[:-3]
            df_timecourse = df_timecourse[cols]
            df_timecourse.to_excel(writer,
                                   sheet_name=str(group) + '_Time courses',
                                   index=True)
            sys.stdout.write(
                f'Writing sheet for time courses of group "{group}" to {outputfile}.\n')

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        sys.stdout.write(f'All done; see {outputfile}')
