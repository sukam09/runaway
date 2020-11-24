from dataset import summoner_spell, champion, rune

import pandas as pd
import requests
from tqdm import tqdm
from operator import itemgetter
import time


class RunawayAgent():

    def __init__(self):
        api_key_file = open('../../api_key.txt', 'r')
        self.api_key = api_key_file.read()

        print('\nRunaway\n')
        print('리그 오브 레전드 승패 예측을 이용한 닷지 추천 시스템')
        print('League of Legends Queue Dodging Recommendation System using Win-Loss Prediction')
        print('(c) 2020 Lee Seung Won. All rights reserved.')
    
    def run(self):
        self.participant_list = self.parsing()  # Parse summoner names from in-game chat
        for summoner_idx in range(5):
            summoner_name = self.participant_list[summoner_idx]
            print()
            self.match_preprocessing(summoner_name, summoner_idx)
        print('\n모든 소환사의 전적 전처리가 완료되었습니다.')

    def parsing(self):
        print('\n아군 팀원의 소환사명이 나타난 채팅을 복사 및 붙여넣기 해주세요. 전적 사이트에서 멀티서치를 하는 방법과 동일합니다.\n')
        while True:
            banpick_chat = []
            while True:
                line = input()
                if line:
                    banpick_chat.append(line)
                else:
                    break
        
            participant_list = []
            for i in range(len(banpick_chat)):
                banpick_chat[i] = banpick_chat[i].split('님이 로비에 참가하셨습니다.')
                if len(banpick_chat[i]) > 1:
                    summoner_name = banpick_chat[i][0]
                    summoner_api = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + self.api_key
                    summoner = requests.get(summoner_api).json()
                    if 'status' not in summoner:
                        participant_list.append(banpick_chat[i][0])
                    elif summoner['status']['status_code'] == 404:
                        print('존재하지 않는 소환사명:', summoner_name)
                        continue
                    else:
                        pass  # Deprecated

            participant_num = len(participant_list)
            print('입력된 소환사명:', participant_list)
            if participant_num == 5:
                print('모든 아군 팀원의 소환사명이 성공적으로 입력되었습니다.')
                return participant_list
            else:
                print('모든 아군 팀원의 소환사명이 입력되지 않았습니다. 다시 입력해 주세요.\n')
    
    def match_preprocessing(self, summoner_name, summoner_idx):
        # League match data structure
        league_match_id = []
        league_match_champion = []
        league_match_win = []
        league_match_info = []
        league_match_data = []

        summoner_api = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + self.api_key
        summoner = requests.get(summoner_api).json()

        while True:
            if 'status' not in summoner:
                account_id = summoner['accountId']
                summoner_id = summoner['id']
                break
            else:
                for _ in tqdm(range(120), desc='API 요청 제한 횟수를 초과로 인한 대기중'):
                    time.sleep(1)
                summoner = requests.get(summoner_api).json()
        
        league_api = 'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summoner_id + '?api_key=' + self.api_key
        league = requests.get(league_api).json()

        while True:
            if 'status' not in league:
                break
            else:
                for _ in tqdm(range(120), desc='API 요청 제한 횟수 초과로 인한 대기중'):
                    time.sleep(1)
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

        # Count played champions
        count = 0
        for i in tqdm(range(league_game // 100 + 1), desc=summoner_name + '의 플레이한 챔피언 집계중'):
            begin_idx = 100 * i
            matchlist_api = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account_id + '?queue=420&beginIndex=' + str(begin_idx) + '&api_key=' + self.api_key
            matchlist = requests.get(matchlist_api).json()['matches']

            while True:
                if 'status' not in matchlist:
                    break
                else:
                    for _ in tqdm(range(120), desc='API 요청 제한 횟수 초과로 인한 대기중'):
                        time.sleep(1)
                    matchlist = requests.get(matchlist_api).json()['matches']

            for j in range(100):
                if count >= league_game:
                    break
                else:
                    league_match_id.append(matchlist[j]['gameId'])
                    league_match_champion.append(matchlist[j]['champion'])
                    count += 1

        # Generate league match data set
        for i in tqdm(range(20), desc=summoner_name + '의 시즌 데이터 셋 구축중'):
            match_api = 'https://kr.api.riotgames.com/lol/match/v4/matches/' + str(league_match_id[i]) + '?api_key=' + self.api_key
            match = requests.get(match_api).json()

            while True:
                if 'status' not in match:
                    game_duration = match['gameDuration']
                    match_team_info = match['participants']
                    break
                else:
                    for _ in tqdm(range(120), desc='API 요청 제한 횟수 초과로 인한 대기중'):
                        time.sleep(1)
                    match = requests.get(match_api).json()

            # Check player's team
            for j in range(10):
                if match_team_info[j]['championId'] == league_match_champion[i]:
                    match_info = match_team_info[j]
                    if j < 5:
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
            league_match_info_row.append(champion[league_match_champion[i]])
            league_match_data_row.append(league_match_champion[i])

            # Win-Loss
            if game_duration <= 300:
                league_match_win.append(-1)  # Invalid matches
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
            # Currently not using item name due to preseason patch
            league_match_info_row.append(stat['item0'])
            league_match_info_row.append(stat['item1'])
            league_match_info_row.append(stat['item2'])
            league_match_info_row.append(stat['item3'])
            league_match_info_row.append(stat['item4'])
            league_match_info_row.append(stat['item5'])

            league_match_data_row.append(stat['item0'])
            league_match_data_row.append(stat['item1'])
            league_match_data_row.append(stat['item2'])
            league_match_data_row.append(stat['item3'])
            league_match_data_row.append(stat['item4'])
            league_match_data_row.append(stat['item5'])

            # Compelete preprocessing for one match
            league_match_info.append(league_match_info_row)
            league_match_data.append(league_match_data_row)

        # Copy to recent matches
        recent_match_info = league_match_info[:20]
        recent_match_data = league_match_data[:20]
        recent_match_win = league_match_win[:20]
        recent_match_champion = league_match_champion[:20]

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
        file_num = summoner_idx + 1
        recent_match_info_df.to_csv('../data/recent_match_info_' + str(file_num) + '.csv')
        recent_match_data_df.to_csv('../data/recent_match_data_' + str(file_num) + '.csv')

        # Count recent match champions
        recent_match_champion_checker = {}
        for i in range(len(recent_match_champion)):
            # If the match is valid
            if recent_match_win[i] != -1:
                if recent_match_champion[i] in recent_match_champion_checker:
                    recent_match_champion_checker[recent_match_champion[i]][0] += 1
                    if recent_match_win[i] == 1:
                        recent_match_champion_checker[recent_match_champion[i]][1] += 1
                    else:
                        recent_match_champion_checker[recent_match_champion[i]][2] += 1
                else:
                    recent_match_champion_checker[recent_match_champion[i]] = [1, 0, 0]
                    if recent_match_win[i] == 1:
                        recent_match_champion_checker[recent_match_champion[i]][1] += 1
                    else:
                        recent_match_champion_checker[recent_match_champion[i]][2] += 1
        recent_match_champion_sorted = sorted(recent_match_champion_checker.items(), key=itemgetter(1), reverse=True)

        # Results
        print('=' * 100)
        print(summoner_name)

        game = len(recent_match_win)
        win = recent_match_win.count(1)
        loss = recent_match_win.count(0)
        win_rate = win / game * 100

        print('=' * 100)
        print('%d시즌 솔로랭크(최근 %d게임)' % (2020, 20))
        print('=' * 100)
        print('총 %s게임 %s승 %s패 승률 %.0f%%' % (game, win, loss, win_rate))
        print('-' * 100)

        for item in recent_match_champion_sorted:
            game = item[1][0]
            win = item[1][1]
            loss = item[1][2]
            win_rate = win / game * 100
            print('%s %d게임 %d승 %d패 승률 %.0f%%' % (champion[item[0]], game, win, loss, win_rate))

        print('-' * 100)
        print('%s' % recent_match_info_df)
    
    def win_prediction(self):
        # ML part
        pass


if __name__ == '__main__':
    runaway_agent = RunawayAgent()
    runaway_agent.run()
