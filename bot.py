import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start = types.KeyboardButton("Погнали")
    markup.add(btn_start)

    mess = f'Привет, <b>{message.from_user.first_name}</b>. Я твой наставник по шахматам в виде бота. Я буду давать тебе шахматные задачи, готов начать?'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def tasks(message):
    if message.text == "Погнали":

        markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_accept = types.KeyboardButton("Я все понял, давай к делу")
        markup_menu.add(btn_accept)

        mess = f'Отлично, рад слышать! Моя база данных задач обновляется каждый день, <b>ныняшняя версия: 0.1</b> ' \
               f'Задачи усложняются по ходу решения. Ты можешь пропустить задачу, вернуться к предыдущей или ' \
               f'вернуться в это меню и начать все заново. Чтобы ответить на задачу необходимо написать ответ в ' \
               f'формате "e2-e4" (пример) и просто отправить мне. Я скажу, если ты ответил правильно или допустил ' \
               f'ошибку. Приятного время препровождения! '
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup_menu)

    elif message.text == "Я все понял, давай к делу":

        keyboard_1 = types.InlineKeyboardMarkup()
        callback_button_1 = types.InlineKeyboardButton(text="Вернуться в меню", callback_data="mainmenu")
        keyboard_1.add(callback_button_1)

        task_1 = 'https://skr.sh/sFLDGEHa3XV?a'
        bot.send_photo(message.chat.id, task_1, 'Задача #1 | Напиши ответ в формате "e2-e4"', reply_markup=keyboard_1)
        bot.register_next_step_handler(message, answer_tasks)


def answer_tasks(message):
    if message.text == "a2-a1":

        next_one = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_next = types.KeyboardButton('Следующая')
        next_one.add(button_next)

        task_1_done = 'https://skr.sh/sFLdRFxiDgV'
        bot.send_photo(message.chat.id, task_1_done, 'Отлично! Ты правильно решил задачу, переходи к следующей!',
                       reply_markup=next_one)
        bot.register_next_step_handler(message, task2)

    elif message.text != "a2-a1":

        next_one = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_next = types.KeyboardButton('Следующая')
        next_one.add(button_next)

        task_1 = 'https://skr.sh/sFLDGEHa3XV?a'
        bot.send_photo(message.chat.id, task_1, 'Ты допустил ошибку, попробуй еще раз или пропусти задачу',
                       reply_markup=next_one)
        bot.register_next_step_handler(message, task2)


def task2(message):
    if message.text == 'Следующая':
        bot.send_message(message.chat.id, 'Следующая')


@bot.callback_query_handler(func=lambda call: True)
def menu(call):
    if call.data == "mainmenu":
        markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_accept = types.KeyboardButton("Я все понял, давай к делу")
        markup_menu.add(btn_accept)

        mess = f'<b>Ты вернулся в меню.</b> Моя база данных задач обновляется каждый день, <b>ныняшняя версия: 0.1</b> ' \
               f'Задачи усложняются по ходу решения. Ты можешь пропустить задачу, вернуться к предыдущей или ' \
               f'вернуться в это меню и начать все заново. Чтобы ответить на задачу необходимо написать ответ в ' \
               f'формате "e2-e4" (пример) и просто отправить мне. Я скажу, если ты ответил правильно или допустил ' \
               f'ошибку. Приятного время препровождения! '
        bot.send_message(call.message.chat.id, mess, parse_mode='html', reply_markup=markup_menu)


bot.polling(none_stop=True)
