import telebot
from telebot import types

bot = telebot.TeleBot('8000703233:AAFbsf9GCJR-YxaEcGp91o6pN6Yr6g6Obak')

keyboard = ['🧮 Рассчитать лизинг']
keyboard_one: list[str] = ['👨‍🦳 Юр. лицо', '🧔‍♂️ ИП', '👱‍♂️ Физ. лицо', '↪️ Вернуться в начало']
keyboard_two = ['🚗 Новая', '🚕 Б/у не старше 10 лет', '🛻 Б/у старше 10 лет', '⬅️ Назад', '↪️ Вернуться в начало']
keyboard_three_leg = ['🚘 Легковой', '🚚 Грузовой', '🔌 Электромобили', '🏗 Спецтехника', '🗜 Оборудование', '🏡 Недвижимость', '⬅️ Назад', '↪️ Вернуться в начало']
keyboard_three_nat = ['🚘 Легковой', '🔌 Электромобили', '⬅️ Назад', '↪️ Вернуться в начало']
back = ['⬅️ Назад', '↪️ Вернуться в начало']
term_nat = ["12 мес.", "18 мес.", "24 мес.", "36 мес.", "48 мес.", "60 мес.", "84 мес.", '⬅️ Назад', "↪️ Вернуться в начало"]
term_leg_ip = ["12 мес.", "18 мес.", "24 мес.", "36 мес.", "48 мес.", "60 мес.", '⬅️ Назад', "↪️ Вернуться в начало"]
percent = ["20%", "25%", "30%", "40%", "50%", "60%", '⬅️ Назад', "↪️ Вернуться в начало"]
end = ['⬅️ Назад', "👨‍💼 Связь с менеджером", "↪️ Вернуться в начало"]
currency_button = ['BYN', 'USD', '⬅️ Назад', '↪️ Вернуться в начало']


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
    markup.add(*keyboard)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}!\n"
                          "Меня зовут Лиза и я помогу Вам рассчитать график платежей по лизингу 📊\n"
                          "После формирования графика у Вас будет возможность заказать дополнительную консультацию со специалистом 📲.\n"
                          "Для этого ответьте, пожалуйста, на несколько вопросов.".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     text="Нажмите /start появится меню.\n"
                          " Пожалуйста, выберите необходимое действие на кнопках клавиатуры ниже.\n"
                          " Если кнопки не отображаются, нажмите специальную иконку возле поля ввода сообщения.")


@bot.message_handler(content_types=['text'])
def func(message):
    global person
    if (message.text == "🧮 Рассчитать лизинг" or message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)

    elif (message.text == "👨‍🦳 Юр. лицо"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_three_leg)
        person = message.text
        msg = bot.send_message(message.chat.id, text="Выберите подходящий предмет лизинга?", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity)

    elif (message.text == "🧔‍♂️ ИП"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_two)
        person = message.text
        msg = bot.send_message(message.chat.id, text="Вас интересует новая автотехника или б/у не старше 10 лет?", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person)

    elif (message.text == "👱‍♂️ Физ. лицо"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_two)
        person = message.text
        msg = bot.send_message(message.chat.id, text="Вас интересует новая автотехника или б/у не старше 10 лет?", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person)

    elif (message.text == "👨‍💼 Связь с менеджером"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*back)
        bot.send_message(message.chat.id,
                               text="Напишите нашему менеджеру, для получения более подробной информации <b>@davidov_max</b>",
                               reply_markup=markup, parse_mode='html')

    elif (message.text == "⬅️ Назад" and person == "👨‍🦳 Юр. лицо"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*percent)
        msg = bot.send_message(message.chat.id, text="Выберите сумму Вашего авансового платежа (от полной ст-ти легкового автомобиля).", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_count)

    elif (message.text == "⬅️ Назад" and person == "🧔‍♂️ ИП"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*percent)
        msg = bot.send_message(message.chat.id, text="Выберите сумму Вашего авансового платежа (от полной ст-ти легкового автомобиля).", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_count)

    elif (message.text == "⬅️ Назад" and person == "👱‍♂️ Физ. лицо"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*percent)
        msg = bot.send_message(message.chat.id, text="Выберите сумму Вашего авансового платежа (от полной ст-ти легкового автомобиля).", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_count)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="Извините, Ваше сообщение не является допустимым. Для продолжения воспользуйтесь кнопками".format(message.from_user),
                         reply_markup=markup)


def natural_person(message):
    if (message.text in ["🚗 Новая", "🚕 Б/у не старше 10 лет", "🛻 Б/у старше 10 лет"]):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_three_nat)
        msg = bot.send_message(message.chat.id, text="Какое транспортное средство Вас интересует?", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_car)

    elif (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)

    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        msg = bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?", reply_markup=markup)
        bot.register_next_step_handler(msg, func)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_two)
        msg = bot.send_message(message.chat.id, text="Извините, Ваше сообщение не является допустимым. Для продолжения воспользуйтесь кнопками!",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person)

def natural_person_car(message):
    if (message.text in ["🚘 Легковой", "🔌 Электромобили"]):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*back)
        msg = bot.send_message(message.chat.id, text="Введите полную стоимость легкового автомобиля в BYN.", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_term)

    elif (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)
    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_two)
        msg = bot.send_message(message.chat.id, text="Вас интересует новая автотехника или б/у не старше 10 лет?", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_three_nat)
        msg = bot.send_message(message.chat.id,
                               text="Извините, Ваше сообщение не является допустимым. Для продолжения воспользуйтесь кнопками!",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_car)

def natural_person_term(message):
    if (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)
    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_three_nat)
        msg = bot.send_message(message.chat.id, text="Какое транспортное средство Вас интересует?", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_car)

    elif (message.text.isdigit()):
        if person == "🧔‍♂️ ИП":
            global cost
            cost = message.text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
            markup.add(*term_leg_ip)
            msg = bot.send_message(message.chat.id, text="Выберите срок лизинга.", reply_markup=markup)
            bot.register_next_step_handler(msg, natural_person_advance)

        else:
            cost = message.text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
            markup.add(*term_nat)
            msg = bot.send_message(message.chat.id, text="Выберите срок лизинга.", reply_markup=markup)
            bot.register_next_step_handler(msg, natural_person_advance)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*back)
        msg = bot.send_message(message.chat.id, text="Введите <b>правильно</b> стоимость легкового автомобиля  в BYN.",
                               reply_markup=markup, parse_mode='html')
        bot.register_next_step_handler(msg, natural_person_term)

def natural_person_advance(message):
    if (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)
    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*back)
        msg = bot.send_message(message.chat.id, text="Введите полную стоимость легкового автомобиля в BYN.", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_term)

    elif (message.text not in term_nat ):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*term_nat)
        msg = bot.send_message(message.chat.id, text="Выберите срок лизинга из предложенных в меню.", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_advance)

    else:
        global advance
        advance = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*percent)
        msg = bot.send_message(message.chat.id,
                               text="Выберите сумму Вашего авансового платежа (от полной ст-ти легкового автомобиля).",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_count)


def natural_person_count(message):
    if (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)

    elif (message.text == "⬅️ Назад"):
        if person == "🧔‍♂️ ИП":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
            markup.add(*term_leg_ip)
            msg = bot.send_message(message.chat.id, text="Выберите срок лизинга.", reply_markup=markup)
            bot.register_next_step_handler(msg, natural_person_advance)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
            markup.add(*term_nat)
            msg = bot.send_message(message.chat.id, text="Выберите срок лизинга.", reply_markup=markup)
            bot.register_next_step_handler(msg, natural_person_advance)

    elif(message.text not in percent):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*percent)
        msg = bot.send_message(message.chat.id,
                               text="Выберите сумму Вашего авансового платежа (от полной ст-ти легкового автомобиля) из предложенных в меню.",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_count)

    else:
        global percent_advance
        percent_advance = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*end)
        pers = percent_advance[0:2]
        advan = (int(cost)/100)*(int(percent_advance[0:2]))

        if (int(advance[0:2]) == 84):
            pay_one = (int(cost) - (int(cost) / 100) * (int(percent_advance[0:2]))) / int(advance[0:2])
            pay_two = ((int(cost) - (int(cost) / 100) * (int(percent_advance[0:2]))) / 100 * 20) / 12
            pay = round(pay_one + pay_two)
            pay = '{0:,}'.format(pay).replace(',', ' ')
            advan = '{0:,}'.format(advan).replace(',', ' ')
            cost_end = '{0:,}'.format(int(cost)).replace(',', ' ')
            bot.send_message(message.chat.id,
                         text=f"<b>Ваша структура по лизингу:</b>\n\n"
                              f"Стоимость: <b>{cost_end} BYN</b>\n"
                              f"Аванс:  <b>{pers}%  ({advan} BYN)</b>\n\n"
                              f"Срок лизинга:  <b>{advance[0:2]} месяцев</b>\n"
                              f"Средний ежемесячный платеж:  <b>{pay} BYN</b>\n\n"
                              f"Если у вас появились вопросы, пожалуйста, обратитесь к специалисту по телефону +375 29 686 68 95 (ПН-ЧТ 9:30-17:30; ПТ 9:30-16:15).",
                              reply_markup=markup, parse_mode='html')
        else:
            pay_one = (int(cost) - (int(cost)/100)*(int(percent_advance[0:2])))/int(advance[0:2])
            pay_two = ((int(cost) - (int(cost)/100)*(int(percent_advance[0:2])))/100*17.5)/12
            pay = round(pay_one+pay_two)
            pay = '{0:,}'.format(pay).replace(',', ' ')
            advan = '{0:,}'.format(advan).replace(',', ' ')
            cost_end = '{0:,}'.format(int(cost)).replace(',', ' ')
            bot.send_message(message.chat.id,
                                   text=f"<b>Ваша структура по лизингу:</b>\n\n"
                                        f"Стоимость: <b>{cost_end} BYN</b>\n"
                                        f"Аванс:  <b>{pers}%  ({advan} BYN)</b>\n\n"
                                        f"Срок лизинга:  <b>{advance[0:2]} месяцев</b>\n"
                                        f"Средний ежемесячный платеж:  <b>{pay} BYN</b>\n\n"
                                        f"Если у вас появились вопросы, пожалуйста, обратитесь к специалисту по телефону +375 29 686 68 95 (ПН-ЧТ 9:30-17:30; ПТ 9:30-16:15).",
                                        reply_markup=markup, parse_mode='html')




def legal_entity(message):
    if (message.text in ['🚘 Легковой', '🚚 Грузовой', '🔌 Электромобили', '🏗 Спецтехника', '🗜 Оборудование', '🏡 Недвижимость']):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*currency_button)
        msg = bot.send_message(message.chat.id, text="В какой валюте лизинг Вас интересует?", reply_markup=markup)
        bot.register_next_step_handler(msg, currency)

    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        msg = bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?", reply_markup=markup)
        bot.register_next_step_handler(msg, func)

    elif (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_three_leg)
        msg = bot.send_message(message.chat.id, text="Извините, Ваше сообщение не является допустимым. Для продолжения воспользуйтесь кнопками!",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity)

def currency(message):
    if (message.text in ['BYN', 'USD']):
        global currency_value
        currency_value = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*back)
        msg = bot.send_message(message.chat.id, text=f"Введите полную стоимость предмета лизинга с НДС в {currency_value}.", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_term)

    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_three_leg)
        msg = bot.send_message(message.chat.id, text="Выберите подходящий предмет лизинга?", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity)

    elif (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*currency_button)
        msg = bot.send_message(message.chat.id,
                               text="Извините, Ваше сообщение не является допустимым. Для продолжения воспользуйтесь кнопками!",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, currency)

def legal_entity_term(message):
    if (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)

    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*currency_button)
        msg = bot.send_message(message.chat.id, text="В какой валюте лизинг Вас интересует?", reply_markup=markup)
        bot.register_next_step_handler(msg, currency)

    elif (message.text.isdigit()):
        global cost
        cost = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*term_leg_ip)
        msg = bot.send_message(message.chat.id, text="Выберите срок лизинга.", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_advance)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*back)
        msg = bot.send_message(message.chat.id, text=f"Введите <b>правильно</b> стоимость предмета лизинга с НДС в {currency_value}.",
                               reply_markup=markup, parse_mode='html')
        bot.register_next_step_handler(msg, legal_entity_term)

def legal_entity_advance(message):
    if(message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)

    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*back)
        msg = bot.send_message(message.chat.id, text=f"Введите полную стоимость предмета лизинга с НДС в {currency_value}.", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_term)

    elif (message.text not in term_leg_ip ):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*term_leg_ip)
        msg = bot.send_message(message.chat.id, text="Выберите срок лизинга из предложенных в меню.", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_advance)

    else:
        global advance
        advance = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*percent)
        msg = bot.send_message(message.chat.id, text="Выберите сумму Вашего авансового платежа (от полной ст-ти легкового автомобиля).", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_count)

def legal_entity_count(message):
    if (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)

    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*term_leg_ip)
        msg = bot.send_message(message.chat.id, text="Выберите срок лизинга.", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_advance)

    elif (message.text not in percent):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*percent)
        msg = bot.send_message(message.chat.id,
                               text="Выберите сумму Вашего авансового платежа (от полной ст-ти легкового автомобиля) из предложенных в меню.",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_count)

    else:
        if currency_value == 'BYN':
            global percent_advance
            percent_advance = message.text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
            markup.add(*end)
            pers = percent_advance[0:2]
            advan = (int(cost)/100)*(int(percent_advance[0:2]))
            pay_one = (int(cost) - (int(cost)/100)*(int(percent_advance[0:2])))/int(advance[0:2])
            pay_two = ((int(cost) - (int(cost)/100)*(int(percent_advance[0:2])))/100*15.5)/12
            pay = round(pay_one+pay_two)
            pay = '{0:,}'.format(pay).replace(',', ' ')
            advan = '{0:,}'.format(advan).replace(',', ' ')
            cost_end = '{0:,}'.format(int(cost)).replace(',', ' ')
            bot.send_message(message.chat.id,
                                   text=f"<b>Ваша структура по лизингу:</b>\n\n"
                                        f"Стоимость: <b>{cost_end} {currency_value}</b>\n"
                                        f"Аванс:  <b>{pers}%  ({advan} {currency_value})</b>\n\n"
                                        f"Срок лизинга:  <b>{advance[0:2]} месяцев</b>\n"
                                        f"Средний ежемесячный платеж:  <b>{pay} {currency_value}</b>\n\n"
                                        f"Если у вас появились вопросы, пожалуйста, обратитесь к специалисту по телефону +375 29 686 68 95 (ПН-ЧТ 9:30-17:30; ПТ 9:30-16:15).",
                                   reply_markup=markup, parse_mode='html')

        else:
            percent_advance = message.text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
            markup.add(*end)
            pers = percent_advance[0:2]
            advan = (int(cost) / 100) * (int(percent_advance[0:2]))
            pay_one = (int(cost) - (int(cost) / 100) * (int(percent_advance[0:2]))) / int(advance[0:2])
            pay_two = ((int(cost) - (int(cost) / 100) * (int(percent_advance[0:2]))) / 100 * 8) / 12
            pay = round(pay_one + pay_two)
            pay = '{0:,}'.format(pay).replace(',', ' ')
            advan = '{0:,}'.format(advan).replace(',', ' ')
            cost_end = '{0:,}'.format(int(cost)).replace(',', ' ')
            bot.send_message(message.chat.id,
                             text=f"<b>Ваша структура по лизингу:</b>\n\n"
                                  f"Стоимость: <b>{cost_end} {currency_value}</b>\n"
                                  f"Аванс:  <b>{pers}%  ({advan} {currency_value})</b>\n\n"
                                  f"Срок лизинга:  <b>{advance[0:2]} месяцев</b>\n"
                                  f"Средний ежемесячный платеж:  <b>{pay} {currency_value}</b>\n\n"
                                  f"Если у вас появились вопросы, пожалуйста, обратитесь к специалисту по телефону +375 29 686 68 95 (ПН-ЧТ 9:30-17:30; ПТ 9:30-16:15).",
                             reply_markup=markup, parse_mode='html')


bot.polling(non_stop=True, interval=0)
