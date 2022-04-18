"""
Developed By Kareem Mahlees
--------------------------------------
This program is made to manage your watchlist in Notion via automating the most 
possible tasks like fetching the data , inserting it into a notion page and sorting the watched and unwatched
movies and tv shows
"""

import os
import _Constants
from NotionApi import NotionClient
from keep_alive import keep_alive

# -------------------------------------
os.system("cls" if os.name == "nt" else "clear")
print("Monitoring..")
try:
    client = NotionClient(_Constants.NOTION_TOKEN, _Constants.DATABASE_ID)
    keep_alive()
    client.monitor_the_database()
except KeyboardInterrupt:
    print("Closed Program !")
# ------------------------------------
