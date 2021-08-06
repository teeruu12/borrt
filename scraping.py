import requests
from bs4 import BeautifulSoup
import telebot
import time


def numsearch(s):
    flag = False
    for i in '0123456789':
        if i in s:
            flag = True
            break
    return flag


last_orders = []
categories = ['180', '22', '170', '169']

bot = telebot.TeleBot('1943250785:AAEJpzntuSPMQihouMJI3n1UojHdvmZe4j0')


@bot.message_handler(commands=["start"])
def start(message):
    while True:

        for categorie in categories:
            req = 'https://freelancehunt.com/projects?skills%5B%5D=' + categorie
            response = requests.get(req)
            soup = BeautifulSoup(response.text, 'lxml')
            trs = soup.find('table', class_='table table-normal project-list').find_all('tr')

            for i in range(0, 3):
                tr = trs[i]
                title = tr.find('a').text
                cost = tr.find('td').find('span').text
                link = tr.find('a').get('href')
                title = str(title)
                cost = str(cost)
                link = str(link)


                if cost == '':
                    cost = "не указана"
                else:
                    cost = cost[2:-2]
                    now = [title, cost, link]

                if not now[0] in last_orders:
                    last_orders.append(now[0])
                    if not numsearch(now[1]):
                        now[1] = 'не указана'
                    elif 'реми' in now[1]:
                        now[1] = 'премиум проект'

                    message_text = str('Название: ' + now[0] + '\n\nЦена: ' + now[1] + '\n\nПодробнее: ' + now[2])
                    bot.send_message(message.chat.id, message_text)
        time.sleep(60)
        if len(categories) > 30:
            categories.pop(len(categories) - 1)
            categories.pop(len(categories) - 1)
            categories.pop(len(categories) - 1)

@bot.message_handler(commands=["text"])
def stop(message):
    bot.send_message(message.chat.id, 'Все ок)')

if __name__ =='__main__':
    bot.polling(none_stop=True)
