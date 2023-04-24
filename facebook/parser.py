# https://www.facebook.com/elvira.aleinichenko
# 100013926015392
# anton14131211

import pickle

from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests
import urllib.request
from selenium import webdriver

new_name = ""
last_posts = []
count_p = 0
count_t = 0
count_v = 0

posts = []


class Parser:
    def open_site(self, browser, graf):
        global new_name

        browser.get('https://www.facebook.com/')  # открываем главную фэйсбука

        time.sleep(50)  # Ждём 50 сек, т.к с впн медленее

        try:
            browser.execute_script(f"window.open('{graf.grafic.reference}', '_self')")

            WebDriverWait(browser, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='x78zum5 xdt5ytf x1wsgfga x9otpla']")))
            new_name = browser.find_element(By.XPATH, "//div[@class='x78zum5 xdt5ytf x1wsgfga x9otpla']").text
            print(new_name)
        except:
            pass

        if new_name == "":
            new_name = "Неопределённая страница в facebook"

    def download_images(self, browser, path):  # метод, скачивающий картинки

        global last_posts, posts
        from selenium.webdriver.common.action_chains import ActionChains
        # Открываем вкладку с сайтом https://vk.com/...
        time.sleep(3)

        # Загружаем посты с изображениями
        posts = browser.find_elements(By.XPATH,
                                      "//a [@class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lliihq x1pdlv7q']//img")
        sec_posts = browser.find_elements(By.XPATH, "//div[@class = 'x6ikm8r x10wlt62 x10l6tqk']//img")
        posts += sec_posts
        print(posts)

        # Отсоединение уже скачанных постов от не
        posts2 = [i for i in posts if i not in last_posts]
        last_posts += posts
        posts = posts2

        # Переменная для названия файлов
        global count_p

        print(f"Загружено постов с фото - {len(posts)} ")
        print(f"Всего обработано {count_p} картинок")

        print(path)

        # Прохождение по картинкам и их скачивание
        for post in posts:
            # Скачивание картинки
            urllib.request.urlretrieve(str(post.get_attribute("src")), str(path) + f"/{str(count_p)}_photo.jpg")
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

        # Загружаем посты с изображениями
        posts = browser.find_elements(By.XPATH,
                                      "//div[@class='x1iorvi4 x1pi30zi x1swvt13 xjkvuk6']")
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
