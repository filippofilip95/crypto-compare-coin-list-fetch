from graphqlclient import GraphQLClient
import requests
import json
import time

URL_TO_FETCH = 'https://www.cryptocompare.com/api/data/coinlist/'
URL_TO_POST = 'YOUR URL TO GRAPHQL SERVER'

client = GraphQLClient(URL_TO_POST)

print('Fetching from {} started.'.format(URL_TO_FETCH))

loaded_page = requests.get(URL_TO_FETCH)

if(loaded_page.status_code == 200):
    response = json.loads(loaded_page.content.decode('utf-8'))

    with open('./loaded_coins.json','w+') as loaded_coins:
        loaded_coins.write(json.dumps(response, indent=4, sort_keys=True))

        print('{} coins loaded and saved to file.'.format(len(response['Data'])))

    coins = response['Data']
    for key, coin in coins.items():
        if(not 'ImageUrl' in coin):
            coin['ImageUrl'] = ''

        result = client.execute('''
            mutation {{
                createCryptoCoin(
                    cId: "{Id}",
                    algorithm: "{Algorithm}",
                    coinName: "{CoinName}",
                    fullName: "{FullName}",
                    fullyPremined: "{FullyPremined}",
                    imageUrl: "{ImageUrl}",
                    name: "{Name}",
                    preMinedValue: "{PreMinedValue}",
                    proofType: "{ProofType}",
                    sortOrder: {SortOrder},
                    symbol: "{Symbol}",
                    totalCoinsFreeFloat: "{TotalCoinsFreeFloat}",
                    totalCoinSupply: "{TotalCoinSupply}",
                    url: "{Url}"){{
                        id
                        fullName
                    }}
            }}
            '''.format(**coin)
        )

        json.loads(result)
        if(('errors' in result) or (not 'data' in result)):
            print('Coin - {} - failed to create!'.format(coin['FullName']))
        else:
            print('Coin - {} - created!'.format(result['data']['createCryptoCoin']['fullName']))


       

