from bs4 import BeautifulSoup
import requests
import argparse
#import pandas

# Setup player page ticker
# Hit page, get tags that we need that contain resourceId for the player
# Use resourceId to form URL string, platform can be a param for now
# Grab other needed values from page before hitting API (playerName, Stats etc)
# Hit API
# TARGET INFO: <div id="player-info" style="display: none;" data-resource-id="238794" data-platform="ps4" data-year="23" data-platform-url="1"></div>
# OLD urlString='https://www.futbin.com/23/sales/26295?platform=ps'


# process args
parser = argparse.ArgumentParser(description='Fetches sales data for a given FUT player id/platform.. Target URL Eg: https://www.futbin.com/23/sales/26295?platform=ps'
, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("action", help="main action to be performed")
parser.add_argument("-p", "--player_num", required=False, default="1000", help="player number to be used with "'player'" action")
parser.add_argument("-c", "--platform", required=False, default="pc", help="platform for search to be performed, can be "'pc'" or "'ps4'"")
parser.add_argument("--pr", required=False, help="add the call to fetch prices")
parser.add_argument("--gr", required=False, help="add the call to fetch player graph data")
parser.add_argument("--sa", required=False, help="add the call to fetch player sales")




args = parser.parse_args()
config = vars(args)
print(config)


# Args
action = args.action # eg."26295"
player_num = args.player_num # eg. "pc"
platform = args.platform

# Globals
baseUrl = 'https://www.futbin.com/24/'  # TODO UPDATE TO: Base 24 Sales Url
baseApiUrl = 'https://www.futbin.com/24/getPlayerSales'
listPlayersExtn = 'players?page='
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


# -- FUNCTIONS --#




def processArgs(action, player_num):
    if action == 'popular':
        print("Fetching popular players list")

    elif action == 'latest':
        print("Fetching latest players")

    elif action == 'player':
        if player_num == None:
            print("Args not passed properly")
            print(help)
            exit()
        print("Fetching individual player data for player: ", player_num)

        showPlayerDetails(player_num)
        getPlayerPrices(playerResourceId)
        getPlayerSales(playerResourceId, platform)
        getPlayerGraph(playerResourceId)

    else:
        print("Args not passed properly")
        print(help)
        exit()


def getPlayerPrices(playerResourceId):

    print("Calling getPlayerPrices (API)")

    # TODO target: ".../24/playerPrices?player=237067&rids="
    # this works: https://www.futbin.com/24/playerPrices?player=237067&rids=

    
    apiStub = 'playerPrices'

    apiUrl = baseUrl + apiStub

    print(apiUrl)
    
    params = {
    'player': playerResourceId,
    'rids' : ""
    } 

    response = requests.get(apiUrl, params=params, headers=headers)
    
    print(response.content.decode())


def getPlayerGraph(playerResourceId):
    # TODO Target: https://www.futbin.com/24/playerGraph?type=daily_graph&year=24&player=237067&set_id=
    
    print("Calling getPlayerGraph (API)")

    # TODO target: "..https://www.futbin.com/24/playerGraph?type=daily_graph&year=24&player=237067&set_id="\
    
    apiStub = 'playerGraph'

    apiUrl = baseUrl + apiStub

    print(apiUrl)
    
    params = {
    'type' : 'daily_graph',
    'year' : '24',
    'player': playerResourceId,
    'set_id' : ""
    } 

    response = requests.get(apiUrl, params=params, headers=headers)
    
    print(response.content.decode())

def getPlayerSales(playerResourceId, platform):
    
    # TEMP - Remove
    '''
    https://www.futbin.com/24/sales/630?platform=pc
    Current Player ResourceID:  212188
    Current Player Name:  Werner
    Current Player Rating:  82
    Current Player Position:  ST
    https://www.futbin.com/24/getPlayerSales?resourceId=212188&platform=pc'''

    print("Calling getPlayerSales")

    apiStub = 'getPlayerSales'
    apiUrl = baseUrl + apiStub
    print(apiUrl)
    
    params = {
    'resourceId': playerResourceId,
    'platform': platform,
    }

    response = requests.get(baseApiUrl, params=params, headers=headers)
    
    #newResp = json.dumps(response.content.decode(), sort_keys=True, indent=10)

    print(response.content.decode())



def showPlayerDetails(player_num):   
    
    #print("Calling showPlayerDetails")
    global playerResourceId
    urlStr = (baseUrl + 'player/' + player_num)

    #response = requests.get(urlString, headers=headers)
    response = requests.get(urlStr, headers=headers)
    soup = BeautifulSoup(response.content,'html.parser')
    #response = requests.get('https://www.futbin.com/24/player/18987/johan-cruyff', headers=headers)
    #soup = BeautifulSoup(response.content, 'html.parser')

    # Capture player resourceId (used for API)
    playerResourceString = soup.find("div", id="page-info")

    # Player Details
    playerId = playerResourceString.attrs["data-id"]
    playerResourceId = playerResourceString.attrs["data-player-resource"]
    playerNation = playerResourceString.attrs["data-nation"]
    playerLeague = playerResourceString.attrs["data-league"]
    playerClub = playerResourceString.attrs["data-club"]
    playerPosition = playerResourceString.attrs["data-position"]    

    print("New player resources: ", "player resource ID: ", playerResourceId, "playerId: ", playerId, "playerNation: ", playerNation, "playerLeague: ", playerLeague, "playerClub: ",  playerClub, "playerPosition: ", playerPosition)

    # Player Attributes

    table = soup.find('table', attrs={'class':'table table-info'})
    table_rows = table.find_all('tr', attrs={'class' : ''})

    data = []

    for row in table_rows:
        row_headers = row.find_all('th')
        cols = row.find_all('td')

        #print(headers.text)
        row_headers = [ele.text.strip() for ele in row_headers]
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in row_headers if ele] + [ele for ele in cols if ele])

    print(data)

    return(playerResourceId, playerId, playerNation, playerLeague, playerClub, playerPosition, data)


# Main flow
processArgs(action, player_num)

# TODO NEXT: Convert all output to json
# TODO getGraphData
# TODO use pandas to tabulate
# TODO Should only be called from within a function: getPlayerSales(playerResourceId, platform)
# TODO Another interesting page : <a href="/24/pgp?pid=18987" 
# TODO Another element: <div id="Player-card" data-special-img="0" data-revision="icon" data-level="gold" data-rare-type="12" class="pcdisplay ut24 card-regular icon gold rare  center-block ">
# TODO Main player details bit: <div id="info_content" class="box-shadow pt-3 pb-3">
                               