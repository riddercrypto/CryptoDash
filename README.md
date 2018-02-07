# CryptoDash
Crypto Challenge 2018 in Dash framework

-- cron job
in terminal: crontab -e volgende regel toevoegen:
/10 * * * * cd /home/wouter/PycharmProjects/Dash && dashvenv/bin/python balance.py

# /10 * * * * betekent dat de job elke 10 minuten loopt
# cd /home/wouter/PycharmProjects/Dash navigeer naar de project folder
# && dashvenv/bin/python balance.py nadat er naar de map is genavigeert activeer the de python van de virtual environment en run je de pythont file
