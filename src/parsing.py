import requests


def parsing(API_KEY):
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
        for idx in range(len(banpick_chat)):
            banpick_chat[idx] = banpick_chat[idx].split('님이 로비에 참가하셨습니다.')
            if len(banpick_chat[idx]) > 1:
                summoner_name = banpick_chat[idx][0]
                summoner_api = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + API_KEY
                summoner = requests.get(summoner_api).json()
                if 'status' not in summoner:
                    participant_list.append(banpick_chat[idx][0])
                elif summoner['status']['status_code'] == 404:
                    print('존재하지 않는 소환사명:', summoner_name)
                    continue
                else:
                    print('Error occurred!!! status code:', summoner['status']['status_code'])

        participant_num = len(participant_list)
        print('입력된 소환사명:', participant_list)
        if participant_num == 5:
            print('모든 아군 팀원의 소환사명이 성공적으로 입력되었습니다.')
            break
        else:
            print('모든 아군 팀원의 소환사명이 입력되지 않았습니다. 다시 입력해 주세요.\n')
    
    return participant_list