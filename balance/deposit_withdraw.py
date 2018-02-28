from binance.client import Client
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://crypto:knight@localhost:5432/crypto')
df_client = pd.read_sql_table('knights', engine)


#### DEPOSITS ####
knights_deposits_usd = []

for p, s in zip(df_client.publicapi, df_client.secretapi):
    client = Client(p,s)
    deposits = client.get_deposit_history()
    dep_list = deposits.get('depositList')

    if not dep_list:
        total_dep_usd = 0
        knights_deposits_usd.append(total_dep_usd)

    else:
        df_d = pd.DataFrame(dep_list)
        dep_list_usd = []

        for amount, asset, insertTime in zip(df_d.amount, df_d.asset, df_d.insertTime):
            if not asset == 'BTC':
                asset += 'BTC'
                start_ts = insertTime
                end_ts = start_ts + 60000
                btc_price_list = client.get_klines(symbol=asset, interval='1m', limit=1, startTime=start_ts, endTime=end_ts)[0]
                btc_price = float(btc_price_list[1])
                btc_deposit = btc_price * amount

                price_list = client.get_klines(symbol='BTCUSDT', interval='1m', limit=1, startTime=start_ts, endTime=end_ts)[0]
                price = float(price_list[1])
                usd_deposit = int(price * btc_deposit)
                dep_list_usd.append(usd_deposit)

            else:
                asset += 'USDT'
                start_ts = insertTime
                end_ts = start_ts + 60000
                price_list = client.get_klines(symbol=asset, interval='1m', limit=1, startTime=start_ts, endTime=end_ts)[0]
                price = float(price_list[1])
                usd_deposit = int(price * amount)
                dep_list_usd.append(usd_deposit)

        total_dep_usd = sum(dep_list_usd)
        knights_deposits_usd.append(total_dep_usd)


#### WITDRAWS ####
knights_withdraws_usd = []

for p, s in zip(df_client.publicapi, df_client.secretapi):
    client = Client(p,s)
    withdraws = client.get_withdraw_history()
    wit_list = withdraws.get('withdrawList')

    if not wit_list:
        total_wit_usd = 0
        knights_withdraws_usd.append(total_wit_usd)

    else:
        df_w = pd.DataFrame(wit_list)
        wit_list_usd = []

        for amount, asset, applyTime in zip(df_w.amount, df_w.asset, df_w.applyTime):
            if not asset == 'BTC':
                asset += 'BTC'
                start_ts = applyTime
                end_ts = start_ts + 60000
                btc_price_list = client.get_klines(symbol=asset, interval='1m', limit=1, startTime=start_ts, endTime=end_ts)[0]
                btc_price = float(btc_price_list[1])
                btc_withdraw = btc_price * amount

                price_list = client.get_klines(symbol='BTCUSDT', interval='1m', limit=1, startTime=start_ts, endTime=end_ts)[0]
                price = float(price_list[1])
                usd_withdraw = int(price * btc_withdraw)
                wit_list_usd.append(usd_withdraw)

            else:
                asset += 'USDT'
                start_ts = applyTime
                end_ts = start_ts + 60000
                price_list = client.get_klines(symbol=asset, interval='1m', limit=1, startTime=start_ts, endTime=end_ts)[0]
                price = float(price_list[1])
                usd_withdraw = int(price * amount)
                wit_list_usd.append(usd_withdraw)


        total_wit_usd = sum(wit_list_usd)
        knights_withdraws_usd.append(total_wit_usd)


#### NET_DEPOSIT_FACTOR ####
df_sum = pd.DataFrame(df_client['name'])
df_sum['deposit_usd'] = knights_deposits_usd
df_sum['withdraw_usd'] = knights_withdraws_usd
df_sum['deposit_net'] = (df_sum['deposit_usd'] - df_sum['withdraw_usd'])
df_sum['deposit_factor'] = (df_sum['deposit_usd'] - df_sum['withdraw_usd'])/100


#### WRITE TO TABLE ####
df_sum.to_sql('deposits', engine, if_exists = 'replace')
