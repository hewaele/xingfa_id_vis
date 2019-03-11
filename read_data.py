import pandas as pd

data = pd.read_excel('F:/hewaele/108/模具id检测项目/2019-1-12-实际预测结果/csv文件/pre_data.xlsx')
print(data.info())
pre_result = pd.DataFrame({'img_name':data['img_name'],
                           'pre_id':data['pre_id'],
                           'real_id':data['real_id'],
                           'omit_num':data['omit_num'],
                           'error_num':data['error_num'],
                           'extra_num':data['extra_num']})

pre_result['real_id'].fillna(pre_result['pre_id'], inplace=True)
print(pre_result)