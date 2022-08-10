import telebot
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

    def checker(company, master, slave, your_pn, inv_qry, columns, warehouses, pn_category):
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
            extra_found = find_machine.extra_finder(slave=slave, master=master, your_pn=your_pn,
                                                    pn_category=pn_category)
            print(extra_found)
            if extra_found:
                result = find_machine.trax_inventory_explorer(inv_qry=inv_qry, columns=columns,
                                                              found=extra_found, warehouses=warehouses)
                print(result)
                if not result.empty:
                    result = result.to_string(index=False, header=False, justify='left')
                    bot.send_message(m.chat.id, 'Я нашёл в ' + company + ':')
                    bot.send_message(m.chat.id, str(result))
                    a = 1
        return a

    vdt = checker(company='VDTM', master=dataset_vdtm.pns_vdtm,
                  slave=dataset_vdtm.pns_vdtm_int, your_pn=requested_pn,
                  inv_qry=dataset_vdtm.inv_qry_vdtm, columns=dataset_vdtm.columns_vdtm,
                  warehouses=dataset_vdtm.wh_list_vdtm,
                  pn_category=dataset_vdtm.pn_vdtm_category)
    airlines = checker(company='ABC и ATRAN', master=dataset_vd_airlines.pns_airlines,
                       slave=dataset_vd_airlines.pns_airlines_int, your_pn=requested_pn,
                       inv_qry=dataset_vd_airlines.inv_qry_airlines, columns=dataset_vd_airlines.columns_airlines,
                       warehouses=dataset_vd_airlines.wh_list_airlines,
                       pn_category=dataset_vd_airlines.pn_airlines_category)
    if vdt == 0 and airlines == 0:
        bot.send_message(m.chat.id, rdm.choice(lists_replies.nb_list))
    else:
        bot.send_message(m.chat.id, rdm.choice(lists_replies.r_list))


# Запускаем бота
bot.polling(none_stop=True, interval=0)
