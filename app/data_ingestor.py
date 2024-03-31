import os
import json
import csv
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
        mean_vals = self.table[(self.table['Question'] == question) & (self.table['YearStart'] >= 2011) & (self.table['YearEnd'] <= 2022)].groupby('LocationDesc')['Data_Value'].mean()
        mean_vals_dict = mean_vals.to_dict()
        # if question in self.questions_best_is_min:
        return dict(sorted(mean_vals_dict.items(), key = lambda pair: pair[1]))
        # else:
        #     return dict(sorted(mean_vals_dict.items(), key = lambda pair: pair[1], reverse=True))