
#### Imports ###################################################################

from typing import Sequence
from module.dir_create import dir_create
import requests
import json
import os

from module import read_text, f_get_session, dir_create, timestamp, write_event_logs_to_db




#### DoingDutyToDo #############################################################

# read in password for fritzbox authentication
password = read_text("~/.fritzpw").replace("\n", "")

# initialize session
info = f_get_session(password=password)

# make data request using session info
res = requests.post(
  url = 'http://fritz.box/data.lua', 
  data = dict(
    sid         = info.session_id, 
    lang        = "de", 
    page        = "log", 
    no_sidrenew = ""
  )
)

# parse json
json_parsed = json.loads(res.content)
logs        = json_parsed["data"]['log']

# transform date to ISO
for i,x in enumerate(logs):
  logs[i][0] = '20' + logs[i][0][6:8] + '-' + logs[i][0][3:5] + '-' + logs[i][0][0:2]




# prepare logs
logs_list  = [dict(date = x[0], time = x[1], text = x[2], syslog_type = x[3], number = x[4]) for x in logs ]
logs_jsons = [json.dumps(x) for x in logs_list ]
# help for syslogs -->
# https://service.avm.de/help/de/FRITZ-Box-Fon-WLAN-7490/018/hilfe_syslog_XXX


# make sure log directory exists
dir_create("~/logs", ignore_exists=True)
dir_create("~/logs/connection_logs", ignore_exists=True)
dir_create("~/logs/connection_logs_db", ignore_exists=True)


# write to file
path = os.path.expanduser("~/logs/connection_logs/")
with open( path + timestamp("%Y-%m-%d_%H%M%S") + "_logs.jsonl", mode = "w") as f:
  f.write('\n'.join(logs_jsons))



# insert into database
write_event_logs_to_db(logs = logs, path = "~/logs/connection_logs_db/logs.db")




