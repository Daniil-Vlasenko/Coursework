import time
from InstagramBotPromotionLibrary import Other
from InstagramBotPromotionLibrary import BrowserSurfingPromotion

class Bot():

    def bot_promotion(self, accounts_for_promotion, username, password, webdriver_path, path_files):
        """
        Раскрутка бота в инстаграмм

        :param accounts_for_following: Массив url на аккаунты, которые будет использоваться для раскрутки
        :param username: Ник аккаунта бота
        :param password: Пароль аккаунта бота
        :param webdriver_path: Путь к webdriver
        :param path_files: Путь к txt фалйам, где храниться информация о подписках
        :return: None
        """
        count = 0
        while True:
            my_bot = BrowserSurfingPromotion(username, password, webdriver_path)
            my_bot.login()
            t = Other()

            # процесс подписок на и лайканья подписчиков, лайкеров и комментаторов переданного аккаунта
            if t.time_in_Moscov() > 0 and t.time_in_Moscov() < 420:
                print('Начался процесс подписки на подписчиков')
                try:
                    my_bot.follow_followers(accounts_for_promotion[count], count = 200)
                except Exception as ex:
                    print(ex)
                print('Закончился процесс подписки на подписчиков')
                time_now = t.time_in_Moscov()
                time.sleep(600 - time_now)

            if t.time_in_Moscov() > 480 and t.time_in_Moscov() < 600:
                print('Начался процесс подписки на лайкеров')
                try:
                    my_bot.follow_lekers(accounts_for_promotion[count], count = 100)
                except Exception as ex:
                    print(ex)
                print('Закончился процесс подписки на лайкеров')
                time_now = t.time_in_Moscov()
                time.sleep(660 - time_now)

            if t.time_in_Moscov() > 660 and t.time_in_Moscov() < 840:
                print('Начался процесс подписки на комментаторов')
                try:
                    my_bot.follow_lekers(accounts_for_promotion[count], count = 100)
                except Exception as ex:
                    print(ex)
                print('Закончился процесс подписки на комментаторов')
                time_now = t.time_in_Moscov()

            # процесс отписки от юзеров из subscription_unsubscribe_3
            if t.time_in_Moscov() > 840 and t.time_in_Moscov() < 1400:
                print('Начинаем процесс отписки')
                my_bot.unsubscribe_file_users(path_files + '\subscription_unsubscribe_3.txt')
                print('Закончили процесс отписки')

            # subscription_unsubscribe_1 -> subscription_unsubscribe_2 -> subscription_unsubscribe_3
            with open(path_files + '\subscription_unsubscribe_2.txt',
                      'r') as subscription_unsubscribe_2_file, open(
                path_files + "\subscription_unsubscribe_3.txt",
                'w') as subscription_unsubscribe_3_file:
                for line in subscription_unsubscribe_2_file:
                    subscription_unsubscribe_3_file.write(line)

            with open(path_files + '\subscription_unsubscribe_1.txt',
                      'r') as subscription_unsubscribe_1_file, open(
                path_files + "\subscription_unsubscribe_2.txt",
                'w') as subscription_unsubscribe_2_file:
                for line in subscription_unsubscribe_1_file:
                    subscription_unsubscribe_2_file.write(line)

            with open(path_files + '\subscription_unsubscribe_1.txt',
                      'w') as subscription_unsubscribe_1_file:
                subscription_unsubscribe_1_file.write('')

            my_bot.close_browser()

            # перебор аккаунтов
            if count < len(accounts_for_promotion):
                count += 1
            else:
                count = 0

            # ждет до 0 a.m. следующего дня
            time_now = t.time_in_Moscov()
            time.sleep(1440 - time_now + 10)



