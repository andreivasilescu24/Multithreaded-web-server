import os
import json
import csv
from numpy import sort
import pandas as pd

class DataIngestor:
    def __init__(self, csv_path: str):
        # TODO: Read csv from csv_path
        # self.data_rows = []
        # self.columns = {}
        
        # with open(csv_path, "r") as csv_file:
        #     reader = csv.reader(csv_file, delimiter=',')

        #     header_row = next(reader)
        #     for idx, column in enumerate(header_row):
        #         self.columns[column.strip()] = idx

        #     for row in reader:
        #         self.data_rows.append(row)
        self.table = pd.read_csv(csv_path)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    def states_mean(self, json_req):
        question = json_req['question']
        mean_vals = self.table[(self.table['Question'] == question) & (self.table['YearStart'] >= 2011) &
                                (self.table['YearEnd'] <= 2022)].groupby('LocationDesc')['Data_Value'].mean()
        mean_vals_dict = mean_vals.to_dict()
        return dict(sorted(mean_vals_dict.items(), key = lambda pair: pair[1]))
    
    def state_mean(self, json_req):
        question = json_req['question']
        state = json_req['state']
        mean_val = self.table[(self.table['Question'] == question) & (self.table['LocationDesc'] == state) &
                               (self.table['YearStart'] >= 2011) &
                                 (self.table['YearEnd'] <= 2022)]['Data_Value'].mean()
        return {state: mean_val}
    
    def best5(self, json_req):
        question = json_req['question']
        mean_vals = self.table[(self.table['Question'] == question) & (self.table['YearStart'] >= 2011) &
                                (self.table['YearEnd'] <= 2022)].groupby('LocationDesc')['Data_Value'].mean()
        
        if question in self.questions_best_is_min:
            return dict(sorted(mean_vals.to_dict().items(), key = lambda pair: pair[1])[:5])
        else:
            return dict(sorted(mean_vals.to_dict().items(), key = lambda pair: pair[1], reverse=True)[:5])
        
    def worst5(self, json_req):
        question = json_req['question']
        mean_vals = self.table[(self.table['Question'] == question) & (self.table['YearStart'] >= 2011) &
                                (self.table['YearEnd'] <= 2022)].groupby('LocationDesc')['Data_Value'].mean()
        if question in self.questions_best_is_min:
            return dict(sorted(mean_vals.to_dict().items(), key = lambda pair: pair[1], reverse=True)[:5])
        else:
            return dict(sorted(mean_vals.to_dict().items(), key = lambda pair: pair[1])[:5])
        
    def global_mean(self, json_req):
        question = json_req['question']
        mean_val = self.table[(self.table['Question'] == question) & (self.table['YearStart'] >= 2011) &
                              (self.table['YearEnd'] <= 2022)]['Data_Value'].mean()
        return {'global_mean' : mean_val}
    
    def diff_from_mean(self, json_req):
        global_mean_val = self.global_mean(json_req)['global_mean']
        states_mean = self.states_mean(json_req)

        diff_from_mean = {}
        for state, mean_val in states_mean.items():
            diff_from_mean[state] = global_mean_val - mean_val

        return dict(sorted(diff_from_mean.items(), key = lambda pair: pair[1], reverse = True))
    
    def state_diff_from_mean(self, json_req):
        global_mean_val = self.global_mean(json_req)['global_mean']
        state_mean = self.state_mean(json_req)
        return {json_req['state'] : global_mean_val - state_mean[json_req['state']]}
    
    # def mean_by_category(self, json_req):
    #     question = json_req['question']
    #     vals = self.table[self.table['Question'] == question]
    #     grouped_vals = vals.groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])['Stratification1'].mean()

    #     # Convert the grouped DataFrame to a dictionary with tuples as keys
    #     results_dict = {(row['LocationDesc'], row['StratificationCategory1'], row['Stratification1']): row['MeanValue'] for index, row in grouped_vals.iterrows()}

    #     # Print the dictionary
    #     print(results_dict)
    #     # for group_name, group_data in vals:
    #     #     print(f"Group: {group_name}")
    #     #     print(group_data)
    #     return None

    # def state_mean_by_category(self, json_req):
    #     pass