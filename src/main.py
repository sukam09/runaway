import pandas as pd
import requests
from tqdm import tqdm
import json
import operator


# Data set
summoner_spell = {
    1: '정화',
    3: '탈진',
    4: '점멸',
    6: '유체화',
    7: '회복',
    11: '강타',
    12: '순간이동',
    13: '총명',
    14: '점화',
    21: '방어막',
}

champion = {
    1: '애니',
    2: '올라프',
    3: '갈리오',
    4: '트위스티드 페이트',
    5: '신 짜오',
    6: '우르곳',
    7: '르블랑',
    8: '블라디미르',
    9: '피들스틱',
    10: '케일',
    11: '마스터 이',
    12: '알리스타',
    13: '라이즈',
    14: '사이온',
    15: '시비르',
    16: '소라카',
    17: '티모',
    18: '트리스타나',
    19: '워윅',
    20: '누누와 윌럼프',
    21: '미스 포츈',
    22: '애쉬',
    23: '트린다미어',
    24: '잭스',
    25: '모르가나',
    26: '질리언',
    27: '신지드',
    28: '이블린',
    29: '트위치',
    30: '카서스',
    31: '초가스',
    32: '아무무',
    33: '람머스',
    34: '애니비아',
    35: '샤코',
    36: '문도 박사',
    37: '소나',
    38: '카사딘',
    39: '이렐리아',
    40: '잔나',
    41: '갱플랭크',
    42: '코르키',
    43: '카르마',
    44: '타릭',
    45: '베이가',
    48: '트런들',
    50: '스웨인',
    51: '케이틀린',
    53: '블리츠크랭크',
    54: '말파이트',
    55: '카타리나',
    56: '녹턴',
    57: '마오카이',
    58: '레넥톤',
    59: '자르반 4세',
    60: '엘리스',
    61: '오리아나',
    62: '오공',
    63: '브랜드',
    64: '리 신',
    67: '베인',
    68: '럼블',
    69: '카시오페아',
    72: '스카너',
    74: '하이머딩거',
    75: '나서스',
    76: '니달리',
    77: '우디르',
    78: '뽀삐',
    79: '그라가스',
    80: '판테온',
    81: '이즈리얼',
    82: '모데카이저',
    83: '요릭',
    84: '아칼리',
    85: '케넨',
    86: '가렌',
    89: '레오나',
    90: '말자하',
    91: '탈론',
    92: '리븐',
    96: '코그모',
    98: '쉔',
    99: '럭스',
    101: '제라스',
    102: '쉬바나',
    103: '아리',
    104: '그레이브즈',
    105: '피즈',
    106: '볼리베어',
    107: '렝가',
    110: '바루스',
    111: '노틸러스',
    112: '빅토르',
    113: '세주아니',
    115: '직스',
    114: '피오라',
    117: '룰루',
    119: '드레이븐',
    120: '헤카림',
    121: '카직스',
    122: '다리우스',
    126: '제이스',
    127: '리산드라',
    131: '다이애나',
    133: '퀸',
    134: '신드라',
    136: '아우렐리온 솔',
    141: '케인',
    142: '조이',
    143: '자이라',
    145: '카이사',
    150: '나르',
    154: '자크',
    157: '야스오',
    161: '벨코즈',
    163: '탈리야',
    164: '카밀',
    201: '브라움',
    202: '진',
    203: '킨드레드',
    222: '징크스',
    223: '탐 켄치',
    235: '세나',
    236: '루시안',
    238: '제드',
    240: '클레드',
    245: '에코',
    246: '키아나',
    254: '바이',
    266: '아트록스',
    267: '나미',
    268: '아지르',
    350: '유미',
    412: '쓰레쉬',
    420: '일라오이',
    421: '렉사이',
    427: '아이번',
    429: '칼리스타',
    432: '바드',
    497: '라칸',
    498: '자야',
    516: '오른',
    517: '사일러스',
    518: '니코',
    523: '아펠리오스',
    555: '파이크',
    875: '세트'
}

item = {
    0: '-',
    1001: '속도의 장화',
    1004: '요정의 부적',
    1006: '원기 회복의 구슬',
    1011: '거인의 허리띠',
    1018: '민첩성의 망토',
    1026: '방출의 마법봉',
    1027: '사파이어 수정',
    1028: '루비 수정',
    1029: '천 갑옷',
    1031: '쇠사슬 조끼',
    1033: '마법무효화의 망토',
    1036: '롱소드',
    1037: '곡괭이',
    1038: 'B.F. 대검',
    1039: '사냥꾼의 부적',
    1041: '사냥꾼의 마체테',
    1042: '단검',
    1043: '곡궁',
    1052: '증폭의 고서',
    1053: '흡혈의 낫',
    1054: '도란의 방패',
    1055: '도란의 검',
    1056: '도란의 반지',
    1057: '음전자 망토',
    1058: '쓸데없이 큰 지팡이',
    1082: '암흑의 인장',
    1083: '수확의 낫',
    1400: '마법 부여: 용사',
    1401: '마법 부여: 잿불거인',
    1402: '마법 부여: 룬의 메아리',
    1412: '마법 부여: 용사',
    1413: '마법 부여: 잿불거인',
    1414: '마법 부여: 룬의 메아리',
    1416: '마법 부여: 피갈퀴손',
    1419: '마법 부여: 피갈퀴손',
    2003: '체력 물약',
    2006: '체력 물약',
    2009: '원기 회복의 완전한 비스킷',
    2010: '굳건한 의지의 완전한 비스킷',
    2015: '키르히아이스의 파편',
    2031: '충전형 물약',
    2033: '부패 물약',
    2047: '예언자의 추출액',
    2051: '가디언의 뿔피리',
    2052: '포로 간식',
    2054: 'Diet Poro-Snax',
    2055: '제어 와드',
    2065: '슈렐리아의 몽상',
    2138: '강철의 영약',
    2139: '마법의 영약',
    2140: '분노의 영약',
    2403: '미니언 해체분석기',
    2419: '초시계 키트',
    2420: '초시계',
    2421: '망가진 초시계',
    2422: '약간 신비한 장화',
    2423: '완벽한 초시계',
    2424: '망가진 초시계',
    3001: '심연의 가면',
    3003: '대천사의 지팡이',
    3004: '마나무네',
    3005: '아트마의 창',
    3006: '광전사의 군화',
    3007: '대천사의 지팡이(급속 충전)',
    3008: '마나무네(급속 충전)',
    3009: '신속의 장화',
    3010: '억겁의 카탈리스트',
    3020: '마법사의 신발',
    3022: '얼어붙은 망치',
    3024: '빙하의 장막',
    3025: '얼어붙은 건틀릿',
    3026: '수호 천사',
    3027: '영겁의 지팡이',
    3028: '조화의 성배',
    3029: '영겁의 지팡이(급속 충전)',
    3030: '마법공학 GLP-800',
    3031: '무한의 대검',
    3033: '필멸자의 운명',
    3035: '최후의 속삭임',
    3036: '도미닉 경의 인사',
    3040: '대천사의 포옹',
    3041: '메자이의 영혼약탈자',
    3042: '무라마나',
    3043: '무라마나',
    3044: '탐식의 망치',
    3046: '유령 무희',
    3047: '닌자의 신발',
    3048: '대천사의 포옹',
    3050: '지크의 융합',
    3052: '요림의 주먹',
    3053: '스테락의 도전',
    3057: '광휘의 검',
    3065: '정령의 형상',
    3067: '점화석',
    3068: '태양불꽃 망토',
    3070: '여신의 눈물',
    3071: '칠흑의 양날 도끼',
    3072: '피바라기',
    3073: '여신의 눈물(급속 충전)',
    3074: '굶주린 히드라',
    3075: '가시 갑옷',
    3076: '덤불 조끼',
    3077: '티아맷',
    3078: '삼위일체',
    3082: '파수꾼의 갑옷',
    3083: '워모그의 갑옷',
    3084: '지배자의 피갑옷',
    3085: '루난의 허리케인',
    3086: '열정의 검',
    3087: '스태틱의 단검',
    3089: '라바돈의 죽음모자',
    3091: '마법사의 최후',
    3094: '고속 연사포',
    3095: '폭풍갈퀴',
    3100: '리치베인',
    3101: '쐐기검',
    3102: '밴시의 장막',
    3105: '군단의 방패',
    3107: '구원',
    3108: '악마의 마법서',
    3109: '기사의 맹세',
    3110: '얼어붙은 심장',
    3111: '헤르메스의 발걸음',
    3112: '수호자의 보주',
    3113: '에테르 환영',
    3114: '금지된 우상',
    3115: '내셔의 이빨',
    3116: '라일라이의 수정홀',
    3117: '기동력의 장화',
    3123: '처형인의 대검',
    3124: '구인수의 격노검',
    3128: '죽음불꽃 손아귀',
    3131: '신성의 검',
    3133: '콜필드의 전투 망치',
    3134: '톱날 단검',
    3135: '공허의 지팡이',
    3136: '기괴한 가면',
    3137: '광신도의 검',
    3139: '헤르메스의 시미터',
    3140: '수은 장식띠',
    3142: '요우무의 유령검',
    3143: '란두인의 예언',
    3144: '빌지워터의 해적검',
    3145: '마법공학 리볼버',
    3146: '마법공학 총검',
    3147: '드락사르의 황혼검',
    3151: '리안드리의 고통',
    3152: '마법공학 초기형 벨트-01',
    3153: '몰락한 왕의 검',
    3155: '주문포식자',
    3156: '맬모셔스의 아귀',
    3157: '존야의 모래시계',
    3158: '명석함의 아이오니아 장화',
    3161: '쇼진의 창',
    3165: '모렐로노미콘',
    3170: '달빛 마법검',
    3172: '서풍',
    3174: '아테나의 부정한 성배',
    3175: '카직스의 머리',
    3179: '그림자 검',
    3181: '핏빛 칼날',
    3184: '수호자의 망치',
    3190: '강철의 솔라리 펜던트',
    3191: '추적자의 팔목 보호대',
    3193: '가고일의 돌갑옷',
    3194: '적응형 투구',
    3196: '마공학 핵 mk-1',
    3197: '마공학 핵 mk-2',
    3198: '완성형 마공학 핵',
    3200: '프로토타입 마공학 핵',
    3211: '망령의 두건',
    3222: '미카엘의 도가니',
    3285: '루덴의 메아리',
    3330: '허수아비',
    3340: '와드 토템',
    3348: '비전 탐지기',
    3361: '상급 투명 토템',
    3362: '상급 투명 감지 토템',
    3363: '망원형 개조',
    3364: '예언자의 렌즈',
    3371: '무한의 용암 대검',
    3373: '대장간 불꽃 망토',
    3374: '라바돈의 죽음왕관',
    3379: '심연의 지옥불 가면',
    3380: '흑요석 양날 도끼',
    3382: '신의 구원',
    3383: '강철의 솔라리 왕관',
    3384: '진 삼위일체',
    3386: '존야의 역설',
    3387: '얼어붙은 주먹',
    3388: '요우무의 망령검',
    3389: '몰락한 왕의 힘',
    3390: '루덴의 파동',
    3400: '수당',
    3410: '카직스의 머리',
    3416: '카직스의 머리',
    3422: '카직스의 머리',
    3455: '카직스의 머리',
    3504: '불타는 향로',
    3508: '정수 약탈자',
    3513: '전령의 눈',
    3514: '전령의 눈',
    3520: '유령 포로',
    3599: '칠흑의 창',
    3600: '칠흑의 창',
    3671: '마법 부여: 용사',
    3672: '마법 부여: 잿불거인',
    3673: '마법 부여: 룬의 메아리',
    3675: '마법 부여: 피갈퀴손',
    3680: '얼음 간식',
    3681: '화르륵 매운맛 간식',
    3682: '에스프레소 간식',
    3683: '무지개 간식 파티 세트',
    3684: '빛의 인도자 포로 간식',
    3685: '어둠의 인도자 포로 간식',
    3690: '우주의 족쇄',
    3691: '블랙홀 랜턴',
    3692: 'Dark Matter Scythe',
    3693: '중력의 장화',
    3694: '성운 망토',
    3695: '암흑의 별 인장',
    3706: '추적자의 검',
    3715: '척후병의 사브르',
    3742: '망자의 갑옷',
    3748: '거대한 히드라',
    3751: '바미의 불씨',
    3800: '정당한 영광',
    3801: '수정 팔 보호구',
    3802: '사라진 양피지',
    3812: '죽음의 무도',
    3814: '밤의 끝자락',
    3850: '주문도둑의 검',
    3851: '얼음 송곳니',
    3853: '얼음 정수의 파편',
    3854: '강철 어깨 보호대',
    3855: '룬 강철 어깨 갑옷',
    3857: '화이트록의 갑옷',
    3858: '고대유물 방패',
    3859: '타곤 산의 방패',
    3860: '타곤 산의 방벽',
    3862: '영혼의 낫',
    3863: '해로윙 초승달낫',
    3864: '검은 안개 낫',
    3901: '가차없는 포격',
    3902: '죽음의 여신',
    3903: '사기진작',
    3905: '쌍둥이 그림자',
    3907: '주문매듭 구슬',
    3916: '망각의 구',
    4001: '유령 장화',
    4003: '생명선',
    4004: '망령 해적검',
    4101: '맹수 추적자의 검',
    4102: '마법 부여: 용사',
    4103: '마법 부여: 잿불거인',
    4104: '마법 부여: 룬의 메아리',
    4105: '마법 부여: 피갈퀴손',
    4201: '도란의 잃어버린 방패',
    4202: '도란의 잃어버린 검',
    4203: '도란의 잃어버린 반지',
    4204: '도란의 잃어버린 우상',
    4401: '대자연의 힘',
    4402: '활력증진의 보석함',
    4403: '뒤집개'
}

rune = {
    8000: '정밀',
    8005: '집중 공격',
    8010: '정복자',
    8008: '치명적 속도',
    8021: '기민한 발놀림',
    8100: '지배',
    8112: '감전',
    8124: '포식자',
    8128: '어둠의 수확',
    8200: '마법',
    8214: '콩콩이 소환',
    8229: '신비로운 유성',
    8230: '난입',
    8300: '영감',
    8351: '빙결 강화',
    8358: '프로토타입: 마법의 돌',
    8360: '봉인 풀린 주문서',
    8400: '결의',
    8437: '착취의 손아귀',
    8439: '여진',
    8465: '수호자',
    9923: '칼날비'
}

# API key
# This api key will not be opened publicly followed by the policies of Riot Games, Inc.
# In code the key has been used correctly.
API_KEY = ''

# Number of recent matches (Default: 20)
MATCHES = 20
SEASON = 2020

print('\nLeague of Legends AI Reporting System')
print('(c) 2020 Seungwon Lee. All rights reserved.')

# Default
# summoner_name = input('\n소환사명을 입력하십시오: ')

# For test
summoner_name = 'Hidden Rough'
print('\n소환사명을 입력하십시오: %s' % summoner_name)

# Data structure
recent_match_id = []
recent_match_champion = []
recent_match_win = []

recent_match_info = []
recent_match_data = []

league_match_id = []
league_match_champion = []
league_match_win = []

league_match_data = []

summoner_api = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + API_KEY
summoner = requests.get(summoner_api).json()
account_id = summoner['accountId']
summoner_id = summoner['id']

# For test
# print('\nAccount ID: %s' % account_id)
# print('Summoner ID: %s' % summoner_id)
# print('Recent Match ID: %s' % recent_match_id)

league_api = 'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summoner_id + '?api_key=' + API_KEY
league = requests.get(league_api).json()

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

matchlist_api = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account_id + '?queue=420&api_key=' + API_KEY
recent_match = requests.get(matchlist_api).json()['matches']

# for begin_idx in range(league_game // 100 + 1):
#     for idx in range(begin_idx * 100, begin_idx * 100 + 100):
#         if idx >= league_game:
#             break
#         else:
#             matchlist_api = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account_id + '?queue=420&beginIndex=' + str(begin_idx) + '&api_key=' + API_KEY
#             matchlist = requests.get(matchlist_api).json()['matches']
#             league_match_id.append(matchlist[idx]['gameId'])

# recent_match_id = league_match_id[:20]

# Check whether the match is solo rank
count = 0
for idx in range(len(recent_match)):
    game_id = recent_match[idx]['gameId']
    match_api = 'https://kr.api.riotgames.com/lol/match/v4/matches/' + str(game_id) + '?api_key=' + API_KEY
    match = requests.get(match_api).json()
    game_duration = match['gameDuration']
    if game_duration > 300:
        recent_match_id.append(recent_match[idx]['gameId'])
        recent_match_champion.append(recent_match[idx]['champion'])
        count += 1
    
    if count == MATCHES:
        break

for match_idx in range(MATCHES):
    match_api = 'https://kr.api.riotgames.com/lol/match/v4/matches/' + str(recent_match_id[match_idx]) + '?api_key=' + API_KEY
    match = requests.get(match_api).json()
    game_duration = match['gameDuration']
    match_team_info = match['participants']

    for participant_idx in range(10):
        if match_team_info[participant_idx]['championId'] == recent_match_champion[match_idx]:
            match_info = match_team_info[participant_idx]
            if participant_idx < 5:
                team = 'blue'
            else:
                team = 'red'
            break

    spell1 = match_info['spell1Id']
    spell2 = match_info['spell2Id']
    stat = match_info['stats']

    match_info_row = []
    recent_match_data_row = []

    # Champion
    match_info_row.append(champion[recent_match_champion[match_idx]])
    recent_match_data_row.append(recent_match_champion[match_idx])

    # Win
    if stat['win']:
        match_info_row.append('승리')
        recent_match_data_row.append(1)
        recent_match_win.append(1)
    else:
        match_info_row.append('패배')
        recent_match_data_row.append(0)
        recent_match_win.append(0)

    # Game duration
    match_info_row.append('%s분 %s초' % (game_duration // 60, game_duration % 60))
    recent_match_data_row.append(game_duration)

    # Summoner spell
    match_info_row.append(summoner_spell[spell1])
    match_info_row.append(summoner_spell[spell2])

    recent_match_data_row.append(spell1)
    recent_match_data_row.append(spell2)

    # Runes
    match_info_row.append(rune[stat['perk0']])
    match_info_row.append(rune[stat['perkSubStyle']])
    
    recent_match_data_row.append(stat['perk0'])
    recent_match_data_row.append(stat['perkSubStyle'])

    # KDA
    kill = int(stat['kills'])
    death = int(stat['deaths'])
    assist = int(stat['assists'])

    if death == 0:
        kda = (kill + assist) * 1.2
    else:
        kda = (kill + assist) / death

    match_info_row.append('%d/%d/%d' % (kill, death, assist))
    match_info_row.append('%.2f' % kda)
    recent_match_data_row.append('%.2f' % kda)
    
    # Level and CS
    level = int(stat['champLevel'])
    cs = int(stat['totalMinionsKilled'])
    cspm = cs / (game_duration / 60)

    match_info_row.append(level)
    match_info_row.append(cs)
    match_info_row.append('%.1f' % cspm)

    recent_match_data_row.append(level)
    recent_match_data_row.append(cs)
    recent_match_data_row.append('%.1f' % cspm)

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
    
    match_info_row.append('%.0f%%' % kp)
    recent_match_data_row.append('%.0f' % kp)

    # Items
    match_info_row.append(item[stat['item0']])
    match_info_row.append(item[stat['item1']])
    match_info_row.append(item[stat['item2']])
    match_info_row.append(item[stat['item3']])
    match_info_row.append(item[stat['item4']])
    match_info_row.append(item[stat['item5']])

    recent_match_data_row.append(stat['item0'])
    recent_match_data_row.append(stat['item1'])
    recent_match_data_row.append(stat['item2'])
    recent_match_data_row.append(stat['item3'])
    recent_match_data_row.append(stat['item4'])
    recent_match_data_row.append(stat['item5'])

    recent_match_info.append(match_info_row)
    recent_match_data.append(recent_match_data_row)

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

recent_match_info_df.to_csv('recent_match_info.csv')
recent_match_data_df.to_csv('recent_match_data.csv')

print('\n===========================')
print('%s시즌 개인/2인 랭크 게임' % SEASON)
print('===========================')
print('총 %s게임 %s승 %s패 승률 %.0f%%' % (league_game, league_win, league_loss, league_win_rate))
# print('\n==================================')
# print('%s시즌 가장 많이 플레이한 챔피언' % SEASON)
# print('==================================')

recent_match_champion_checker = {}

for idx in range(len(recent_match_champion)):
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

recent_match_champion_sorted = sorted(recent_match_champion_checker.items(), key=operator.itemgetter(1), reverse=True)

print('\n======================')
print('최근에 플레이한 챔피언')
print('======================')

for item in recent_match_champion_sorted:
    game = item[1][0]
    win = item[1][1]
    loss = item[1][2]
    win_rate = win / game * 100
    print('%s %d게임 승률 %.0f%% %d승 %d패' % (champion[item[0]], game, win_rate, win, loss))

print('\n============================')
print('최근 %s회 개인/2인 랭크 게임' % MATCHES)
print('============================\n%s' % recent_match_info_df)
