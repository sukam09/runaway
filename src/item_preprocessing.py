import pandas as pd
import requests
from tqdm import tqdm
import json


with open('../item.json', 'r') as item_data:
    item = json.load(item_data)

item_key = list(item['data'].keys())
item = item['data']

for i in range(len(item_key)):
    print('%s: %s' % (item_key[i], item[item_key[i]]['name']))
