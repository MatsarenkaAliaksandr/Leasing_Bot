import requests
import telebot
import json
from telebot import types
import random

bot = telebot.TeleBot('8000703233:AAFbsf9GCJR-YxaEcGp91o6pN6Yr6g6Obak')

keyboard = ['🧮 Рассчитать лизинг']
keyboard_one: list[str] = ['👨‍🦳 Юр. лицо', '🧔‍♂️ ИП', '👱‍♂️ Физ. лицо', '↪️ Вернуться в начало']
keyboard_two = ['🚗 Новая', '🚕 Б/у не старше 10 лет', '🛻 Б/у старше 10 лет', '⬅️ Назад', '↪️ Вернуться в начало']
keyboard_three = ['🚘 Легковой', '🚚 Грузовой', '🔌 Электромобили', '⬅️ Назад', '↪️ Вернуться в начало']
back = ['⬅️ Назад', '↪️ Вернуться в начало']
term = ["13 мес.", "18 мес.", "24 мес.", "36 мес.", "48 мес.", "60 мес.", "84 мес.", '⬅️ Назад', "↪️ Вернуться в начало"]
percent = ["20%", "30%", "40%", "50%", "60%", '⬅️ Назад', "↪️ Вернуться в начало"]
end = ['⬅️ Назад', "👨‍💼 Связь с менеджером", "↪️ Вернуться в начало"]


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
    if (message.text == "🧮 Рассчитать лизинг" or message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)

    elif (message.text == "👨‍🦳 Юр. лицо"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_two)
        msg = bot.send_message(message.chat.id, text="Вас интересует новая автотехника или б/у не старше 10 лет?", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity)

    elif (message.text in ["🧔‍♂️ ИП", "👱‍♂️ Физ. лицо"]):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_two)
        msg = bot.send_message(message.chat.id, text="Вас интересует новая автотехника или б/у не старше 10 лет?", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person)

    elif (message.text == "👨‍💼 Связь с менеджером"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*back)
        bot.send_message(message.chat.id,
                               text="Напишите нашему менеджеру, для получения более подробной информации <b>@davidov_max</b>",
                               reply_markup=markup, parse_mode='html')

    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*percent)
        msg = bot.send_message(message.chat.id, text="Выберите сумму Вашего авансового платежа (от полной ст-ти легкового автомобиля).", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_count)

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..введите /start")


def natural_person(message):
    if (message.text in ["🚗 Новая", "🚕 Б/у не старше 10 лет", "🛻 Б/у старше 10 лет"]):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_three)
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

def natural_person_car(message):
    if (message.text in ["🚘 Легковой", "🚚 Грузовой", "🔌 Электромобили"]):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*back)
        msg = bot.send_message(message.chat.id, text="Введите полную стоимость легкового автомобиля с НДС.", reply_markup=markup)
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

def natural_person_term(message):
    if (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)
    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_three)
        msg = bot.send_message(message.chat.id, text="Какое транспортное средство Вас интересует?", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_car)

    elif (message.text.isdigit()):
        global cost
        cost = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*term)
        msg = bot.send_message(message.chat.id, text="Выберите срок лизинга.", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_advance)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*back)
        msg = bot.send_message(message.chat.id, text="Введите <b>правильно</b> стоимость легкового автомобиля с НДС.",
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
        msg = bot.send_message(message.chat.id, text="Введите полную стоимость легкового автомобиля с НДС.", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_term)

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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*term)
        msg = bot.send_message(message.chat.id, text="Выберите срок лизинга.", reply_markup=markup)
        bot.register_next_step_handler(msg, natural_person_advance)

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
            bot.send_message(message.chat.id,
                         text=f"<b>Ваша структура по лизингу:</b>\n\n"
                              f"Стоимость: <b>{cost} BYN</b>\n"
                              f"Аванс:  <b>{pers}%  ({advan} BYN)</b>\n\n"
                              f"Срок лизинга:  <b>{advance[0:2]} месяцев</b>\n"
                              f"Средний ежемесячный платеж:  <b>{pay} BYN</b>\n\n"
                              f"Если у вас появились вопросы, пожалуйста, обратитесь к специалисту по телефону +375 29 686 68 95 (ПН-ЧТ 9:30-17:30; ПТ 9:30-16:15).",
                              reply_markup=markup, parse_mode='html')
        else:
            pay_one = (int(cost) - (int(cost)/100)*(int(percent_advance[0:2])))/int(advance[0:2])
            pay_two = ((int(cost) - (int(cost)/100)*(int(percent_advance[0:2])))/100*17.5)/12
            pay = round(pay_one+pay_two)
            bot.send_message(message.chat.id,
                                   text=f"<b>Ваша структура по лизингу:</b>\n\n"
                                        f"Стоимость: <b>{cost} BYN</b>\n"
                                        f"Аванс:  <b>{pers}%  ({advan} BYN)</b>\n\n"
                                        f"Срок лизинга:  <b>{advance[0:2]} месяцев</b>\n"
                                        f"Средний ежемесячный платеж:  <b>{pay} BYN</b>\n\n"
                                        f"Если у вас появились вопросы, пожалуйста, обратитесь к специалисту по телефону +375 29 686 68 95 (ПН-ЧТ 9:30-17:30; ПТ 9:30-16:15).",
                                        reply_markup=markup, parse_mode='html')


def legal_entity(message):
    if (message.text in ["🚗 Новая", "🚕 Б/у не старше 10 лет", "🛻 Б/у старше 10 лет"]):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_three)
        msg = bot.send_message(message.chat.id, text="Какое транспортное средство Вас интересует?", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_car)

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
def legal_entity_car(message):
    if (message.text in ["🚘 Легковой", "🚚 Грузовой", "🔌 Электромобили"]):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*back)
        msg = bot.send_message(message.chat.id, text="Введите полную стоимость легкового автомобиля с НДС.", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_term)

    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_two)
        msg = bot.send_message(message.chat.id, text="Вас интересует новая автотехника или б/у не старше 10 лет?", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity)

    elif (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)
def legal_entity_term(message):
    if (message.text == "↪️ Вернуться в начало"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_one)
        bot.send_message(message.chat.id, text="На кого вы хотите оформить лизинг авто?".format(message.from_user),
                         reply_markup=markup)

    elif (message.text == "⬅️ Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*keyboard_three)
        msg = bot.send_message(message.chat.id, text="Какое транспортное средство Вас интересует?", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_car)

    elif (message.text.isdigit()):
        global cost
        cost = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*term)
        msg = bot.send_message(message.chat.id, text="Выберите срок лизинга.", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_advance)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*back)
        msg = bot.send_message(message.chat.id, text="Введите <b>правильно</b> стоимость легкового автомобиля с НДС.",
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
        msg = bot.send_message(message.chat.id, text="Введите полную стоимость легкового автомобиля с НДС.", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_term)

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
        markup.add(*term)
        msg = bot.send_message(message.chat.id, text="Выберите срок лизинга.", reply_markup=markup)
        bot.register_next_step_handler(msg, legal_entity_advance)

    else:
        global percent_advance
        percent_advance = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
        markup.add(*end)
        pers = percent_advance[0:2]
        advan = (int(cost)/100)*(int(percent_advance[0:2]))
        pay_one = (int(cost) - (int(cost)/100)*(int(percent_advance[0:2])))/int(advance[0:2])
        pay_two = ((int(cost) - (int(cost)/100)*(int(percent_advance[0:2])))/100*15.5)/12
        pay = round(pay_one+pay_two)
        bot.send_message(message.chat.id,
                               text=f"<b>Ваша структура по лизингу:</b>\n\n"
                                    f"Стоимость: <b>{cost} BYN</b>\n"
                                    f"Аванс:  <b>{pers}%  ({advan} BYN)</b>\n\n"
                                    f"Срок лизинга:  <b>{advance[0:2]} месяцев</b>\n"
                                    f"Средний ежемесячный платеж:  <b>{pay} BYN</b>\n\n"
                                    f"Если у вас появились вопросы, пожалуйста, обратитесь к специалисту по телефону +375 29 686 68 95 (ПН-ЧТ 9:30-17:30; ПТ 9:30-16:15).",
                               reply_markup=markup, parse_mode='html')


bot.polling(non_stop=True, interval=0)
