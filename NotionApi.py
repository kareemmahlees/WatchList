"""
This is a code that simply utilises the Notion api to post data into the app fetched from TMDB api 
"""

import json
import requests
from TMDB_Api import TMDB_Client
import time
import _Constants


class NotionClient:
    def __init__(self, TOKEN, DATABASE_ID) -> None:
        self.token = TOKEN
        self.database_id = DATABASE_ID
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16",
        }

    def monitor_the_database(self):
        while True:  # Event loop
            time.sleep(0.25)
            res = requests.post(
                f"https://api.notion.com/v1/databases/{self.database_id}/query",
                headers=self.headers,
            )
            data_json = json.dumps(res.json())
            data_dict = json.loads(data_json)
            for element in data_dict["results"]:
                try:
                    scheme = element["properties"]["Name"]["title"][0]["text"][
                        "content"
                    ]
                except IndexError:
                    continue
                try:
                    if (
                        scheme.endswith(";")
                        and element["properties"]["Type"]["select"]["name"] == "Movie"
                    ):
                        self.page_id = element["id"]
                        self.movie_name = scheme[: len(scheme) - 1]
                        self.patch_movie()
                    elif (
                        scheme.endswith(";")
                        and element["properties"]["Type"]["select"]["name"] == "Tv Show"
                    ):
                        self.page_id = element["id"]
                        self.show_name = scheme[: len(scheme) - 1]
                        self.patch_tv_show()
                except TypeError:
                    continue

    def patch_movie(self):
        patch_url = f"https://api.notion.com/v1/pages/{self.page_id}"
        client_TMDB = TMDB_Client(_Constants.TMDB_TOKEN)
        try:
            client_TMDB.search_for_movie(self.movie_name)
            client_TMDB.get_movie_details()
        except:
            data = {
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": "Name Not Found , Try Again.."},
                            }
                        ]
                    },
                }
            }
        else:
            data = {
                "icon": {"type": "external", "external": {"url": client_TMDB.poster_m}},
                "cover": {
                    "type": "external",
                    "external": {"url": client_TMDB.backdrop_m},
                },
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": client_TMDB.original_title_m},
                            }
                        ]
                    },
                    "Genres": {
                        "multi_select": [{"name": _} for _ in client_TMDB.genres_list_m]
                    },
                    "Release Date": {
                        "rich_text": [{"text": {"content": client_TMDB.release_date_m}}]
                    },
                    "Runtime": {"number": round(client_TMDB.runtime_m / 60, 1)},
                    "Statues": {"select": {"name": client_TMDB.statues_m}},
                    "Tag Line": {
                        "rich_text": [{"text": {"content": client_TMDB.tagline_m}}]
                    },
                    "Watch Statues": {"select": {"name": "Unwatched"}},
                    "Cover": {
                        "files": [
                            {
                                "type": "external",
                                "name": "Poster",
                                "external": {"url": client_TMDB.poster_m},
                            }
                        ]
                    },
                },
            }
        data = json.dumps(data)
        requests.patch(url=patch_url, headers=self.headers, data=data)

    def patch_tv_show(self):
        patch_url = f"https://api.notion.com/v1/pages/{self.page_id}"
        client_TMDB = TMDB_Client(_Constants.TMDB_TOKEN)
        try:
            client_TMDB.search_for_tv_show(self.show_name)
            client_TMDB.get_show_details()
        except:
            data = {
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": "Name Not Found , Try Again.."},
                            }
                        ]
                    },
                }
            }
        else:
            data = {
                "icon": {"type": "external", "external": {"url": client_TMDB.poster_s}},
                "cover": {
                    "type": "external",
                    "external": {"url": client_TMDB.backdrop_s},
                },
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": client_TMDB.original_name},
                            }
                        ]
                    },
                    "Genres": {
                        "multi_select": [{"name": _} for _ in client_TMDB.genres_list_s]
                    },
                    "Watch Statues": {"select": {"name": "Unwatched"}},
                    "Tag Line": {
                        "rich_text": [{"text": {"content": client_TMDB.tagline_s}}]
                    },
                    "Seasons": {"number": client_TMDB.number_of_seasons},
                    "Episodes": {"number": client_TMDB.number_of_episodes},
                    "Statues": {"select": {"name": client_TMDB.statues_s}},
                    "Release Date": {
                        "rich_text": [{"text": {"content": client_TMDB.release_date_s}}]
                    },
                    "Cover": {
                        "files": [
                            {
                                "type": "external",
                                "name": "Poster",
                                "external": {"url": client_TMDB.poster_s},
                            }
                        ]
                    },
                },
            }
        data = json.dumps(data)
        requests.patch(url=patch_url, headers=self.headers, data=data)
