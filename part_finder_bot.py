import telebot
from decouple import config
import random as rdm
import find_machine
import dataset_vdtm
import dataset_vd_airlines
import lists_replies

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
    bot.send_message(m.chat.id, rdm.choice(lists_replies.ok_list))

    def checker(company, master, slave, your_pn, inv_qry, columns, warehouses, mat_type, precision):
        a = 0
        found = find_machine.finder(master=master, slave=slave, your_pn=your_pn)
        result = find_machine.trax_inventory_explorer(inv_qry=inv_qry, columns=columns, warehouses=warehouses,
                                                      found=found)
        if not result.empty:
            result = result.to_string(index=False, header=False, justify='left')
            bot.send_message(m.chat.id, 'Я нашёл в ' + company + ':')
            bot.send_message(m.chat.id, str(result))
            a = 1
        else:
            extra_found = find_machine.extra_finder(slave=slave, mat_type=mat_type, precision=precision,
                                                    your_pn=your_pn)
            if extra_found:
                extra_found_extracted = find_machine.extractor(extra_found)
                extra_found_extracted = find_machine.finder(master=master, slave=slave, your_pn=extra_found_extracted)
                result = find_machine.trax_inventory_explorer(inv_qry=inv_qry, columns=columns,
                                                              found=extra_found_extracted, warehouses=warehouses)
                if not result.empty:
                    result = result.to_string(index=False, header=False, justify='left')
                    bot.send_message(m.chat.id, 'Я нашёл в ' + company + ':')
                    bot.send_message(m.chat.id, str(result))
                    a = 1
        return a

    vdt = checker(company='ВДТМ', master=dataset_vdtm.pns_vdtm, slave=dataset_vdtm.pns_vdtm_int, your_pn=requested_pn,
                  inv_qry=dataset_vdtm.inv_qry_vdtm,
                  columns=dataset_vdtm.columns_vdtm, warehouses=dataset_vdtm.wh_list_vdtm,
                  mat_type=dataset_vdtm.pn_vdtm_category, precision=85)
    airlines = checker(company='ABC и ATRAN', master=dataset_vd_airlines.pns_airlines,
                       slave=dataset_vd_airlines.pns_airlines_int, your_pn=requested_pn,
                       inv_qry=dataset_vd_airlines.inv_qry_airlines, columns=dataset_vd_airlines.columns_airlines,
                       warehouses=dataset_vd_airlines.wh_list_airlines,
                       mat_type=dataset_vd_airlines.pn_airlines_category, precision=85)
    if vdt == 0 and airlines == 0:
        bot.send_message(m.chat.id, rdm.choice(lists_replies.nb_list))
    else:
        bot.send_message(m.chat.id, rdm.choice(lists_replies.r_list))


# Запускаем бота
bot.polling(none_stop=True, interval=0)
