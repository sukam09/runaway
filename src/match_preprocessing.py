import pandas as pd
import requests
from tqdm import tqdm
from operator import itemgetter
import time

from data_set import summoner_spell, champion, item, rune


# API key
api_key_file = open('../api_key.txt', 'r')
API_KEY = api_key_file.read()

# Number of recent matches (Default: 20)
MATCHES = 20
SEASON = 2020

print('Runaway')
print('(c) 2020 Seungwon Lee. All rights reserved.')
print('리그 오브 레전드 닷지 추천 시스템 Runaway에 오신 것을 환영합니다.')

summoner_name = input('\n소환사명을 입력하십시오: ')
print()

# League match data structure
league_match_id = []
league_match_champion = []
league_match_win = []

league_match_info = []
league_match_data = []

summoner_api = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + API_KEY
summoner = requests.get(summoner_api).json()

try:
    account_id = summoner['accountId']
    summoner_Id = summoner['id']
except KeyError:
    print('\nAPI 요청 제한 횟수를 초과하여 대기 중입니다...')
    time.sleep(120)
    summoner = requests.get(summoner_api).json()
    account_id = summoner['accountId']
    summoner_Id = summoner['id']

account_id = summoner['accountId']
summoner_id = summoner['id']

league_api = 'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summoner_id + '?api_key=' + API_KEY
league = requests.get(league_api).json()

# Calculate solo rank games, wins, losses, win rate
if len(league) == 1:
    league_win = league[0]['wins']
    league_loss = league[0]['losses']
else:
    if league[0]['queueType'] == 'RANKED_SOLO_5x5':
        league_win = league[0]['wins']
        league_loss = league[0]['losses']
    else:
        league_win = league[1]['wins']
        league_loss = league[1]['losses']

league_game = league_win + league_loss
league_win_rate = league_win / league_game * 100

# Count played champions
count = 0

for match_idx in tqdm(range(league_game // 100 + 1), desc='플레이한 챔피언 집계중...'):
    begin_idx = 100 * match_idx
    matchlist_api = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account_id + '?queue=420&beginIndex=' + str(begin_idx) + '&api_key=' + API_KEY
    matchlist = requests.get(matchlist_api).json()['matches']
    for matchlist_idx in range(100):
        if count >= league_game:
            break
        else:
            league_match_id.append(matchlist[matchlist_idx]['gameId'])
            league_match_champion.append(matchlist[matchlist_idx]['champion'])
            count += 1

# Generate league match data set
for match_idx in tqdm(range(league_game), desc='시즌 데이터 셋 구축중...'):
    match_api = 'https://kr.api.riotgames.com/lol/match/v4/matches/' + str(league_match_id[match_idx]) + '?api_key=' + API_KEY
    match = requests.get(match_api).json()

    try:
        game_duration = match['gameDuration']
        match_team_info = match['participants']
    except KeyError:
        print('\nAPI 요청 제한 횟수를 초과하여 대기 중입니다...')
        time.sleep(120)
        match = requests.get(match_api).json()
        game_duration = match['gameDuration']
        match_team_info = match['participants']

    # Check player's team
    for participant_idx in range(10):
        if match_team_info[participant_idx]['championId'] == league_match_champion[match_idx]:
            match_info = match_team_info[participant_idx]
            if participant_idx < 5:
                team = 'blue'
            else:
                team = 'red'
            break

    spell1 = match_info['spell1Id']
    spell2 = match_info['spell2Id']
    stat = match_info['stats']

    league_match_info_row = []
    league_match_data_row = []

    # Champion
    league_match_info_row.append(champion[league_match_champion[match_idx]])
    league_match_data_row.append(league_match_champion[match_idx])

    # Win
    if game_duration <= 300:
        # Invalid matches
        # league_match_info_row.append('다시하기')
        # league_match_data_row.append(-1)
        league_match_win.append(-1)
        
        # For test
        # print('다시하기: %s' % league_match_id[match_idx])

        # Go to next match
        continue
    elif stat['win']:
        league_match_info_row.append('승리')
        league_match_data_row.append(1)
        league_match_win.append(1)
    else:
        league_match_info_row.append('패배')
        league_match_data_row.append(0)
        league_match_win.append(0)

    # Game duration
    league_match_info_row.append('%s분 %s초' % (game_duration // 60, game_duration % 60))
    league_match_data_row.append(game_duration)

    # Summoner spell
    league_match_info_row.append(summoner_spell[spell1])
    league_match_info_row.append(summoner_spell[spell2])
    league_match_data_row.append(spell1)
    league_match_data_row.append(spell2)

    # Runes
    league_match_info_row.append(rune[stat['perk0']])
    league_match_info_row.append(rune[stat['perkSubStyle']])
    league_match_data_row.append(stat['perk0'])
    league_match_data_row.append(stat['perkSubStyle'])

    # KDA
    kill = int(stat['kills'])
    death = int(stat['deaths'])
    assist = int(stat['assists'])

    league_match_info_row.append('%d/%d/%d' % (kill, death, assist))
    league_match_data_row.append(kill)
    league_match_data_row.append(death)
    league_match_data_row.append(assist)

    if death == 0:
        kda = (kill + assist) * 1.2
        league_match_info_row.append('Perfect')
        league_match_data_row.append('%.2f' % kda)
    else:
        kda = (kill + assist) / death
        league_match_info_row.append('%.2f' % kda)
        league_match_data_row.append('%.2f' % kda)
    
    # Level and CS
    level = int(stat['champLevel'])
    cs = int(stat['totalMinionsKilled'])
    cspm = cs / (game_duration / 60)

    league_match_info_row.append(level)
    league_match_info_row.append(cs)
    league_match_info_row.append('%.1f' % cspm)
    league_match_data_row.append(level)
    league_match_data_row.append(cs)
    league_match_data_row.append('%.1f' % cspm)

    # Kill participation
    team_score = 0
    if team == 'blue':
        for idx in range(5):
            team_score += match_team_info[idx]['stats']['kills']
    else:
        for idx in range(5, 10):
            team_score += match_team_info[idx]['stats']['kills']
    
    if team_score == 0:
        kp = 0
    else:
        kp = (kill + assist) / team_score * 100

    league_match_info_row.append('%.0f%%' % kp)
    league_match_data_row.append('%.0f' % kp)

    # Items
    league_match_info_row.append(item[stat['item0']])
    league_match_info_row.append(item[stat['item1']])
    league_match_info_row.append(item[stat['item2']])
    league_match_info_row.append(item[stat['item3']])
    league_match_info_row.append(item[stat['item4']])
    league_match_info_row.append(item[stat['item5']])
    league_match_data_row.append(stat['item0'])
    league_match_data_row.append(stat['item1'])
    league_match_data_row.append(stat['item2'])
    league_match_data_row.append(stat['item3'])
    league_match_data_row.append(stat['item4'])
    league_match_data_row.append(stat['item5'])

    league_match_info.append(league_match_info_row)
    league_match_data.append(league_match_data_row)

# Copy to recent matches
recent_match_info = league_match_info[:MATCHES]
recent_match_data = league_match_data[:MATCHES]
recent_match_win = league_match_win[:MATCHES]
recent_match_champion = league_match_champion[:MATCHES]

league_match_info_df = pd.DataFrame(league_match_info,
    columns=[
        '챔피언',
        '게임 결과',
        '게임 시간',
        '소환사 주문1',
        '소환사 주문2',
        '메인 룬',
        '보조 룬',
        'KDA',
        '평점',
        '레벨',
        'CS',
        '분당 CS',
        '킬관여',
        '아이템1',
        '아이템2',
        '아이템3',
        '아이템4',
        '아이템5',
        '아이템6'
    ]
)

league_match_data_df = pd.DataFrame(league_match_data,
    columns=[
        'champion',
        'win',
        'time',
        'spell1',
        'spell2',
        'rune1',
        'rune2',
        'kill',
        'death',
        'assist',
        'kda',
        'lv',
        'cs',
        'cspm',
        'kp',
        'item1',
        'item2',
        'item3',
        'item4',
        'item5',
        'item6'
    ]
)

recent_match_info_df = pd.DataFrame(recent_match_info,
    columns=[
        '챔피언',
        '게임 결과',
        '게임 시간',
        '소환사 주문1',
        '소환사 주문2',
        '메인 룬',
        '보조 룬',
        'KDA',
        '평점',
        '레벨',
        'CS',
        '분당 CS',
        '킬관여',
        '아이템1',
        '아이템2',
        '아이템3',
        '아이템4',
        '아이템5',
        '아이템6'
    ]
)

recent_match_data_df = pd.DataFrame(recent_match_data,
    columns=[
        'champion',
        'win',
        'time',
        'spell1',
        'spell2',
        'rune1',
        'rune2',
        'kill',
        'death',
        'assist',
        'kda',
        'lv',
        'cs',
        'cspm',
        'kp',
        'item1',
        'item2',
        'item3',
        'item4',
        'item5',
        'item6'
    ]
)

# Save to csv files
league_match_info_df.to_csv('./data/league_match_info.csv')
league_match_data_df.to_csv('./data/league_match_data.csv')
recent_match_info_df.to_csv('./data/recent_match_info.csv')
recent_match_data_df.to_csv('./data/recent_match_data.csv')

# Count league match champions
league_match_champion_checker = {}

for idx in range(len(league_match_champion)):
    # If the match is valid
    if league_match_win[idx] != -1:
        if league_match_champion[idx] in league_match_champion_checker:
            league_match_champion_checker[league_match_champion[idx]][0] += 1
            if league_match_win[idx] == 1:
                league_match_champion_checker[league_match_champion[idx]][1] += 1
            else:
                league_match_champion_checker[league_match_champion[idx]][2] += 1
        else:
            if league_match_win[idx] == 1:
                league_match_champion_checker[league_match_champion[idx]] = [1, 1, 0]
            else:
                league_match_champion_checker[league_match_champion[idx]] = [1, 0, 1]

league_match_champion_sorted = sorted(league_match_champion_checker.items(), key=itemgetter(1), reverse=True)

# Count recent match champions
recent_match_champion_checker = {}

for idx in range(len(recent_match_champion)):
    # If the match is valid
    if recent_match_win[idx] != -1:
        if recent_match_champion[idx] in recent_match_champion_checker:
            recent_match_champion_checker[recent_match_champion[idx]][0] += 1
            if recent_match_win[idx] == 1:
                recent_match_champion_checker[recent_match_champion[idx]][1] += 1
            else:
                recent_match_champion_checker[recent_match_champion[idx]][2] += 1
        else:
            recent_match_champion_checker[recent_match_champion[idx]] = [1, 0, 0]
            if recent_match_win[idx] == 1:
                recent_match_champion_checker[recent_match_champion[idx]][1] += 1
            else:
                recent_match_champion_checker[recent_match_champion[idx]][2] += 1

recent_match_champion_sorted = sorted(recent_match_champion_checker.items(), key=itemgetter(1), reverse=True)

# Results
print('\n===================================')
print('개인/2인 랭크 게임(%s시즌 전체)' % SEASON)
print('===================================')
print('총 %s게임 %s승 %s패 승률 %.0f%%' % (league_game, league_win, league_loss, league_win_rate))
print('-----------------------------------')

for item in league_match_champion_sorted:
    game = item[1][0]
    win = item[1][1]
    loss = item[1][2]
    win_rate = win / game * 100
    print('%s %d게임 %d승 %d패 승률 %.0f%% ' % (champion[item[0]], game, win, loss, win_rate))

game = len(recent_match_win)
win = recent_match_win.count(1)
loss = recent_match_win.count(0)
win_rate = win / game * 100

print('\n===================================')
print('개인/2인 랭크 게임(최근 %s게임)' % MATCHES)
print('===================================')
print('총 %s게임 %s승 %s패 승률 %.0f%%' % (game, win, loss, win_rate))
print('-----------------------------------')

for item in recent_match_champion_sorted:
    game = item[1][0]
    win = item[1][1]
    loss = item[1][2]
    win_rate = win / game * 100
    print('%s %d게임 %d승 %d패 승률 %.0f%%' % (champion[item[0]], game, win, loss, win_rate))

print('-----------------------------------')
print('%s' % recent_match_info_df)
