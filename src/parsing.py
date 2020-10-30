def parsing():
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
                participant_list.append(banpick_chat[idx][0])

        # participant_num = len(participant_list)
        # print('입력된 소환사명: ', end='')
        # for participant in range(participant_num - 1):
        #     print(participant_list[participant])
        # print(participant_list[participant_num - 1])

        participant_num = len(participant_list)
        print('입력된 소환사명:', participant_list)
        if participant_num == 5:
            print('모든 아군 팀원의 소환사명이 성공적으로 입력되었습니다.')
            break
        else:
            print('아군 팀원 %d명의 소환사명이 입력되지 않았습니다. 다시 입력해주세요.\n' % (5 - participant_num))
    
    return participant_list
        
    # banpick_chat = []
    # while True:
    #     line = input()
    #     if line:
    #         banpick_chat.append(line)
    #     else:
    #         break

    # participant_list = []

    # for idx in range(len(banpick_chat)):
    #     banpick_chat[idx] = banpick_chat[idx].split('님이 로비에 참가하셨습니다.')
    #     if len(banpick_chat[idx]) > 1:
    #         participant_list.append(banpick_chat[idx][0])

    # participant_num = len(participant_list)

    # print('입력된 소환사명: ', end='')
    # print(', '.join(participant_list))
    # print()

    # if participant_num == 5:
    #     print('모든 아군 팀원의 소환사명이 성공적으로 입력되었습니다.')
    # else:
    #     print('아군 팀원 %d명의 소환사명이 입력되지 않았습니다. 다시 입력해주세요.' % (5 - participant_num))

    # return participant_list

# participant_list = parsing()
# print(participant_list)