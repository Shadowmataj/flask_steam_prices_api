# from decorators import time_decorator
from steamscraping import SteamScraper

steam_scraper = SteamScraper()

def scrapper_process():

    steam_scraper.last_scraped_data()
    steam_scraper.scrap_games_price()
    steam_scraper.close_driver()


scrapper_process()
