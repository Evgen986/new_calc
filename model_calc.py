from telebot import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot.types
from config import TOKEN_API


bot = telebot.TeleBot(TOKEN_API)

example = ''

calc_keyboard = InlineKeyboardMarkup(row_width=4)
calc_keyboard.add(InlineKeyboardButton('(', callback_data='('),
                  InlineKeyboardButton(')', callback_data=')'),
                  InlineKeyboardButton('/', callback_data='/'),
                  InlineKeyboardButton('<=', callback_data='<='),
                  InlineKeyboardButton('7', callback_data='7'),
                  InlineKeyboardButton('8', callback_data='8'),
                  InlineKeyboardButton('9', callback_data='9'),
                  InlineKeyboardButton('*', callback_data='*'),
                  InlineKeyboardButton('4', callback_data='4'),
                  InlineKeyboardButton('5', callback_data='5'),
                  InlineKeyboardButton('6', callback_data='6'),
                  InlineKeyboardButton('+', callback_data='+'),
                  InlineKeyboardButton('1', callback_data='1'),
                  InlineKeyboardButton('2', callback_data='2'),
                  InlineKeyboardButton('3', callback_data='3'),
                  InlineKeyboardButton('-', callback_data='-'),
                  InlineKeyboardButton('0', callback_data='0'),
                  InlineKeyboardButton('=', callback_data='='),
                  InlineKeyboardButton('выход', callback_data='выход'),
                  InlineKeyboardButton('i', callback_data='i'))


@bot.message_handler(commands=['calc'])
def calc_command(message: types.Message):
    bot.send_message(message.chat.id, '0', reply_markup=calc_keyboard)


@bot.callback_query_handler(lambda callback: callback.data)
def get_value(callback: types.CallbackQuery):
    global example
    if callback.data == '=':
        str_example, list_example = get_nums(example)
        result = get_result(list_example)
        bot.edit_message_text(f'{str_example} = {result}', callback.message.chat.id, callback.message.id,
                              reply_markup=calc_keyboard)
        example = ''
    elif callback.data == 'выход':
        bot.delete_message(callback.message.chat.id, callback.message.id)
        example = ''
    elif callback.data == '<=':
        if len(example) == 1:
            example = ''
            bot.edit_message_text('0', callback.message.chat.id, callback.message.id, reply_markup=calc_keyboard)
        else:
            example = example[:-1]
            bot.edit_message_text(example, callback.message.chat.id, callback.message.id, reply_markup=calc_keyboard)
    else:  # Если нажата любая из оставшихся кнопок
        example += callback.data
        bot.edit_message_text(example, callback.message.chat.id, callback.message.id, reply_markup=calc_keyboard)


def get_nums(num):  # Получение данных от пользователя
    user_nums = num
    nums = user_nums.replace('+', ' + ') \
        .replace('-', ' - ') \
        .replace('*', ' * ') \
        .replace('/', ' / ') \
        .replace('(', '( ') \
        .replace(')', ' )') \
        .replace('i', 'j') \
        .split()
    nums_list = list()
    for el in nums:
        if 'j' in el:
            nums_list.append(complex(el))
        elif el.isdigit():
            nums_list.append(int(el))
        else:
            nums_list.append(el)
    return user_nums, nums_list


def calc(my_list):  # Функция решения арифметических действий
    while '*' in my_list or '/' in my_list:
        for i in range(1, len(my_list), 2):
            if my_list[i] == '*':
                result = my_list.pop(i + 1) * my_list.pop(i - 1)
                my_list[i - 1] = result
                break
            elif my_list[i] == '/':
                result = my_list.pop(i - 1) / my_list.pop(i)
                my_list[i - 1] = result
                break

    while '+' in my_list or '-' in my_list:
        for i in range(1, len(my_list), 2):
            if my_list[i] == '-':
                result = my_list.pop(i - 1) - my_list.pop(i)
                my_list[i - 1] = result
                break
            elif my_list[i] == '+':
                result = my_list.pop(i + 1) + my_list.pop(i - 1)
                my_list[i - 1] = result
                break

    return my_list


def get_result(data):
    while '(' in data:  # Открытие скобок если они имеются
        first_i = len(data) - data[::-1].index('(') - 1
        second_i = first_i + data[first_i + 1:].index(')') + 1
        data = data[:first_i] + calc(data[first_i + 1:second_i]) + data[second_i + 1:]
    else:
        data = calc(data)  # Вызов функции calc() после открытия скобок
        return ''.join(map(str, data))


bot.polling(none_stop=True)