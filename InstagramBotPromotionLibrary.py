from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import random
import os


class BrowserSurfingPromotion():

    def __init__(self, username, password, path_webdriver):
        """
        :param username: Имя аккаунта
        :param password: Пароль аккаунта
        :param path_webdriver: Путь к webdriver
        """

        self.username = username
        self.password = password
        options = Options()
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(path_webdriver, options=options)

    def close_browser(self):
        """
        Закрытие браузера
        :return: None
        """

        self.browser.close()
        self.browser.quit()

    def login(self):
        """
        Вход в аккаунт

        :return: None
        """

        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)  # имя аккаунта

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)  # пароль аккаунта

        password_input.send_keys(Keys.ENTER)
        time.sleep(15)

    def like_photo_by_hashtag(self, hashtag):
        """
        Проставление лайков по хештегу

        :param hashtag: имя хештега
        :return: None
        """

        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 4):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(3)
                like_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(3, 6))
                # time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.close_browser()

    def xpath_exists(self, url):
        """
        Проверка существование элемента по xpath на текущей страничке браузера

        :param url: xpath
        :return: bool
        """

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def put_exactly_like(self, userpost):
        """
        Проставление лайка по url на пост

        :param userpost: url на пост
        :return: None
        """

        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого поста не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пост успешно найден, ставим лайк!")
            time.sleep(2)

            like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
            browser.find_element_by_xpath(like_button).click()
            time.sleep(2)

            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()

    def get_all_posts_urls(self, userpage):
        """
        Взятие ссылок на все посты пользователя, создает файл

        :param userpage: url пользователя
        :return: None
        """

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пользователь успешно найден, ставим лайки!")
            time.sleep(2)

            posts_count = int(browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

    def put_likes(self, count):
        """
        Проставить count лайков на открытый аккаунт пользователя

        :param count: Количество лайков
        :return: None
        """
        browser = self.browser
        time.sleep(4)

        posts_count = int(browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)

        if posts_count >= 1:
            posts_urls = []
            hrefs = browser.find_elements_by_tag_name('a')
            hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

            for href in hrefs:
                posts_urls.append(href)

            for post_url in posts_urls:
                count -= 1
                try:
                    browser.get(post_url)
                    time.sleep(2)

                    like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                    browser.find_element_by_xpath(like_button).click()

                    print(f"Лайк на пост: {post_url} успешно поставлен!")

                    if count == 0:
                        break
                    else:
                        time.sleep(random.randrange(80, 100))
                except Exception as ex:
                    print(ex)
                    self.close_browser()

    def follow_or_not(self):
        """
        Проверка на то, стоит ли подписываться на данный аккаунт или нет

        :return: 1 or 0
        """
        browser = self.browser

        followers_button = browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        followers_count = followers_button.get_attribute('title')

        # если количество подписчиков больше 999, убираем пробелы
        if ' ' in followers_count:
            followers_count = int(''.join(followers_count.split(' ')))
        followers_count = int(followers_count)

        following_count = browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text

        # если количество подписок больше 999, убираем пробелы
        if ' ' in following_count:
            following_count = int(''.join(following_count.split(' ')))
        following_count = int(following_count)

        posts_count = browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text

        # если количество постов больше 999, убираем пробелы
        if ' ' in posts_count:
            posts_count = int(''.join(posts_count.split(' ')))
        posts_count = int(posts_count)

        user_avatar_button = browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/div/div/span/img')
        user_avatar = user_avatar_button.get_attribute('src')

        counter = 0

        if 's320x320' in user_avatar:
            counter += 0.3

        if followers_count >= 10:
            counter += 0.2

        if (following_count >= 10) and (following_count < 500):
            counter += 0.3

        if posts_count > 3:
            counter += 0.2

        print('Counter is: ', counter)

        if counter >= 0.8:
            return 1
        else:
            return 0

    def follow_followers(self, userpage, count = 200):
        """
        Подписка на подписчиков userpage

        :param userpage: url аккаунта, который используем как источник пользователей для подписок
        :param count: Количество подписок
        :return: None
        """

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        username = userpage.split("/")[-2]

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f"Пользователя {username} не существует, проверьте URL")
            self.close_browser()
        else:

            print(f"Пользователь {username} успешно найден, подписываемся и ставим лайки")
            time.sleep(2)

            # создаём папку для всех фалов связанных с пописками
            if os.path.exists("subscription_unsubscribe"):
                print("Папка subscription_unsubscribe уже существует!")
            else:
                print("Создаём папку пользователя subscription_unsubscribe.")
                os.mkdir('subscription_unsubscribe')

            followers_button = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
            followers_count = followers_button.get_attribute('title')

            # если количество подписчиков больше 999, убираем пробелы
            if ' ' in followers_count:
                followers_count = int(''.join(followers_count.split(' ')))
            else:
                followers_count = int(followers_count)

            print(f"Количество подписчиков: {followers_count}")

            loops_count = int(followers_count / 12)
            print(f"Число итераций: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)

            followers_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")

            try:
                followers_urls = []
                count_of_followers = 0
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")
                    count_of_followers += 12
                    if count_of_followers >= count * 15:
                        break

                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                for user in followers_urls:
                    if count > 0:
                        break
                    try:
                        try:
                            with open('subscription_unsubscribe/all_subscriptions_list.txt',
                                      'r') as all_subscriptions_list_file:
                                lines = all_subscriptions_list_file.readlines()
                                if user in lines:
                                    print(
                                        f'Мы уже подписаны или были подписаны на {user}, переходим к следующему пользователю!')
                                    continue

                        except Exception as ex:
                            print('Файл со ссылками ещё не создан!')
                            print(ex)

                        browser = self.browser
                        browser.get(user)
                        page_owner = user.split("/")[-2]

                        if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/a"):
                            print("Это наш профиль, уже подписан, пропускаем итерацию!")
                        elif self.xpath_exists(
                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button"):
                            print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                        else:

                            if self.xpath_exists(
                                    "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                print('Закрытый аккаунт! Пропускаем')
                                continue
                            else:
                                try:
                                    if self.follow_or_not():

                                        if self.xpath_exists(
                                                '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button'):
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button").click()
                                        elif self.xpath_exists(
                                                '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button'):
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button").click()
                                        time.sleep(random.randrange(2, 4))

                                        self.put_likes(1)
                                        print(
                                            f'Подписались на пользователя {page_owner} и лайкнули 1 его пост. Открытый аккаунт!')

                                        count -= 1

                                        # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                                        with open('subscription_unsubscribe/all_subscriptions_list.txt',
                                                  'a') as all_subscriptions_list_file:
                                            all_subscriptions_list_file.write(user + '\n')

                                        # записываем данные в файл для ссылок сегодняшнего дня, если файла нет, создаём, если есть - дополняем
                                        with open('subscription_unsubscribe/subscription_unsubscribe_1.txt',
                                                  'a') as all_subscriptions_list_1_file:
                                            all_subscriptions_list_1_file.write(user + '\n')

                                        time.sleep(random.randrange(80, 110))

                                    else:
                                        time.sleep(random.randrange(2, 4))
                                        continue

                                    time.sleep(5)
                                except Exception as ex:
                                    print(ex)

                    except Exception as ex:
                        print(ex)
                        self.close_browser()

            except Exception as ex:
                print(ex)
                self.close_browser()

        self.close_browser()

    def follow_lekers(self, userpage, count = 100):
        """
        Подписка на пользователей, которые лайкают посты userpage

        :param userpage: url аккаунта, который используем как источник пользователей для подписок
        :param count: Количество подписок
        :return: None
        """

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        username = userpage.split("/")[-2]

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f"Пользователя {username} не существует, проверьте URL")
            self.close_browser()
        else:

            print(f"Пользователь {username} успешно найден, подписываемся и ставим лайки")
            time.sleep(2)

            # создаём папку для всех фалов связанных с пописками
            if os.path.exists("subscription_unsubscribe"):
                print("Папка subscription_unsubscribe уже существует!")
            else:
                print("Создаём папку пользователя subscription_unsubscribe.")
                os.mkdir('subscription_unsubscribe')

            posts_urls = []

            hrefs = browser.find_elements_by_tag_name('a')
            hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

            for href in hrefs:
                posts_urls.append(href)

            for post_url in posts_urls:
                likers_button = ''
                likers_count = ''
                try:
                    browser.get(post_url)
                    time.sleep(2)
                    if self.xpath_exists(
                            '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button/span'):
                        likers_button = browser.find_element_by_xpath(
                            "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button/span")
                        likers_count = likers_button.text
                    else:
                        continue

                except Exception as ex:
                    print(ex)
                    self.close_browser()

                # если количество лайкеров больше 999, убираем пробелы
                if ' ' in likers_count:
                    likers_count = int(''.join(likers_count.split(' ')))
                else:
                    likers_count = int(likers_count)

                loops_count = int(likers_count / 12)
                print(f"Число итераций: {loops_count}")
                time.sleep(4)

                likers_button.click()
                time.sleep(4)

                likers_ul = None
                if self.xpath_exists('/html/body/div[5]/div/div/div[2]/div'):
                    likers_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div")
                elif self.xpath_exists('/html/body/div[4]/div/div/div[2]/div'):
                    likers_ul = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div")

                try:
                    all_urls_div = likers_ul.find_elements_by_tag_name("a")
                    # all_urls_div = likers_ul.find_elements_by_class_name('                     Igw0E   rBNOH        eGOV_     ybXk5    _4EzTm                                                                                   XfCBB          HVWg4                 ')
                    count_of_likers = 0
                    likers_uls = []
                    likers_uls_new = []
                    for i in range(1, loops_count + 1):

                        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", likers_ul)
                        time.sleep(random.randrange(2, 4))
                        all_urls_div = likers_ul.find_elements_by_tag_name("a")
                        # all_urls_div = likers_ul.find_elements_by_class_name('                     Igw0E   rBNOH        eGOV_     ybXk5    _4EzTm                                                                                   XfCBB          HVWg4                 ')

                        for url in all_urls_div:
                            url = url.get_attribute("href")
                            likers_uls.append(url)

                        # убираем повторяющиеся
                        for url_new in likers_uls:
                            if url_new not in likers_uls_new:
                                likers_uls_new.append(url_new)

                        print(f"Итерация #{i}")
                        count_of_likers += 12
                        time.sleep(random.randrange(2, 4))

                        if count_of_likers >= count * 7:
                            break


                    for user in likers_uls_new:
                        if count > 0:
                            break
                        try:
                            try:
                                with open('subscription_unsubscribe/all_subscriptions_list.txt',
                                          'r') as all_subscriptions_list_file:
                                    lines = all_subscriptions_list_file.readlines()
                                    if user in lines:
                                        print(
                                            f'Мы уже подписаны или были подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                print('Файл со ссылками ещё не создан!')
                                print(ex)

                            browser = self.browser
                            browser.get(user)
                            time.sleep(2)
                            page_owner = user.split("/")[-2]

                            if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/a"):
                                print("Это наш профиль, уже подписан, пропускаем итерацию!")
                            elif self.xpath_exists(
                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button"):
                                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                            else:

                                if self.xpath_exists(
                                        "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    print('Закрытый аккаунт! Пропускаем')
                                    continue
                                else:
                                    try:
                                        if self.follow_or_not():

                                            if self.xpath_exists(
                                                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button'):
                                                follow_button = browser.find_element_by_xpath(
                                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button").click()
                                            elif self.xpath_exists(
                                                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button'):
                                                follow_button = browser.find_element_by_xpath(
                                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button").click()
                                            time.sleep(random.randrange(2, 4))
                                            self.put_likes(1)

                                            print(
                                                f'Подписались на пользователя {page_owner} и лайкнули 1 его пост. Открытый аккаунт!')
                                            count -= 1

                                            # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                                            with open('subscription_unsubscribe/all_subscriptions_list.txt',
                                                      'a') as all_subscriptions_list_file:
                                                all_subscriptions_list_file.write(user + '\n')

                                            # записываем данные в файл для ссылок сегодняшнего дня, если файла нет, создаём, если есть - дополняем
                                            with open('subscription_unsubscribe/subscription_unsubscribe_1.txt',
                                                      'a') as all_subscriptions_list_1_file:
                                                all_subscriptions_list_1_file.write(user + '\n')

                                            time.sleep(random.randrange(80, 110))
                                        else:
                                            time.sleep(random.randrange(2, 4))
                                            continue

                                    except Exception as ex:
                                        print(ex)

                        except Exception as ex:
                            print(ex)
                            self.close_browser()

                except Exception as ex:
                    print(ex)
                    self.close_browser()

        self.close_browser()

    def follow_commentators(self, userpage, count = 100):
        """
        Подписка на пользователей, которые комментируют посты userpage

        :param userpage: url аккаунта, который используем как источник пользователей для подписок
        :param count: Количество подписок
        :return: None
        """
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        username = userpage.split("/")[-2]

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f"Пользователя {username} не существует, проверьте URL")
            self.close_browser()
        else:
            print(f"Пользователь {username} успешно найден, подписываемся и ставим лйки")
            time.sleep(2)

            # создаём папку для всех фалов связанных с пописками
            if os.path.exists("subscription_unsubscribe"):
                print("Папка subscription_unsubscribe уже существует!")
            else:
                print("Создаём папку пользователя subscription_unsubscribe.")
                os.mkdir('subscription_unsubscribe')

            posts_urls = []

            hrefs = browser.find_elements_by_tag_name('a')
            hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

            for href in hrefs:
                posts_urls.append(href)

            for post_url in posts_urls:
                if count > 0:
                    break
                browser.get(post_url)
                comments_ul = browser.find_element_by_xpath(
                    "/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul")

                try:
                    try:
                        i = 1
                        counter_comments = 0
                        while True:
                            time.sleep(random.randrange(2, 4))
                            print(f"Итерация #{i}")

                            if not (self.xpath_exists(
                                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/li/div/button')) or counter_comments > 700:
                                break
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/li/div/button').click()
                            i += 1
                            counter_comments += 12

                    except Exception as ex:
                        print(ex)

                    all_urls = comments_ul.find_elements_by_class_name("Mr508")
                    print(f'Колличество комментаторов поста {post_url}: {len(all_urls)}')

                    comments_uls = []
                    for url in all_urls:
                        url = url.find_element_by_tag_name("a").get_attribute("href")
                        comments_uls.append(url)

                    for user in comments_uls:
                        try:
                            try:
                                with open('subscription_unsubscribe/all_subscriptions_list.txt',
                                          'r') as all_subscriptions_list_file:
                                    lines = all_subscriptions_list_file.readlines()
                                    if user in lines:
                                        print(
                                            f'Мы уже подписаны или были подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                print('Файл со ссылками ещё не создан!')
                                print(ex)

                            browser = self.browser
                            browser.get(user)
                            page_owner = user.split("/")[-2]

                            if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/a"):
                                print("Это наш профиль, уже подписан, пропускаем итерацию!")
                            elif self.xpath_exists(
                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button"):
                                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                            else:

                                if self.xpath_exists(
                                        "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    print('Закрытый аккаунт! Пропускаем')
                                    continue
                                else:
                                    try:
                                        if self.follow_or_not():

                                            if self.xpath_exists(
                                                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button'):
                                                follow_button = browser.find_element_by_xpath(
                                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button").click()
                                            elif self.xpath_exists(
                                                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button'):
                                                follow_button = browser.find_element_by_xpath(
                                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button").click()
                                            time.sleep(random.randrange(2, 4))
                                            self.put_likes(1)
                                            print(
                                                f'Подписались на пользователя {page_owner} и лайкнули 1 его пост. Открытый аккаунт!')

                                            count -= 1

                                            # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                                            with open('subscription_unsubscribe/all_subscriptions_list.txt',
                                                      'a') as all_subscriptions_list_file:
                                                all_subscriptions_list_file.write(user + '\n')

                                            # записываем данные в файл для ссылок сегодняшнего дня, если файла нет, создаём, если есть - дополняем
                                            with open('subscription_unsubscribe/subscription_unsubscribe_1.txt',
                                                      'a') as all_subscriptions_list_1_file:
                                                all_subscriptions_list_1_file.write(user + '\n')

                                            time.sleep(random.randrange(80, 110))
                                        else:
                                            time.sleep(random.randrange(2, 4))
                                            continue

                                        time.sleep(5)
                                    except Exception as ex:
                                        print(ex)

                        except Exception as ex:
                            print(ex)
                            self.close_browser()

                except Exception as ex:
                    print(ex)
                    self.close_browser()

        self.close_browser()

    def unsubscribe_file_users(self, path):
        """
        Отписка от всех пользователей переданного файла с url

        :param path: Путь к файлу
        :return: None
        """

        browser = self.browser
        with open(path, 'r') as file:
            for user_url in file.readlines():
                browser.get(user_url)
                time.sleep(random.randrange(3, 6))

                unfollow_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button').click()
                time.sleep(random.randrange(2, 4))
                unfollow_button = browser.find_element_by_xpath(
                    '/html/body/div[5]/div/div/div/div[3]/button[1]').click()
                print(f'Отписались от {user_url}')

                time.sleep(random.randrange(80, 110))

class Other():

    def time_in_Moscov(self):
        """
        Время GMT+3 в минутах

        :return: GMT+3 в минутах
        """
        t = (time.ctime()).split(' ')[3]
        hour = t.split(':')[0]
        minute = t.split(':')[1]
        return int(hour) * 60 + int(minute)
