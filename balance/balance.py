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
    conn = psycopg2.connect("dbname='crypto' user='crypto' host='localhost' password='knight'")
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
    # Maak van de kolommen 'free' en 'locked' float waardes en tel deze bij elkaar op in een nieuwe kolom genaamd 'amount'
        df = pd.DataFrame(balances)
        df.free = df.free.astype(float)
        df.locked = df.locked.astype(float)
        df['amount'] = df['free'] + df['locked']
        df.amount = df.amount.astype(float)
    # verwijder de kolommen 'free' en 'locked'
        del df['free']
        del df['locked']

    # Maak van de kolommen 'free' en 'locked' float waardes en tel deze bij elkaar op in een nieuwe kolom genaamd 'amount'
        dft = pd.DataFrame(balances)
        dft.free = dft.free.astype(float)
        dft.locked = dft.locked.astype(float)
        dft['amount'] = dft['free'] + dft['locked']
        dft['amount'] = dft['amount'].apply(pd.to_numeric)
    # verwijder de kolommen 'free' en 'locked'
        del dft['free']
        del dft['locked']

    # bitcoinprice van marketcap
        coinmarketcap = Market()
        btc = coinmarketcap.ticker('bitcoin', convert = 'USD')
        btcusd = btc[0]['price_usd']
        btcusdfloat = float(btcusd)
    # Get price per token
        prices = client.get_all_tickers()
        dfp = pd.DataFrame(prices)
        dfp2 = dfp.loc[dfp['symbol'].str[-3:] == 'BTC']
        dfp2.loc[:,'asset']=dfp2['symbol'].apply(edit_symbol)
        del dfp2['symbol']
    # merge prices per token with balances and get balance per token in BTC
        merged_df = dft.merge(dfp2, how='left', on="asset")
        merged_df['price'] = merged_df['price'].apply(pd.to_numeric)
        merged_df.loc[merged_df['asset'] == 'BTC', 'price'] = 1
        merged_df["total"] = merged_df['amount'] * merged_df['price']
        Totaal = merged_df['total'].sum()

    # transponeer de tabel zodat elke asset zijn eigen kolom heeft en maak een extra kolom aan voor de datetime.now()
        df = df.set_index('asset').T
        df['datetime'] = dt.datetime.now()
        df['total_btc'] = merged_df['total'].sum()
        df['total_usd'] = Totaal * btcusdfloat
        df['btc_usd'] = btcusdfloat
    # maak een connectie met de database en update de tabel voor de knight
        engine = create_engine('postgresql://crypto:knight@localhost:5432/crypto')
        df.to_sql(knight[1], con=engine, if_exists = 'append', index = False )


knights = get_knights()
get_balances_all_knights()
