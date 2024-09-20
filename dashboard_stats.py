import pandas as pd


class Dashboard:

    def __init__(self):
        pass

    @classmethod
    def get_suite_statistics(self, suite_list):
        suite_data_frame = pd.DataFrame.from_records(suite_list)
        suite_stats = {
            "Total" : (suite_data_frame.Name).count(),
            "Pass"  : (suite_data_frame.Status == 'PASS').sum(),
            "Fail"  : (suite_data_frame.Status == 'FAIL').sum(),
            "Skip"  : (suite_data_frame.Status == 'SKIP').sum(),
            "Time"  : (suite_data_frame.Time).sum(),
            "Min"  : (suite_data_frame.Time).min(),
            "Max"  : (suite_data_frame.Time).max(),
            "Avg"  : (suite_data_frame.Time).mean()
        }
        # print(suite_stats)
        return suite_stats
    
    @classmethod
    def get_test_statistics(self, test_list):
        test_data_frame = pd.DataFrame.from_records(test_list)
        # print(test_data_frame)
        test_stats = {
            "Total" : (test_data_frame.Status).count(),
            "Pass"  : (test_data_frame.Status == 'PASS').sum(),
            "Fail"  : (test_data_frame.Status == 'FAIL').sum(),
            "Skip"  : (test_data_frame.Status == 'SKIP').sum(),
            "Time"  : (test_data_frame.Time).sum(),
            "Min"  : (test_data_frame.Time).min(),
            "Max"  : (test_data_frame.Time).max(),
            "Avg"  : (test_data_frame.Time).mean()
        }
        # print(test_stats)
        return test_stats

    # Customised code for tags - Author : Shriman

    @classmethod
    def get_tag_statistics(self, tag_list):
        tag_data_frame = pd.DataFrame.from_records(tag_list)
        all_tag_stats = {}
        for tag in list(set(tag_data_frame['Tag Name'])):
            tempdf = tag_data_frame.loc[tag_data_frame['Tag Name'] == tag]
            tag_stats = {
                                "Total": (tempdf.Status).count(),
                                "Pass": (tempdf.Status == 'PASS').sum(),
                                "Fail": (tempdf.Status == 'FAIL').sum(),
                                "Skip": (tempdf.Status == 'SKIP').sum(),
                                "Time": (tempdf.Time).sum(),
                                "Min": (tempdf.Time).min(),
                                "Max": (tempdf.Time).max(),
                                "Avg": (tempdf.Time).mean()
                            }
            all_tag_stats[tag] = tag_stats

        # Tag statatistics for all tags
        agg_functions = {'Tag Name':'first','Suite Name': lambda x: x._append(x), 'Test Name': lambda x: x._append(x), 'Test Id': lambda x: x._append(x), 'Status': lambda x: x._append(x), 'Time':'sum'}
        tag_data_frame = tag_data_frame.groupby('Tag Name' , as_index=False).aggregate(agg_functions)
        for i,row in tag_data_frame.iterrows():
            tag_data_frame.at[i, 'Suite Name'] = list(set(row['Suite Name']))
            tag_data_frame.at[i, 'Test Name'] = list(set(row['Test Name']))
            tag_data_frame.at[i, 'Test Id'] = zip(list(set(row['Test Id'])),tag_data_frame['Test Name'])
            if 'FAIL' in row['Status']:
                 tag_data_frame.at[i,'Status']= 'FAIL'
            elif 'SKIP' in row['Status']:
                tag_data_frame.at[i,'Status'] = 'SKIP'
            else:
               tag_data_frame.at[i,'Status'] = 'PASS'

        tag_stats = {
            "Total" : (tag_data_frame.Status).count(),
            "Pass"  : (tag_data_frame.Status == 'PASS').sum(),
            "Fail"  : (tag_data_frame.Status == 'FAIL').sum(),
            "Skip"  : (tag_data_frame.Status == 'SKIP').sum(),
            "Time": (tag_data_frame.Time).sum(),
            "Min": (tag_data_frame.Time).min(),
            "Max": (tag_data_frame.Time).max(),
            "Avg": (tag_data_frame.Time).mean()
        }
        all_tag_stats['All'] = tag_stats
        tag_data_frame = tag_data_frame.to_dict('records')
        
        return all_tag_stats,tag_data_frame

    @classmethod
    def get_keyword_statistics(self, kw_list):
        kw_data_frame = pd.DataFrame.from_records(kw_list)
        if not kw_data_frame.empty:
            kw_stats = {
                "Total" : (kw_data_frame.Status).count(),
                "Pass"  : (kw_data_frame.Status == 'PASS').sum(),
                "Fail"  : (kw_data_frame.Status == 'FAIL').sum(),
                "Skip"  : (kw_data_frame.Status == 'SKIP').sum()
            }
        else:
            kw_stats = {
                "Total" : 0,
                "Pass"  : 0,
                "Fail"  : 0,
                "Skip"  : 0,
            }
        return kw_stats
    
    def group_error_messages(self, test_list):
        test_data_frame = pd.DataFrame.from_records(test_list)
        return (test_data_frame.groupby("Message").agg(times = ("Status", "count")).head(6).reset_index()).sort_values(by = ['times'], ascending = [False], ignore_index=True)
    
    def suite_error_statistics(self, suite_list):
        suite_data_frame = pd.DataFrame.from_records(suite_list)
        required_data_frame = pd.DataFrame(suite_data_frame, columns = ['Name', 'Total', 'Fail'])
        required_data_frame['percent'] = (required_data_frame['Fail'] / required_data_frame['Total'])*100
        # print(required_data_frame)
        return required_data_frame.sort_values(by = ['Fail'], ascending = [False], ignore_index=True).head(10).reset_index()
