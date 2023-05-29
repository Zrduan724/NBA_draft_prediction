import requests
import csv
import json
import math

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
        data_all = json_data['resultSets'][0]['rowSet']
        return data_all

def player_data(json_data):
        playerList = []
        for items in json_data:
                player_data = {}

                PLAYER_ID = items[1]
                PLAYER_NAME = items[4]
                POSITION = items[5]
                STANDING_VERTICAL_LEAP = items[6]
                MAX_VERTICAL_LEAP = items[7]
                LANE_AGILITY_TIME = items[8]
                MODIFIED_LANE_AGILITY_TIME = items[9]
                THREE_QUARTER_SPRINT = items[10]
                BENCH_PRESS = items[11]

                player_data['PLAYER_ID'] = PLAYER_ID
                player_data['PLAYER_NAME'] = PLAYER_NAME
                player_data['POSITION'] = POSITION
                player_data['STANDING_VERTICAL_LEAP'] = STANDING_VERTICAL_LEAP
                player_data['MAX_VERTICAL_LEAP'] = MAX_VERTICAL_LEAP
                player_data['LANE_AGILITY_TIME'] = LANE_AGILITY_TIME
                player_data['MODIFIED_LANE_AGILITY_TIME'] = MODIFIED_LANE_AGILITY_TIME
                player_data['THREE_QUARTER_SPRINT'] = THREE_QUARTER_SPRINT
                player_data['BENCH_PRESS'] = BENCH_PRESS
                playerList.append(player_data)
        # print(playerList)
        return playerList

def player_data_ranking(json_data):
    player_ranking = []
    for items in json_data:
        PLAYER_NAME = items[1]
        player_ranking.append(PLAYER_NAME)
    return player_ranking

def sort(playerList,player_ranking):
    playerList_sort = []
    for i in range(len(player_ranking)):
        name = player_ranking[i]
        for j in range(len(playerList)):
            item = playerList[j]
            NAME = playerList[j]['PLAYER_NAME']
            if (name == NAME):
                rank = math.ceil((i+1)/5)
                item['RANKING'] = str(rank)
                playerList_sort.append(item)
    print(playerList_sort)
    return playerList_sort


def write_data(filename,playerList_sort):
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        write = csv.DictWriter(f, fieldnames=['PLAYER_ID', 'PLAYER_NAME', 'POSITION', 'STANDING_VERTICAL_LEAP', 'MAX_VERTICAL_LEAP', 'LANE_AGILITY_TIME',
                                            'MODIFIED_LANE_AGILITY_TIME' ,'THREE_QUARTER_SPRINT', 'BENCH_PRESS','RANKING'])
        write.writeheader()
        for data in playerList_sort:
            write.writerow(data)
    return 0

# url = 'https://stats.nba.com/stats/draftcombinedrillresults?LeagueID=00&SeasonYear=2022-23'
# url_ranking = 'https://stats.nba.com/stats/drafthistory?College=&LeagueID=00&OverallPick=&RoundNum=&RoundPick=&Season=2022&TeamID=0&TopX='

for i in range(2013,2023):
        url = 'https://stats.nba.com/stats/draftcombinedrillresults?LeagueID=00&SeasonYear='+str(i)+'-'+str(i-1999)
        url_ranking = 'https://stats.nba.com/stats/drafthistory?College=&LeagueID=00&OverallPick=&RoundNum=&RoundPick=&Season='+str(i)+'&TeamID=0&TopX='
        json_data = get_data(url)
        json_data_ranking = get_data(url_ranking)
        playerList = player_data(json_data)
        player_ranking = player_data_ranking(json_data_ranking)
        playerList_sort = sort(playerList,player_ranking)
        filename = 'nba_player_dynamic measurement data-'+str(i)+'.csv'
        print(len(playerList_sort),len(player_ranking))
        write_data(filename, playerList_sort)

#

