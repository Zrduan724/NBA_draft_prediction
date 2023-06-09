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
    # print(json_data)
    data_all = json_data['resultSets'][0]['rowSet']
    # print(data_all)
    return data_all


def player_data(json_data):
    playerList = []
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
    # print(playerList_sort)
    return playerList_sort

def delate(playerList):
    # 统计None出现次数，大于4删除该球员信息
    player_delate = []
    for i in range (len(playerList)):
        c = 0
        item = playerList[i]
        for key in item:
            if (item[key] == None):
                c += 1
        if (c<=4):
            player_delate.append(item)
    return player_delate



def write_data(filename,playerList_sort):
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        write = csv.DictWriter(f, fieldnames=['PLAYER_ID', 'PLAYER_NAME', 'POSITION', 'HEIGHT_WO_SHOES_FT_IN', 'HEIGHT_W_SHOES_FT_IN', 'WEIGHT',
                                                'WINGSPAN_FT_IN','STANDING_REACH_FT_IN', 'BODY_FAT_PCT','HAND_LENGTH','HAND_WIDTH','RANKING'])
        write.writeheader()
        for data in playerList_sort:
            write.writerow(data)
    return 0

def count(playerList):
    count_ = 0
    count_effective = 0
    for i in range (len(playerList)):
        item = playerList[i]
        for key in item:
            count_ += 1
            if (item[key] != None):
                count_effective += 1
    return count_, count_effective



# url = 'https://stats.nba.com/stats/draftcombineplayeranthro?LeagueID=00&SeasonYear=2022-23'
# url_ranking = 'https://stats.nba.com/stats/drafthistory?College=&LeagueID=00&OverallPick=&RoundNum=&RoundPick=&Season=2022&TeamID=0&TopX='

num_static_total = 0
num_ranking = 0

total_count = 0
total_count_effective = 0

playerList_delate_all = []

for i in range(2013,2023):
        url = 'https://stats.nba.com/stats/draftcombineplayeranthro?LeagueID=00&SeasonYear='+str(i)+'-'+str(i-1999)
        url_ranking = 'https://stats.nba.com/stats/drafthistory?College=&LeagueID=00&OverallPick=&RoundNum=&RoundPick=&Season='+str(i)+'&TeamID=0&TopX='
        json_data = get_data(url)
        json_data_ranking = get_data(url_ranking)
        # 全部静态体测数据
        playerList = player_data(json_data)
        # 对应年份排名数据
        player_ranking = player_data_ranking(json_data_ranking)
        # 结合排名和静态体测数据
        playerList_sort = sort(playerList, player_ranking)
        # 删除数据缺失的NBA球员
        playerList_delate = delate(playerList_sort)

        for data in playerList_delate:
            playerList_delate_all.append(data)

        # 静态数据总人数
        num_static_total += len(playerList)
        # 拥有排名人数
        num_ranking += len(playerList_sort)

        # 有排名的NBA球员的全部静态体测数据和有效静态体测数据
        count_, count_effective = count(playerList_sort)
        total_count += count_
        total_count_effective += count_effective

        filename = 'nba_player_static measurement data-' + str(i) + '.csv'
        write_data(filename, playerList_sort)


filename_delate = 'nba_player_static measurement data all.csv'
write_data(filename_delate, playerList_delate_all)

print("爬取静态数据总人数：",num_static_total," 拥有排名人数：",num_ranking)
category = len(playerList_sort[0])
print("类别总数：",category)
print("NBA球员的全部静态体测数据：",total_count," 和有效静态体测数据：",total_count_effective)
