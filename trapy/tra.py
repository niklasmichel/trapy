import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
        .metrics    - DataFrame of metrics per trial
        .data       - Dictionary of DataFrames of bout-time-data per group
    Methods:
        .to_excel() - writes metrics and time courses to
                      'TapeResponseAssay.xlsx'
    """

    def __init__(self, folder='/'):
        self.folder = folder
        self.trials = instantiate(self.folder)
        self.groups = set(sorted(set(trial.group for trial in self.trials)))
        self.dates = set(trial.date for trial in self.trials)
        self.mice = set(trial.mouse for trial in self.trials)
        self.metrics = trials_to_df(self.trials)
        self.data = timecourses_to_dfs(self)


    def plot_data(self, seconds=300):
        """Returns an array of plots of bout-time data and saves it in TRA.folder as png file."""
        # plt array of subfigures in 2 columns and (nr of groups + 1) rows:
        # - left: single bout-time-curves per group
        # - right: group average ± SD
        # - bottom row:
        #   - left: all group averages ± SD
        #   - right: all group averages ± SEM
        nrows = len(self.groups) + 1
        ncols = 2
        errorevery = int(np.log10(seconds))
        time = seconds + 1
        fig, axes = plt.subplots(nrows, ncols, figsize=(15, (nrows * 5)))
        fig.subplots_adjust(hspace=0.3)
        fig.suptitle('Bout-time-curves of trials and groups', fontsize=15)
        x = range(time)

        for ax, group in zip(axes.flatten()[:-2:2], self.groups):
            mice = [trial.mouse for trial in self.trials if trial.group == group]
            for mouse in mice:
                y = self.data[group][mouse][:time]
                ax.plot(x, y)
            ax.legend(mice, loc='upper left');
            ax.set(title=f'Time courses per mouse in {group}',
                   xlabel='Trial time (s)',
                   ylabel='Cumulative bouts');

        for ax, group in zip(axes.flatten()[1:-2:2], self.groups):
            y = self.data[group]['Mean'][:time]
            yerr = self.data[group]['SD(n-1)'][:time]
            ax.errorbar(x, y,
                        yerr=yerr,
                        errorevery=errorevery)
            ax.legend((group,), loc='upper left');
            ax.set(title='Averaged time course curve ± SD',
                   xlabel='Trial time (s)',
                   ylabel='Cumulative bouts');

        for group in self.groups:
            y = self.data[group]['Mean'][:time]
            yerr = self.data[group]['SD(n-1)'][:time]
            axes.flatten()[-2].errorbar(x, y,
                                        yerr=yerr,
                                        errorevery=errorevery)
            axes.flatten()[-2].legend(self.groups, loc='upper left');
            axes.flatten()[-2].set(title='Averaged time course curves ± SD',
                                   xlabel='Trial time (s)',
                                   ylabel='Cumulative bouts');
            yerr2 = self.data[group]['SD(n-1)'][:time] / np.sqrt(self.data[group]['n'][:time])
            axes.flatten()[-1].errorbar(x, y,
                                        yerr=yerr2,
                                        errorevery=errorevery)
            axes.flatten()[-1].legend(self.groups, loc='upper left');
            axes.flatten()[-1].set(title='Averaged time course curves ± SEM',
                                   xlabel='Trial time (s)',
                                   ylabel='Cumulative bouts');
        figname = f'time_courses_t{seconds}.png'
        fig.savefig(self.folder + '/' + figname)
        print(f'Saved {figname} to {self.folder}')
        return fig

    def plot_results(self):
        # plt array of (bar graphs?)
        # - total bouts means | total time means | bpm means
        # - success rates | idle time means | auc means
        pass

    def to_excel(self):
        """Crawls folder for txt files; instantiates them as Trial() objects,
        thereby analyzing various tape assay metrics;
        prints these metrics to 'TapeResponseAssay.xlsx'.
        Creates worksheets for all metrics and timecourse per group, respectively.
        """
        outputfile = os.path.join(self.folder, 'TapeResponseAssay.xlsx')
        writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')

        # Write each dataframe (all metrics, group timecourse) to a different worksheet.

        df_metrics = self.metrics
        df_metrics.to_excel(writer, sheet_name='All Trials Metrics', index=False)
        sys.stdout.write(f'Writing sheet "All Trials Metrics" to excel file.\n')

        for group in self.groups:
            df_timecourse = self.data[group]
            df_timecourse.to_excel(writer,
                                   sheet_name=str(group) + '_Time courses',
                                   index=True)
            sys.stdout.write(
                f'Writing sheet for time courses of group "{group}" to excel file.\n')

        writer.save()
        sys.stdout.write(f'All done; see {outputfile}')


def trials_to_df(trials):
    """Returns DataFrame of trial metrics."""
    group, mouse, date, success, total_bouts, total_time, idle_time, bpm, auc = [], [], [], [], [], [], [], [], []

    for trial in trials:
        group.append(trial.group)
        mouse.append(trial.mouse)
        date.append(trial.date)
        success.append(trial.success)
        total_bouts.append(trial.total_bouts)
        total_time.append(trial.total_time)
        idle_time.append(trial.idle_time)
        bpm.append(trial.bouts_per_minute)
        auc.append(trial.auc)

    df_metrics = pd.DataFrame({
        'Group': group,
        'Mouse': mouse,
        'Date': date,
        'Success': success,
        'Total bouts': total_bouts,
        'Total time': total_time,
        'Idle time': idle_time,
        'Bouts per minute': bpm,
        'AUC (Area under the trial time course curve)': auc
    })

    return df_metrics


def timecourses_to_dfs(experiment):
    tc_groups = dict()
    for group in experiment.groups:
        df_timecourse = pd.DataFrame({trial.mouse: trial.timecourse300 for trial in experiment.trials
                                      if trial.group == group})
        df_timecourse['Mean'] = df_timecourse[[trial.mouse for trial in experiment.trials
                                               if trial.group == group]].mean(axis=1)
        df_timecourse['SD(n-1)'] = df_timecourse[[trial.mouse for trial in experiment.trials
                                                  if trial.group == group]].std(axis=1, ddof=1)
        df_timecourse['n'] = df_timecourse[[trial.mouse for trial in experiment.trials
                                            if trial.group == group]].count(axis=1)
        cols = df_timecourse.columns.tolist()
        cols = cols[-3:] + cols[:-3]
        df_timecourse = df_timecourse[cols]
        tc_groups[group] = df_timecourse

    return tc_groups
