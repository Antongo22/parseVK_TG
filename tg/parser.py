# 14131211Anton
import pickle

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import urllib.request
from selenium.webdriver.common.alert import Alert

new_name = ""
last_posts = []
count_p = 0
count_t = 0
count_v = 0
tr = False
posts = []


class Parser:

    def open_site(self, browser, graf):

        global new_name
        # Открываем вкладку с сайтом https://vk.com/feed

        browser.get('https://web.telegram.org/z/')

        # Ждем 40 секунд
        time.sleep(30)

        print(graf.grafic.reference)
        try:

            browser.execute_script(f"window.open('{graf.grafic.reference}', '_self')")

            WebDriverWait(browser, 20).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='ChatInfo']")))
            new_name = browser.find_element(By.XPATH, "//div[@class='ChatInfo']").text
            print(new_name)

            time.sleep(10)

        except Exception as e:
            print("Произошла ошибка\n" + e)

        if new_name == "":
            new_name = "Неопределённая группа в telegram"

    def download_images(self, browser, path):  # метод, скачивающий картинки
        import re
        global last_posts, posts
        from selenium.webdriver.common.action_chains import ActionChains
        # Открываем вкладку с сайтом https://vk.com/...
        time.sleep(3)

        # WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,
        #                                                                 "//a[@class='wall_text']//img")))

        while True:
            browser.execute_script("window.scrollBy(0, -2000)")
            end_of_page = browser.execute_script(
                "return (window.pageYOffset <= 0)")

            if end_of_page:
                break

        # Загружаем посты с изображениями
        posts = browser.find_elements(By.XPATH,
                                      "//div[@class='page_post_sized_thumbs clear_fix']//a")
        print(posts)

        # Отсоединение уже скачанных постов от не
        posts2 = [i for i in posts if i not in last_posts]
        last_posts += posts
        posts = posts2

        # Переменная для названия файлов
        global count_p

        print(f"Загружено постов с фото - {len(posts)} ")
        print(f"Всего обработано {count_p} картинок")

        # Прохождение по картинкам и их скачивание
        for post in posts:
            print(str(post.get_attribute("style")))
            # Скачивание картинки
            url = re.findall(r'(https?://\S+)', str(post.get_attribute("style")))[0]
            urllib.request.urlretrieve(url, str(path) + f"/{str(count_p)}_photo.jpg")
            count_p += 1
            actions = ActionChains(browser)
            time.sleep(2)

            # Скрол к картинке
            browser.execute_script("window.scrollBy(0, 300)")
            actions.move_to_element(post).perform()
            time.sleep(3)

        # Доп скрол
        browser.execute_script("window.scrollBy(0, 2000)")

    def download_text(self, browser, path):  # Метод, скачивающий текст
        global last_posts
        from selenium.webdriver.common.action_chains import ActionChains
        # Открываем вкладку с сайтом https://vk.com/...
        time.sleep(3)

        # WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,
        #                                                                 "//a[@class='wall_text']//img")))

        while True:
            browser.execute_script("window.scrollBy(0, -2000)")
            end_of_page = browser.execute_script(
                "return (window.pageYOffset <= 0)")

            if end_of_page:
                break

        # Загружаем посты с изображениями
        posts = browser.find_elements(By.XPATH,
                                      "//div[@class='im-mess--text wall_module _im_log_body']")
        print(posts)

        # Отсоединение уже скачанных постов от не
        posts2 = [i for i in posts if i not in last_posts]
        last_posts += posts
        posts = posts2

        # Переменная для названия файлов
        global count_t

        print(f"Загружено постов с текстом - {len(posts)} ")
        print(f"Всего обработано {count_t} текстовых поста")

        # Прохождение по картинкам и их скачивание
        for post in posts:
            # Скачивание картинки

            file = open(path, "a")

            # print(str(path))

            # print(str(post.text))
            # f"{str(count_p)}\n" + str(post.text) + "\n\n"

            file.write(f"{str(count_t)}\n" + str(post.text) + "\n\n")

            count_t += 1
            actions = ActionChains(browser)
            time.sleep(2)

            # Скрол к картинке
            browser.execute_script("window.scrollBy(0, 300)")
            actions.move_to_element(post).perform()
            time.sleep(3)

        # Доп скрол
        browser.execute_script("window.scrollBy(0, 2000)")

    def download_videos(self, browser, path):
        global last_posts
        from selenium.webdriver.common.action_chains import ActionChains
        # Открываем вкладку с сайтом https://vk.com/...
        time.sleep(3)

        # WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,
        #                                                                 "//a[@class='wall_text']//img")))

        # Загружаем посты с изображениями
        posts = browser.find_elements(By.XPATH,
                                      "//div[@class='page_post_sized_thumbs  clear_fix']//a")
        print(posts)

        # Отсоединение уже скачанных постов от не
        posts2 = [i for i in posts if i not in last_posts]
        last_posts += posts
        posts = posts2

        # Переменная для названия файлов
        global count_v

        print(f"Загружено постов с вилео - {len(posts)} ")
        print(f"Всего обработано {count_v} видео")

        # Прохождение по видео и их скачивание
        for post in posts:
            # Скачивание картинки
            # urllib.request.urlretrieve(str(post.get_attribute("href")), str(path) + f"/{str(count_p)}.mp4")
            # print(str(post.get_attribute("href")))

            import youtube_dl

            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([str(post.get_attribute("href"))])

            count_v += 1
            actions = ActionChains(browser)
            time.sleep(2)

            # Скрол к картинке
            browser.execute_script("window.scrollBy(0, 300)")
            actions.move_to_element(post).perform()
            time.sleep(3)

        # Доп скрол
        browser.execute_script("window.scrollBy(0, 2000)")

    def end(self, browser):
        browser.quit()
