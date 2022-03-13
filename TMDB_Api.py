"""
This is a code that simply utilises the TMDB api to fetch various data about a movie or tv show
"""

import json
import requests


class TMDB_Client:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json;charset=utf-8",
        }

    def search_for_movie(self, movie_name):
        request_url = f"https://api.themoviedb.org/3/search/movie?api_key={self.token}&query={movie_name.replace(' ','+')}"
        res = requests.get(request_url)
        res_JSON = json.dumps(res.json())
        res_dict = json.loads(res_JSON)
        self.movie_id = res_dict["results"][0]["id"]
        # if len(res_dict["results"]) > 2:
        #     for num, element in enumerate(res_dict["results"], 1):
        #         print(f'{num}-{element["original_title"]}')
        #     print("#" * 50)
        #     prompt = int(input("Which one ? "))
        #     self.movie_id = res_dict["results"][prompt - 1]["id"]
        # else:
        #     self.movie_id = res_dict["results"][0]["id"]

    def get_movie_details(self):
        res = requests.get(
            f"https://api.themoviedb.org/3/movie/{self.movie_id}?api_key={self.token}"
        )
        res_JSON = json.dumps(res.json())
        res_dict = json.loads(res_JSON)
        # -------------------------------------------------------------
        self.genres_list_m = [_["name"] for _ in res_dict["genres"]]
        self.release_date_m = res_dict["release_date"]
        self.runtime_m = res_dict["runtime"]
        self.statues_m = res_dict["status"]
        self.tagline_m = res_dict["tagline"]
        self.original_title_m = res_dict["original_title"]
        self.poster_m = (
            f"https://www.themoviedb.org/t/p/original{res_dict['poster_path']}"
        )
        self.backdrop_m = (
            f"https://www.themoviedb.org/t/p/original{res_dict['backdrop_path']}"
        )

    def search_for_tv_show(self, Show_name):
        request_url = f"https://api.themoviedb.org/3/search/tv?api_key={self.token}&query={Show_name.replace(' ','+')}"
        res = requests.get(request_url)
        res_JSON = json.dumps(res.json())
        res_dict = json.loads(res_JSON)
        self.show_id = res_dict["results"][0]["id"]

    def get_show_details(self):
        res = requests.get(
            f"https://api.themoviedb.org/3/tv/{self.show_id}?api_key={self.token}"
        )
        res_JSON = json.dumps(res.json())
        res_dict = json.loads(res_JSON)
        # ----------------------------------------------------------------
        self.release_date_s = res_dict["first_air_date"]
        self.statues_s = res_dict["status"]
        self.poster_s = (
            f"https://www.themoviedb.org/t/p/original{res_dict['poster_path']}"
        )
        self.original_name = res_dict["original_name"]
        self.number_of_seasons = res_dict["number_of_seasons"]
        self.number_of_episodes = res_dict["number_of_episodes"]
        self.tagline_s = res_dict["tagline"]
        self.genres_list_s = [_["name"] for _ in res_dict["genres"]]
        self.statues_m = res_dict["status"]
        self.backdrop_s = (
            f"https://www.themoviedb.org/t/p/original{res_dict['backdrop_path']}"
        )
