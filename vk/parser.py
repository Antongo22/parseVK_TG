from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests
import urllib.request
#
# from program.loop_program import browser, new_folder_path

# url = "https://vk.com/"
# response = requests.get(url)
# print(response.text)


wh = True
new_name = ""
last_posts = []
count = 0
tr = False


class Parser:

    def open_site(self, browser, graf):

        global new_name
        # Открываем вкладку с сайтом https://vk.com/feed
        browser.get('https://vk.com/feed')

        # Ждем 30 секунд
        time.sleep(25)

        browser.execute_script(f"window.open('{graf.grafic.reference}', '_self')")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//h1[@class='page_name']")))
        new_name = browser.find_element(By.XPATH, "//h1[@class='page_name']").text

    def download_images(self, browser, path):
        try:
            global last_posts
            global wh
            from selenium.webdriver.common.action_chains import ActionChains
            # Открываем вкладку с сайтом https://vk.com/...
            time.sleep(3)

            # WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,
            #                                                                 "//a[@class='wall_text']//img")))
            posts = browser.find_elements(By.XPATH,
                                          "//div[@class='MediaGridContainerWeb--post']//img")
            print(posts)
            print(wh)
            posts2 = [i for i in posts if i not in last_posts]
            last_posts += posts
            posts = posts2

            if posts == []:
                raise Exception("Some exception")

            global count

            for post in posts:
                urllib.request.urlretrieve(str(post.get_attribute("src")), str(path) + f"/{str(count)}.jpg")
                count += 1
                actions = ActionChains(browser)
                time.sleep(2)
                browser.execute_script("window.scrollBy(0, 300)")
                actions.move_to_element(post).perform()
                time.sleep(3)

            browser.execute_script("window.scrollBy(0, 2000)")
        except Exception:
            wh = False
