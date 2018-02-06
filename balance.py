from binance.client import Client
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import datetime as dt

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

knights = get_knights()
get_balances_all_knights()