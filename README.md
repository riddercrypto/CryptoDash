#https://moderndata.plot.ly/create-a-plotly-dashboards-in-under-10-minutes/

# CryptoDash
Crypto Challenge 2018 in Dash framework

# cron job
- Terminal: crontab -e 
- volgende regel aan de file toevoegen toevoegen:
/10 * * * * cd /home/wouter/PycharmProjects/Dash && dashvenv/bin/python balance.py
  - Stel de frequentie van de job in: /10 * * * * 
  - Navigeer naar de project folder: cd /home/wouter/PycharmProjects/Dash 
  - Run python vanuit je virtualenv, open de file: && dashvenv/bin/python balance.py
