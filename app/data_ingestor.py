import pandas as pd

class DataIngestor:
    def __init__(self, csv_path: str):
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
    
    def mean_by_category(self, json_req):
        question = json_req['question']
        filtered_vals = self.table[self.table['Question'] == question]
        grouped_vals = filtered_vals.groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])['Data_Value'].mean()
        grouped_vals_dict = {str(key): value for key, value in grouped_vals.to_dict().items()}
        return dict(sorted(grouped_vals_dict.items(), key = lambda pair: pair[0][0]))


    def state_mean_by_category(self, json_req):
        question = json_req['question']
        state = json_req['state']
        filtered_vals = self.table[(self.table['Question'] == question) & (self.table['LocationDesc'] == state)]
        grouped_vals = filtered_vals.groupby(['StratificationCategory1', 'Stratification1'])['Data_Value'].mean()
        grouped_vals_dict = {str(key): value for key, value in grouped_vals.to_dict().items()}
        sorted_grouped_vals = dict(sorted(grouped_vals_dict.items(), key = lambda pair: pair[0][0]))
        return {state: sorted_grouped_vals}
