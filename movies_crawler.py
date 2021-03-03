import requests
from bs4 import BeautifulSoup

class Movies:
    def _get_wanna_see_movies_url(self):
        wanna_see_movies_url = []
        text = requests.get("https://movies.yahoo.com.tw/chart.html?cate=exp_30&search_date=30").text
        soup = BeautifulSoup(text, "lxml")
        wanna_see_movies = soup.select_one("div.rank_list").select("div.tr")
        for idx in range(1, 4):
            wanna_see_movies_url.append(wanna_see_movies[idx].select_one("a")["href"])
        return wanna_see_movies_url
    
    def _get_most_like_movies_url(self):
        most_like_movies_url = []
        text = requests.get("https://movies.yahoo.com.tw/chart.html?cate=rating&search_year=30").text
        soup = BeautifulSoup(text, "lxml")
        all_vote = []
        for tag in soup.select_one("div.rank_list").select("div.tr")[1::]:
            all_vote.append(int(tag.select_one("h4").text.split("共")[1].split("人")[0]))
        standard = sorted(all_vote)[-5:][0]
        for tag in soup.select_one("div.rank_list").select("div.tr")[1::]:
            if int(tag.select_one("h4").text.split("共")[1].split("人")[0]) >= standard and len(most_like_movies_url)<3:
                most_like_movies_url.append((tag.select_one("a")["href"]))
        return most_like_movies_url
    
    def _get_movies_info(self, url):
        text = requests.get(url).text
        soup = BeautifulSoup(text, "lxml")
        movie_info = {}
        movie_data = soup.select_one("div.movie_intro_info_r")
        movie_info["name"] = movie_data.select_one("h1").text
        movie_info["trans_name"] = movie_data.select_one("h3").text
        for tag in soup.select("meta")[3:]:
            if str(tag["content"])[-3:] in ["jpg", "png", "jpeg"]:
                movie_info["poster"] = str(tag["content"])
                break
        if movie_data.select_one("span").text.startswith("上映日期"):
            movie_info["release_date"] =  movie_data.select_one("span").text
        else:
            movie_info["release_date"] =  " "
        return movie_info