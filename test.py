import json
import pandas as pd
import utils as ut


message_dict = {}

pp = pd.read_csv('clean_phone_data_final.csv')

event_dict = json.loads('''{"type": "all", "top_n": 10}''')
top_n = event_dict.get('top_n', 10)

if event_dict.get('type', None) == 'all':        
    message_dict['type'] = 'return-all'

    message_dict['top'] = {col: '\n'.join(['Any'] + list(ut.get_top_words(pp[col].astype(str).to_list(), 10).keys())) for col in pp.columns}
else:
    message_dict['type'] = 'return-top'
    col = event_dict.get('type', None).split('-')[-1]

    message_dict['top'] = '\n'.join(['Any'] + list(ut.get_top_words(pp[col].astype(str).to_list(), 10).keys()))

message_dict['status'] = 'success'


print(json.dumps(message_dict))