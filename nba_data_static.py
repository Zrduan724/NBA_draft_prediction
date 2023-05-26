import requests
import csv
import json

def get_data(url):
    headers={
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Connection': 'keep-alive',
                'Host': 'stats.nba.com',
                'Origin': 'https://www.nba.com',
                'Referer': 'https://www.nba.com/',
                'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                }
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    # print(json_data)
    data_all = json_data['resultSets'][0]['rowSet']
    # print(data_all)
    return data_all

playerList=[]


def player_data(json_data):
    for items in json_data:
        player_data = {}

        PLAYER_ID = items[1]
        PLAYER_NAME = items[4]
        POSITION = items[5]
        HEIGHT_WO_SHOES_FT_IN = items[7]
        HEIGHT_W_SHOES_FT_IN = items[9]
        WEIGHT = items[10]
        WINGSPAN_FT_IN = items[12]
        STANDING_REACH_FT_IN = items[14]
        BODY_FAT_PCT = items[15]
        HAND_LENGTH = items[16]
        HAND_WIDTH = items[17]


        player_data['PLAYER_ID'] = PLAYER_ID
        player_data['PLAYER_NAME'] = PLAYER_NAME
        player_data['POSITION'] = POSITION
        player_data['HEIGHT_WO_SHOES_FT_IN'] = HEIGHT_WO_SHOES_FT_IN
        player_data['HEIGHT_W_SHOES_FT_IN'] = HEIGHT_W_SHOES_FT_IN
        player_data['WEIGHT'] = WEIGHT
        player_data['WINGSPAN_FT_IN'] = WINGSPAN_FT_IN
        player_data['STANDING_REACH_FT_IN'] = STANDING_REACH_FT_IN
        player_data['BODY_FAT_PCT'] = BODY_FAT_PCT
        player_data['HAND_LENGTH'] = HAND_LENGTH
        player_data['HAND_WIDTH'] = HAND_WIDTH
        playerList.append(player_data)
    print(playerList)
    return playerList


url = 'https://stats.nba.com/stats/draftcombineplayeranthro?LeagueID=00&SeasonYear=2022-23'
for i in range(2013,2024):
        url = 'https://stats.nba.com/stats/draftcombineplayeranthro?LeagueID=00&SeasonYear='+str(i)+'-'+str(i-1999)
        json_data = get_data(url)
        playerList = player_data(json_data)

with open('nba_player_Static measurement data.csv', 'w', encoding='utf-8', newline='') as f:
    write = csv.DictWriter(f, fieldnames=['PLAYER_ID', 'PLAYER_NAME', 'POSITION', 'HEIGHT_WO_SHOES_FT_IN', 'HEIGHT_W_SHOES_FT_IN', 'WEIGHT',
                                            'WINGSPAN_FT_IN','STANDING_REACH_FT_IN', 'BODY_FAT_PCT','HAND_LENGTH','HAND_WIDTH'])
    write.writeheader()
    for data in playerList:
        write.writerow(data)