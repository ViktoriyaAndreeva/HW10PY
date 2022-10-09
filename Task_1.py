# Калькулятор
from email import message
import telebot
from telebot import types
import logging

telebot.apihelper.ENABLE_MIDDLEWARE = True

bot = telebot.TeleBot('5527888167:AAFV2XoHi8ELi0sUb0eJbzatH3ZMZgiMscs')

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

del_buttons = telebot.types.ReplyKeyboardRemove()

buttons1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1.row(telebot.types.KeyboardButton('Комплексные'),
             telebot.types.KeyboardButton('Рациональные'))
buttons1.row(telebot.types.KeyboardButton('Ещё не определился'))

buttons2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons2.row(telebot.types.KeyboardButton('+'),
             telebot.types.KeyboardButton('-'))
buttons2.row(telebot.types.KeyboardButton('*'),
             telebot.types.KeyboardButton('/'))

buttons3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons3.row(telebot.types.KeyboardButton('результат'),
             telebot.types.KeyboardButton('считаем дальше'))


user_num1 = ""
user_num2 = ""
user_operation = ""
user_result = None


formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("logs.txt")

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger = logging.Logger("tgbot")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


@bot.middleware_handler(update_types=['message'])
def log_all_messages(bot_instance, message: telebot.types.Message):
    logger.info("Message %s from %s", message.text, message.from_user.username)


@bot.message_handler(commands=["start", "help"])
def send_first_message(message: telebot.types.Message):
    logger.info("New user %s", message.from_user.username)

    msg = bot.send_message(
        message.chat.id, "Привет! я бот-калькулятор\nВыберите режим работы", reply_markup=buttons1)
    bot.register_next_step_handler(msg, answer)


def answer(msg: telebot.types.Message):
    logger.info(f"User %s selects: %s", msg.from_user.username, msg.text)
    if msg.text == 'Комплексные':
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите первое комплексное число в формате "a+bj"',
                         reply_markup=del_buttons)
        bot.register_next_step_handler(msg, first_step_complex)
    elif msg.text == 'Рациональные':
        bot.register_next_step_handler(msg, process_num1_step_rational)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Введите первое число.',
                         reply_markup=del_buttons)
    elif msg.text == 'Ещё не определился':
        bot.register_next_step_handler(msg, answer)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Возвращайтесь, когда определитесь.')
    else:
        bot.register_next_step_handler(msg, answer)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Пожалуйста, используйте кнопки.')

        bot.send_message(chat_id=msg.from_user.id,
                         text='Выберите режим работы калькулятора.', reply_markup=buttons1)


def process_num1_step_rational(message:  telebot.types.Message, user_result=None):
    try:
        global user_num1
        if user_result == None:
            user_num1 = int(message.text)
        else:
            user_num1 = str(user_result)

        msg = bot.send_message(
            message.chat.id, "Выберите операцию", reply_markup=buttons2)
        bot.register_next_step_handler(msg, process_operation_step_rational)
    except Exception as e:
        bot.reply_to(message, "Введите число!")


def process_operation_step_rational(message: telebot.types.Message):
    try:
        global user_operation
        user_operation = message.text
        msg = bot.send_message(
            message.chat.id, "Введите еще число", reply_markup=del_buttons)
        bot.register_next_step_handler(msg, process_num2_step_rational)
    except Exception as e:
        bot.reply_to(message, "Введите число!")


def process_num2_step_rational(message: telebot.types.Message):
    try:
        global user_num2
        user_num2 = int(message.text)

        msg = bot.send_message(
            message.chat.id, "Смотрим результат или продолжаем вычислять?", reply_markup=buttons3)
        bot.register_next_step_handler(msg, process_alternative_step_rational)
    except Exception as e:
        bot.reply_to(message, "Введите число!")


def process_alternative_step_rational(message: telebot.types.Message):
    try:
        calc()

        if message.text.lower() == "результат":
            bot.send_message(
                message.chat.id, print_calculator(), reply_markup=markup)
        elif message.text.lower() == "считаем дальше":
            process_num1_step_rational(message, user_result)
    except Exception as e:
        bot.reply_to(message, "Ошибка!")


def print_calculator():
    global user_num1, user_num2, user_operation, user_result
    return "Результат: " + str(user_num1) + ' ' + user_operation + ' ' + str(user_num2) + ' = ' + str(user_result)


def calc():
    global user_num1, user_num2, user_operation, user_result
    user_result = eval(str(user_num1) + user_operation + str(user_num2))
    return user_result


def first_step_complex(message: telebot.types.Message, user_result=None):
    try:
        global user_num1
        if user_result == None:
            user_num1 = complex(message.text)
        else:
            user_num1 = str(user_result)

        msg = bot.send_message(
            message.chat.id, "Выберите операцию", reply_markup=buttons2)
        bot.register_next_step_handler(msg, process_operation_step_complex)
    except Exception as e:
        bot.reply_to(message, "Введите комплексное число!")


def process_operation_step_complex(message: telebot.types.Message):
    try:
        global user_operation
        user_operation = message.text
        msg = bot.send_message(
            message.chat.id, "Введите еще комплексное число", reply_markup=del_buttons)
        bot.register_next_step_handler(msg, process_num2_step_complex)
    except Exception as e:
        bot.reply_to(message, "Введите комплексное число!")


def process_num2_step_complex(message: telebot.types.Message):
    try:
        global user_num2
        user_num2 = complex(message.text)

        msg = bot.send_message(
            message.chat.id, "Смотрим результат или продолжаем вычислять?", reply_markup=buttons3)
        bot.register_next_step_handler(msg, process_alternative_step_complex)
    except Exception as e:
        bot.reply_to(message, "Введите число!")


def process_alternative_step_complex(message: telebot.types.Message):
    try:
        calc()
        if message.text.lower() == "результат":
            bot.send_message(message.chat.id, print_calculator(),
                             reply_markup=del_buttons)
        elif message.text.lower() == "считаем дальше":
            first_step_complex(message, user_result)

    except Exception as e:
        bot.reply_to(message, "Ошибка!")


logger.info("Bot started")
bot.polling(none_stop=True, interval=0)
