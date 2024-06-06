import sqlite3
import os

#CONSTANTS
DATA_BASE = 'gpt.db'
MAX_ID = "SELECT MAX(vidId) FROM Videos"
GPT_SCRIPT_FILE = 'gpt.py'
VIDS_DIR_NAME = 'seriesOfVideos'
READ_MODE = 'r'
INSERT_DATA_INTO_TABLE = "INSERT INTO Videos VALUES (?, ?, ?, ?)"
UNICODE_FORMAT = 'utf-8'


#Updating the database
conn = sqlite3.connect(DATA_BASE)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())

# Get the maximum vidId from the Videos table
c.execute(MAX_ID)
result = c.fetchone()
vidId = result[0] if result[0] is not None else 0

script_path = os.path.dirname(os.path.abspath(GPT_SCRIPT_FILE))
vid_dir_path = os.path.join(script_path, VIDS_DIR_NAME)
files = os.listdir(vid_dir_path)

#Updating the database
for file in files:
  vidId += 1
  completed_path = os.path.join(vid_dir_path, file)
  with open(completed_path, READ_MODE, encoding = UNICODE_FORMAT) as file_op:

    vidName = file_op.readline().strip()
    vidLink = file_op.readline().strip()
    vidText = ''.join(file_op.readlines())
    c.execute(INSERT_DATA_INTO_TABLE, (vidId, vidName, vidText, vidLink))
  conn.commit()

#Removing the same videos

