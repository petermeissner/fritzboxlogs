import os
import sqlite3
from typing import List


def write_event_logs_to_db(logs: List[List], path: str) -> None:

  # prepare path
  path = os.path.expanduser(path)
  
  # establkish connection to database
  con  = sqlite3.connect(path)
  cur  = con.cursor()


  # Create table
  cur.execute('''CREATE TABLE IF NOT EXISTS 
                logs 
                (
                  date text, 
                  time text, 
                  message text, 
                  syslog_type integer, 
                  number integer
                )
                ;
  ''')

  cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS 
                  logs_date_time_syslog_type 
                  ON 
                  logs (date, time, syslog_type)
                  ;
  ''')

  con.commit()

  # Insert a row of data
  cur.executemany('''INSERT OR IGNORE INTO 
                      logs 
                      (date, time, message, syslog_type, number) 
                      VALUES 
                      (?, ?, ?, ? , ?)
                      ;
                    ''', 
                    [x[0:5] for x in logs]
  )

  # Save (commit) the changes
  con.commit()

  # close things
  cur.close()
  con.close()
