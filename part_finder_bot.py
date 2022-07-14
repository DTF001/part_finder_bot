import telebot
import random as rdm

from find_machine import finder
from find_machine import extra_finder
from find_machine import extractor
from find_machine import trax_inventory_explorer

from dataset_vdtm import inv_qry_vdtm
from dataset_vdtm import pns_vdtm
from dataset_vdtm import pns_vdtm_int
from dataset_vdtm import pn_vdtm_category
from dataset_vdtm import columns_vdtm
from dataset_vdtm import wh_list_vdtm

from dataset_vd_airlines import inv_qry_airlines
from dataset_vd_airlines import pns_airlines
from dataset_vd_airlines import pns_airlines_int
from dataset_vd_airlines import pn_airlines_category
from dataset_vd_airlines import columns_airlines
from dataset_vd_airlines import wh_list_airlines

from lists_replies import r_list
from lists_replies import ok_list
from lists_replies import nb_list

# BOT_KEY

bot = telebot.TeleBot('5375777787:AAHjFAjfGquE-BtZ7kCvemee-5dbKu9dPYw')


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, 'Это бот для проверки складских остатков.')
    bot.send_message(m.chat.id, 'Бот в стадии разработки, v0,1a')


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(m):
    requested_pn = str(m.text)
    bot.send_message(m.chat.id, 'Запрошенный p/n: ' + requested_pn)
    bot.send_message(m.chat.id, rdm.choice(ok_list))

    def checker(company, master, slave, your_pn, inv_qry, columns, warehouses, mat_type, precision):
        a = 0
        found = finder(master=master, slave=slave, your_pn=your_pn)
        result = trax_inventory_explorer(inv_qry=inv_qry, columns=columns, warehouses=warehouses, found=found)
        if not result.empty:
            result = result.to_string(index=False, header=False, justify='left')
            bot.send_message(m.chat.id, 'Я нашёл в ' + company + ':')
            bot.send_message(m.chat.id, str(result))
            a = 1
        else:
            extra_found = extra_finder(slave=slave, mat_type=mat_type, precision=precision, your_pn=your_pn)
            if extra_found:
                extra_found_extracted = extractor(extra_found)
                extra_found_extracted = finder(master=master, slave=slave, your_pn=extra_found_extracted)
                result = trax_inventory_explorer(inv_qry=inv_qry, columns=columns, found=extra_found_extracted,
                                                 warehouses=warehouses)
                if not result.empty:
                    result = result.to_string(index=False, header=False, justify='left')
                    bot.send_message(m.chat.id, 'Я нашёл в ' + company + ':')
                    bot.send_message(m.chat.id, str(result))
                    a = 1
        return a

    vdt = checker(company='ВДТМ', master=pns_vdtm, slave=pns_vdtm_int, your_pn=requested_pn, inv_qry=inv_qry_vdtm,
                  columns=columns_vdtm, warehouses=wh_list_vdtm, mat_type=pn_vdtm_category, precision=75)
    airlines = checker(company='ABC и ATRAN', master=pns_airlines, slave=pns_airlines_int, your_pn=requested_pn,
                       inv_qry=inv_qry_airlines, columns=columns_airlines, warehouses=wh_list_airlines,
                       mat_type=pn_airlines_category, precision=75)
    if vdt == 0 and airlines == 0:
        bot.send_message(m.chat.id, rdm.choice(nb_list))
    else:
        bot.send_message(m.chat.id, rdm.choice(r_list))


# Запускаем бота
bot.polling(none_stop=True, interval=0)
