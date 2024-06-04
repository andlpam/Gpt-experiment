import sqlite3
import os


#Updating the database
conn = sqlite3.connect('gpt.db')
c = conn.cursor()

# Get the maximum vidId from the Videos table
c.execute("SELECT MAX(vidId) FROM Videos")
result = c.fetchone()
vidId = result[0] if result[0] is not None else 0

script_path = os.path.dirname(os.path.abspath('gpt.py'))
vid_dir_path = os.path.join(script_path, 'seriesOfVideos')
files = os.listdir(vid_dir_path)

#Updating the database
for file in files:
  vidId += 1
  completed_path = os.path.join(vid_dir_path, file)
  with open(completed_path, 'r', encoding='utf-8') as file_op:

    vidName = file_op.readline().strip()
    vidLink = file_op.readline().strip()
    vidText = ''.join(file_op.readlines())
    c.execute("INSERT INTO Videos VALUES (?, ?, ?, ?)", (vidId, vidName, vidText, vidLink))
  conn.commit()

