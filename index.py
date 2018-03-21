from graphqlclient import GraphQLClient
import requests
import json
import time

URL_TO_FETCH = 'https://www.cryptocompare.com/api/data/coinlist/'
URL_TO_POST = 'URL TO GRAPHQL SERVER'

client = GraphQLClient(URL_TO_POST)

print('Fetching from %(url)s started.' % { 'url': URL_TO_FETCH })

loaded_page = requests.get(URL_TO_FETCH)

if(loaded_page.status_code == 200):
    with open('./loaded_coins.json','w+') as loaded_coins:
        response = json.loads(loaded_page.content.decode('utf-8'))
        loaded_coins.write(json.dumps(response, indent=4, sort_keys=True))

        print('%(coins_length)s coins loaded and saved to file.' % { 'coins_length': len(response['Data']) })

        coins = response['Data']
        for key, coin in coins.items():
            if(not 'ImageUrl' in coin):
                coin['ImageUrl'] = ''

            result = client.execute('''
            mutation {
                createCryptoCoin(
                    cId: "%(Id)s",
                    algorithm: "%(Algorithm)s",
                    coinName: "%(CoinName)s",
                    fullName: "%(FullName)s",
                    fullyPremined: "%(FullyPremined)s",
                    imageUrl: "%(ImageUrl)s",
                    name: "%(Name)s",
                    preMinedValue: "%(PreMinedValue)s",
                    proofType: "%(ProofType)s",
                    sortOrder: %(SortOrder)s,
                    symbol: "%(Symbol)s",
                    totalCoinsFreeFloat: "%(TotalCoinsFreeFloat)s",
                    totalCoinSupply: "%(TotalCoinSupply)s",
                    url: "%(Url)s"){
                        id
                        fullName
                    }
            }
            '''
            % { 
                'Id': coin['Id'],
                'Algorithm': coin['Algorithm'],
                'CoinName': coin['CoinName'],
                'FullName': coin['FullName'],
                'FullyPremined': coin['FullyPremined'],
                'ImageUrl': coin['ImageUrl'],
                'Name': coin['Name'],
                'PreMinedValue': coin['PreMinedValue'],
                'ProofType': coin['ProofType'],
                'SortOrder': coin['SortOrder'],
                'Symbol': coin['Symbol'],
                'TotalCoinsFreeFloat': coin['TotalCoinsFreeFloat'],
                'TotalCoinSupply': coin['TotalCoinSupply'],
                'Url': coin['Url']
            })

            result = json.loads(result)
            if('errors' in result):
                print('Coin - %(crypto_coin)s - failed to create!' % { 'crypto_coin' : coin['FullName'] })
            else:
                print('Coin - %(crypto_coin)s - created!' % { 'crypto_coin' : result['data']['createCryptoCoin']['fullName'] })


       

