
import telepot as tp
import requests as rq
from telepot.loop import MessageLoop
import time
import logging
import sys

from config import suprnova_api, telegram_api, suprnova_url, suprnova_id,coinmkcap_url

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='%(asctime)s: %(levelname)s: %(message)s')
handler  = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
log.addHandler(handler)

class Telebot:
    def __init__(self,bot):
        self.s_api = suprnova_api
        self.s_id = suprnova_id
        self.t_api = telegram_api
        self.s_url = suprnova_url
        self.c_url = coinmkcap_url
        self.bot = bot

    def tel_handler(self,msg):
        content_type, chat_type, chat_id = tp.glance(msg)
        log.info("Message received: {0}".format(msg['text']))
        if content_type == 'text':
            if msg['text'] == '/balance':
                final_price = self.q_supr('zencash')
                self.bot.sendMessage(chat_id,"Hi there. Current balance: ${}".format(final_price))
                log.info("sent message to telegrambot...")


    def q_supr(self,coin):
        params = {
            'page': 'api',
            'action' : 'getuserbalance',
            'api_key' : self.s_api,
            'id' : self.s_id
        }


        try:
            req = rq.get(self.s_url,params=params)
            if  req.status_code == 200:
                req = req.json()
                price = req['getuserbalance']['data']['confirmed']
                final_price = self.calc_price(price,coin)
                return final_price
        except Exception as ex:
            log.error('exception ocurred: {}'.format(ex))


    def calc_price(self,price,coin):
        params = {
            'fsym' : 'ZEN',
            'tsyms' : 'USD'

        }
        try:
            req = rq.get(self.c_url,params=params)
            if  req.status_code == 200:
                req = req.json()
                final_price = req['USD']
                final_price = float(price) * float(final_price)
                return round(final_price,3)
        except Exception as ex:
            log.error('exception ocurred: {}'.format(ex))


telebot = tp.Bot(telegram_api)
bot = Telebot(telebot)

MessageLoop(telebot,bot.tel_handler).run_as_thread()
log.info("telebot listening...")
while 1:
    time.sleep(10)




