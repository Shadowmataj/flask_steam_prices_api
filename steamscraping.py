from tabulate import tabulate
from time import sleep
from datetime import datetime

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas
from selenium.webdriver.support.ui import Select

TIME_TO_SLEEP = 1


class SteamScraper:
    """Main steam scrapper class"""
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option(name="detach", value=True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrap_games_price(self) -> None:
        """Function to get list of the games to  search"""
        game_info_list = []
        with open("games_list.csv") as csv_file:
            file = pandas.read_csv(csv_file)
            for index, row in file.iterrows():
                game_info = self.scrap_game(row["link"])
                game_info_list += game_info
        headers = ["game", "price", "currency", "relase_date"]
        rows = [element.values() for element in game_info_list]

        df1 = pandas.DataFrame(rows, columns=headers)

        today=datetime.today()
        df1.to_csv(f"csv/games_info_{today.strftime('%x').replace('/','-')}.csv")
        headers = ["index"]+ headers
        print(tabulate(rows, headers=headers, tablefmt='double_outline', showindex=True))


    def scrap_game(self, link:str) -> list:
        """Scrap main function."""
        game = link.split("/")[-1].replace("__", ": ").replace("_", " ").title()
        print(f"******************************** Cheking: {game} ********************************")
        game_info_list = []
        release_date = False
        try:
            print("Age Checker:", end=" ")
            self.driver.get(link)
            sleep(TIME_TO_SLEEP)
            day_selector  = Select(self.driver.find_element(By.ID, "ageDay"))
            month_selector = Select(self.driver.find_element(By.ID, "ageMonth"))
            year_selector = Select(self.driver.find_element(By.ID, "ageYear"))
            print("Age Check required.")
            print("View Page Button Checker:", end=" ")
        except NoSuchElementException:
            print("No Age Check required.")
            try:
                print("View Page Button Checker:",end=" ")
                view_page_button = self.driver.find_element(By.ID, "view_product_page_btn")
                view_page_button.click()
            except NoSuchElementException:
                print("No View Page Button Check required.")
                pass
        else:
            day_selector.select_by_value("22")
            month_selector.select_by_value("September")
            year_selector.select_by_value("1993")
            view_page_button = self.driver.find_element(By.ID, "view_product_page_btn")
            view_page_button.click()
            print("View Page Button Check required.")

        sleep(TIME_TO_SLEEP)

        try:
            print("Release date checker:", end=" ")
            coming_soon = self.driver.find_element(By.XPATH, '//*[@class="game_area_comingsoon game_area_bubble"]/div/h1')
        except NoSuchElementException:
            print("The game has been release already!")
        else:
            print(coming_soon.text)
            release_date = coming_soon.text
        finally:
            print("Checkers resolved, continue...")

        game_names = self.driver.find_elements(By.XPATH, '//*[@class="game_area_purchase_game_wrapper"]/div/h2')
        game_price = self.driver.find_elements(By.CLASS_NAME, 'game_purchase_price')
        print(f"******************************** Finished: {game} ********************************", end="\n\n\n")

        if release_date and "prevista" in release_date:
            game_dict = {"game_name": game,
                         "game_price": "N/A",
                         "currency": "N/A",
                         "release_date": f"Previsto: {release_date.split(' ')[-1]}"}
            game_info_list.append(game_dict)
        else:
            for row in range(len(game_names)):
                game_dict = {"game_name": game_names[row].text.replace("Buy ", ""), "game_price": game_price[row].text.split(" ")[1], "currency": game_price[row].text.split(" ")[0], "release_date": "nan"}
                if release_date:
                    game_dict["release_date"] = release_date.replace("Lanzamiento: ", "")
                game_info_list.append(game_dict)

        return game_info_list

    def last_scraped_data(self) -> None:
        with open("csv/games_info_02-15-25.csv") as csv_file:
            df = pandas.read_csv(csv_file)
            print(tabulate(df, headers="keys", tablefmt='double_outline', showindex=False))

    def close_driver(self) -> None:
        self.driver.close()
