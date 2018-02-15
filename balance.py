from binance.client import Client
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import datetime as dt
from coinmarketcap import Market

def edit_symbol(x):
    x = x.split(' ')[0]
    x = x[:-3]
    return x

def get_knights():
    """ query data from the knihgts table """
    conn = psycopg2.connect("dbname='cryptoChallenge' user='postgres' host='localhost' password=''")
    cur = conn.cursor()
    cur.execute("SELECT * FROM knights ORDER BY id ASC")
    knights = cur.fetchall()
    return knights


def get_balances_all_knights():
    """ Functie om de actuele asset stand op te halen en in de database te schrijven """
    for knight in knights:
    # set de client om met de binance te praten
        client = Client(knight[2],knight[3])
    # get balance informatie en stop deze in een dataframe
        account = client.get_account()
        balances = account.get('balances')
        df = pd.DataFrame(balances)
    # Maak van de kolommen 'free' en 'locked' float waardes en tel deze bij elkaar op in een nieuwe kolom genaamd 'amount'
        df.free = df.free.astype(float)
        df.locked = df.locked.astype(float)
        df['amount'] = df['free'] + df['locked']
        df.amount = df.amount.astype(float)
    # verwijder de kolommen 'free' en 'locked'
        del df['free']
        del df['locked']
    # transponeer de tabel zodat elke asset zijn eigen kolom heeft en maak een extra kolom aan voor de datetime.now()
        df = df.set_index('asset').T
        df['datetime'] = dt.datetime.now()
    # maak een connectie met de database en update de tabel voor de knight
        engine = create_engine('postgresql://postgres:@localhost:5432/cryptoChallenge')
        df.to_sql(knight[1], engine, if_exists = 'append', index = False )

def total_balance_USD():
    """ functie om de totale waarde van de portfolio per knight in een tabel te schrijven """
    # Set Client and get token balances
    for knight in knights:
    # set de client om met de binance te praten
        client = Client(knight[2],knight[3])
    # get balance informatie en stop deze in een dataframe
        account = client.get_account()
        balances = account.get('balances')
        df = pd.DataFrame(balances)
    # Maak van de kolommen 'free' en 'locked' float waardes en tel deze bij elkaar op in een nieuwe kolom genaamd 'amount'
        df.free = df.free.astype(float)
        df.locked = df.locked.astype(float)
        df['amount'] = df['free'] + df['locked']
        df['amount'] = df['amount'].apply(pd.to_numeric)
    # verwijder de kolommen 'free' en 'locked'
        del df['free']
        del df['locked']
    # bitcoinprice van marketcap
        coinmarketcap = Market()
        btc = coinmarketcap.ticker('bitcoin', convert = 'EUR')
        btcusd = btc[0]['price_usd']
        btcusdfloat = float(btcusd)
    # Get price per token
        prices = client.get_all_tickers()
        dfp = pd.DataFrame(prices)
        dfp2 = dfp.loc[dfp['symbol'].str[-3:] == 'BTC']
        dfp2.loc[:,'asset']=dfp2['symbol'].apply(edit_symbol)
        del dfp2['symbol']
    # merge prices per token with balances and get balance per token in BTC
        merged_df = df.merge(dfp2, how='left', on="asset")
        merged_df['price'] = merged_df['price'].apply(pd.to_numeric)
        merged_df.loc[merged_df['asset'] == 'BTC', 'price'] = 1
        merged_df["total"] = merged_df['amount'] * merged_df['price']
        Totaal = merged_df['total'].sum()
        knight = knight[0]
        knightint = int(knight)
        usd = Totaal * btcusdfloat
        datetime = dt.datetime.now()
        conn = psycopg2.connect("dbname='cryptoChallenge' user='postgres' host='localhost' password=''")
        cur = conn.cursor()
        cur.execute("INSERT INTO public.total (knight, btc, btcusd, usd, datetime) VALUES (%s, %s, %s , %s, %s)", (knightint,Totaal,btcusdfloat,usd, datetime))
        conn.commit()



knights = get_knights()
get_balances_all_knights()
total_balance_USD()