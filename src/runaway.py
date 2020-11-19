from data_set import summoner_spell, champion, item, rune
from parsing import parsing
from match_preprocessing import match_preprocessing
from win_prediction import win_prediction


def runaway():
    # API key
    api_key_file = open('../../api_key.txt', 'r')
    API_KEY = api_key_file.read()

    # Number of recent matches (Default: 20)
    MATCHES = 20
    SEASON = 2020


    print('\nRunaway\n')
    print('리그 오브 레전드 승패 예측을 이용한 닷지 추천 시스템')
    print('League of Legends Queue Dodging Recommendation System using Win-Loss Prediction')
    print('(c) 2020 Lee Seung Won. All rights reserved.')

    # Parsing summoner names from in-game chat
    participant_list = parsing(API_KEY)
    for summoner_idx in range(5):
        summoner_name = participant_list[summoner_idx]
        print()
        match_preprocessing(API_KEY, summoner_name, summoner_idx, summoner_spell, champion, item, rune)

    print('\n모든 소환사의 전적 전처리가 완료되었습니다.')

    # ML part
    # win_prediction()


if __name__ == '__main__':
    runaway()
