import requests


summoner_name = 'Koori'
api_key_file = open('../api_key.txt', 'r')
API_KEY = api_key_file.read()

summoner_api = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + API_KEY
summoner = requests.get(summoner_api).json()
print(summoner)

test_dict_1 = {'status': {'message': 'Rate limit exceeded', 'status_code': 429}}
test_dict_2 = {'id': 'HcnBbg3K-14v0AHXRC5GIU7EHjKSiCd0bkfUKY0E7ZUMrA', 'accountId': 'JdFekB3s0X-Ij6d8sXwGcPrGQ2Qi1trlaTxhKkT5iyYW', 'puuid': 'c6ODulnPAhN9yC2qDiCnh4wkRK-B7y9OpkuNUq_qCasHeoSyIdnGhA6Z5bDtfK7-iEMf0KU-EiIfvw', 'name': 'Koori', 'profileIconId': 4661, 'revisionDate': 1603451852000, 'summonerLevel': 287}
# print('yes') if 'status' in test_dict_1 else print('no')
# print('yes') if 'status' in test_dict_2 else print('no')

print('status' not in test_dict_1)
print('status' not in test_dict_2)

# while True:
#     summoner_api = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + API_KEY
#     summoner = requests.get(summoner_api).json()
#     print(summoner)