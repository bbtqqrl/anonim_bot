import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message,  CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import sqlite3
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
import requests
from aiogram.client.default import DefaultBotProperties
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from database import Database
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


# ____________тут більшість взіх змінн та частково кнопки______
# ############################################################################################################################################


db = Database('db.db')

gender_dict_ru = {
    'boy': 'Мужской🤵',
    'girl': 'Женский👸'
}

gender_dict_eng = {
    'boy': 'Male🤵',
    'girl': 'Female👸'
}

gender_dict_ua = {
    'boy': 'Чоловіча🤵',
    'girl': 'Жіноча👸'
}

age_dict_ru = {
    'True': 'Больше 18🔞🍓',
    'False': 'Меньше 18🫣💋'
}

age_dict_eng = {
    'True': 'More than 18🔞🍓',
    'False': 'Less than 18🫣💋'
}

age_dict_ua = {
    'True': 'Більше 18🔞🍓',
    'False': 'Менше 18🫣💋'
}

language_dict = {
    'ua': {'eng' : 'Англійська', 'ru' : 'Російська', 'ua' : 'Українська'},
    'ru': {'eng' : 'Английский', 'ua' : 'Украинский', 'ru' : 'Русский'},
    'eng': {'ua' : 'Ukrainian', 'ru' : 'Russian', 'eng' : 'English'}
}

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

count_mess_1, count_mess_2, count_chat_1, count_chat_2, id_1, id_2, username, marker = 0, 0, 0, 0, 0, 0, 'Пользователь', False
reffer_id = 0

def create_reply_keyboard(buttons, adjust):
    kb = ReplyKeyboardBuilder()
    if type(buttons) == list:
        for button in buttons:
            kb.button(text=button)
        kb.adjust(*adjust)
    else:
        kb.button(text=buttons)
    return kb.as_markup(resize_keyboard=True)

def create_inline_keyboard(buttons, adjust):
    ikb = InlineKeyboardBuilder()
    for button in buttons:
        ikb.button(text=button[0], callback_data=button[1])
    ikb.adjust(*adjust)
    return ikb.as_markup()

# Create reply keyboards
all_kb_ru = create_reply_keyboard(
    ['Парень🔎🤵', '👥Рандом', 'Девушка🔎👸', 'Профиль📖', 'VIP СТАТУС💎', 'Обмен → 💠'], 
    adjust=[3, 3]
)

all_kb_ua = create_reply_keyboard(
    ['Хлопець🔎🤵', '👥Випадковий', 'Дівчина🔎👸', 'Профіль📖', 'VIP СТАТУС💎', 'Обмін → 💠'], 
    adjust=[3, 3]
)

all_kb_eng = create_reply_keyboard(
    ['Boy🔎🤵', '👥Random', 'Girl🔎👸', 'Profile📖', 'VIP STATUS💎', 'Exchange → 💠'], 
    adjust=[3, 3]
)

menu_kb_ru = create_reply_keyboard('Главное меню📋', adjust=[1])
menu_kb_eng = create_reply_keyboard('Main menu📋', adjust=[1])
menu_kb_ua = create_reply_keyboard('Головне меню📋', adjust=[1])
chat_kb_ru = create_reply_keyboard(['Сделать подарок🎁', '/stop'], adjust=[2])
chat_kb_ua = create_reply_keyboard(['Надіслати подарунок🎁', '/stop'], adjust=[2])
chat_kb_eng = create_reply_keyboard(['Make gift🎁', '/stop'], adjust=[2])
stop_kb = create_reply_keyboard('/stop_search', adjust=[1])

# Create inline keyboards
gift_kb_ru = create_inline_keyboard([
    ('Купить баллы💠', 'buy'),
    ('Подарить баллы🎁', 'gift')
], adjust=[1])

gift_kb_ua = create_inline_keyboard([
    ('Купити бали💠', 'buy'),
    ('Надіслати бали🎁', 'gift')
], adjust=[1])

gift_kb_eng = create_inline_keyboard([
    ('Buy points💠', 'buy'),
    ('Gift points🎁', 'gift')
], adjust=[1])

present_kb_ru = create_inline_keyboard([
    ('3 балла💠', 'gift_1'),
    ('10 баллов💠', 'gift_2'),
    ('20 баллов💠', 'gift_3'),
    ('30 баллов💠', 'gift_4')
], adjust=[1])

present_kb_ua = create_inline_keyboard([
    ('3 бали💠', 'gift_1'),
    ('10 балів💠', 'gift_2'),
    ('20 балів💠', 'gift_3'),
    ('30 балів💠', 'gift_4')
], adjust=[1])

present_kb_eng = create_inline_keyboard([
    ('3 points💠', 'gift_1'),
    ('10 points💠', 'gift_2'),
    ('20 points💠', 'gift_3'),
    ('30 points💠', 'gift_4')
], adjust=[1])

top_kb_ru = create_inline_keyboard([
    ('🏆Топ активности🥊', 'activ'),
    ('🏆Топ кармы🎭', 'karma')
], adjust=[1])

top_kb_ua = create_inline_keyboard([
    ('🏆Топ активності🥊', 'activ'),
    ('🏆Топ карми🎭', 'karma')
], adjust=[1])

top_kb_eng = create_inline_keyboard([
    ('🏆Top activities🥊', 'activ'),
    ('🏆Top karma🎭', 'karma')
], adjust=[1])

like_kb = create_inline_keyboard([
    ('👍', 'like'),
    ('👎', 'dislike')
], adjust=[2])

report_kb_ru = create_inline_keyboard([    
    ('👍', 'like'),
    ('👎', 'dislike'),
    ('Жалоба⚠️', 'report')]
, adjust=[2, 1])

report_kb_ua = create_inline_keyboard([
    ('👍', 'like'),
    ('👎', 'dislike'),
    ('Скарга⚠️', 'report')]
, adjust=[2, 1])

report_kb_eng = create_inline_keyboard([
    ('👍', 'like'),
    ('👎', 'dislike'),
    ('Report⚠️','report')]
, adjust=[2, 1])

profile_kb_ru = create_inline_keyboard([
    ('⚙️Редактировать профиль', 'redact'),
    ('📬Реферальная система', 'referal'),
    ('🥇Топы участников', 'top')
], adjust=[1])

profile_kb_eng = create_inline_keyboard([
    ('⚙️Edit profile', 'redact'),
    ('📬Referral system', 'referal'),
    ('🥇Top users', 'top')
], adjust=[1])

profile_kb_ua = create_inline_keyboard([
    ('⚙️Редагувати профіль', 'redact'),
    ('📬Реферальна система', 'referal'),
    ('🥇Топи користувачів', 'top')
], adjust=[1])


language_kb = create_inline_keyboard([
    ('English', 'eng'),
    ('Українська', 'ua'),
    ('Русский', 'ru')
], adjust=[1])

gender_kb_ru = create_inline_keyboard([
    ('Парень🤵', 'boy'),
    ('Девушка👸', 'girl')
], adjust=[1])

gender_kb_ua = create_inline_keyboard([
    ('Хлопець🤵', 'boy'),
    ('Дівчина👸', 'girl')
], adjust=[1])

gender_kb_eng = create_inline_keyboard([
    ('Boy🤵', 'boy'),
    ('Girl👸', 'girl')
], adjust=[1])

shop_kb_ru = create_inline_keyboard([
    ('Сброс дизлайков😉 — 3 балла💠', 'shop_1'),
    ('1 день VIP статуса🏆 — 10 баллов💠', 'shop_2'),
    ('3 дня VIP статуса🏆 — 20 баллов💠', 'shop_3'),
    ('6 дней VIP статуса🏆 — 30 баллов💠', 'shop_4'),
    ('VIP статус👑 НАВСЕГДА — 200 баллов💠', 'shop_5')
], adjust=[1])

shop_kb_ua = create_inline_keyboard([
    ('Скидання дизлайків😉 — 3 бали💠', 'shop_1'),
    ('1 день VIP статусу🏆 — 10 балів💠', 'shop_2'),
    ('3 дні VIP статусу🏆 — 20 балів💠', 'shop_3'),
    ('6 днів VIP статусу🏆 — 30 балів💠', 'shop_4'),
    ('VIP статус👑 НАЗАВЖДИ — 200 балів💠', 'shop_5')
], adjust=[1])

shop_kb_eng = create_inline_keyboard([
    ('Reset dislikes😉 — 3 points💠', 'shop_1'),
    ('1 day of VIP status🏆 — 10 points💠', 'shop_2'),
    ('3 days of VIP status🏆 — 20 points💠', 'shop_3'),
    ('6 days of VIP status🏆 — 30 points💠', 'shop_4'),
    ('VIP status👑 FOREVER — 200 points💠', 'shop_5')
], adjust=[1])



vip_kb_ru = create_inline_keyboard([('КУПИТЬ БАЛЛЫ💠', 'vip_access')], adjust=[1])

vip_kb_eng = create_inline_keyboard([('BUY POINTS💠', 'vip_access')], adjust=[1])

vip_kb_ua = create_inline_keyboard([('КУПИТИ БАЛИ💠', 'vip_access')], adjust=[1])

vip_bool_kb_ru = create_inline_keyboard([
    ('Я оплатил✅', 'yes_vip'),
    ('Отменить❌', 'no_vip')
], adjust=[1])

vip_bool_kb_ua = create_inline_keyboard([
    ('Я оплатив✅', 'yes_vip'),
    ('Відмінити❌', 'no_vip')
], adjust=[1])

vip_bool_kb_eng = create_inline_keyboard([
    ('I payed✅', 'yes_vip'),
    ('Cancel❌', 'no_vip')
], adjust=[1])

age_kb_ru = create_inline_keyboard([
    ('Больше 18🔞🍓', 'True'),
    ('Меньше 18🫣💋', 'False')
], adjust=[1])

age_kb_ua = create_inline_keyboard([
    ('Більше 18🔞🍓', 'True'),
    ('Менше 18🫣💋', 'False')
], adjust=[1])

age_kb_eng = create_inline_keyboard([
    ('More than 18🔞🍓', 'True'),
    ('Less than 18🫣💋', 'False')
], adjust=[1])

search_boy_kb_ru = create_inline_keyboard([
    ('Больше 18🔞🍓', 'boy_True'),
    ('Меньше 18🫣💋', 'boy_False')
], adjust=[1])

search_girl_kb_ru = create_inline_keyboard([
    ('Больше 18🔞🍓', 'girl_True'),
    ('Меньше 18🫣💋', 'girl_False')
], adjust=[1])

search_boy_kb_ua = create_inline_keyboard([
    ('Більше 18🔞🍓', 'boy_True'),
    ('Менше 18🫣💋', 'boy_False')
], adjust=[1])

search_girl_kb_ua = create_inline_keyboard([
    ('Більше 18🔞🍓', 'girl_True'),
    ('Менше 18🫣💋', 'girl_False')
], adjust=[1])

search_boy_kb_eng = create_inline_keyboard([
    ('More than 18🔞🍓', 'boy_True'),
    ('Less than 18🫣💋', 'boy_False')
], adjust=[1])

search_girl_kb_eng = create_inline_keyboard([
    ('More than 18🔞🍓', 'girl_True'),
    ('Less than 18🫣💋', 'girl_False')
], adjust=[1])


search_gender_kb_ru = create_inline_keyboard([
    ('Парень🔎🤵', 'search_boy'),
    ('Девушка🔎👸', 'search_girl')
], adjust=[1])

search_gender_kb_ua = create_inline_keyboard([
    ('Хлопець🔎🤵', 'search_boy'),
    ('Дівчина🔎👸', 'search_girl')
], adjust=[1])

search_gender_kb_eng = create_inline_keyboard([
    ('Boy🔎🤵', 'search_boy'),
    ('Girl🔎👸', 'search_girl')
], adjust=[1])

bool_kb_ru = create_inline_keyboard([
    ('ДА✅', 'yes_name'),
    ('НЕТ❌', 'no_name')
], adjust=[1])

bool_kb_ua = create_inline_keyboard([
    ('Так✅', 'yes_name'),
    ('Ні❌', 'no_name')
], adjust=[1])

bool_kb_eng = create_inline_keyboard([
    ('YES✅', 'yes_name'),
    ('NO❌', 'no_name')
], adjust=[1])

redakt_kb_ru = create_inline_keyboard([
    ('ДА✅', 'yes_name_redakt'),
    ('НЕТ❌', 'no_name_redakt')
], adjust=[1])

redakt_kb_ua = create_inline_keyboard([
    ('Так✅', 'yes_name_redakt'),
    ('Ні❌', 'no_name_redakt')
], adjust=[1])

redakt_kb_eng = create_inline_keyboard([
    ('YES✅', 'yes_name_redakt'),
    ('NO❌', 'no_name_redakt')
], adjust=[1])

# ############################################################################################################################################
# ############################################################################################################################################



        
# функцыонал гендеру, меню ы тд_____________________________________
# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp.message(F.text.in_(['Профиль📖', 'Профіль📖', 'Profile📖']))
async def profile(message: Message):
    global username
    username = message.from_user.first_name
    vip_ru = 'Присутсвует' if db.get_vip(message.chat.id) != '0' else 'Отсутсвует'
    vip_eng = 'True' if db.get_vip(message.chat.id) != '0' else 'False'
    vip_ua = 'Присутній' if db.get_vip(message.chat.id) != '0' else 'Відсутній'
    language = db.get_language(message.chat.id)

    if language == 'ru':
        await message.answer(
            f'<b>Ваш профиль👾 \n\n#️⃣ ID: <em><code>{message.chat.id}</code></em> \n'
            f'📚 Язык: Русский\n'
            f'👫 Пол:  <em>{gender_dict_ru[db.get_gender(message.chat.id)]}</em>\n'
            f'😇Возраст: <em>{age_dict_ru[db.get_age(message.chat.id)]}\n\n'
            f'🏆VIP статус: {vip_ru}\n👑VIP никнейм: {db.get_vip_name(message.chat.id)}\n\n'
            f'💬Сообщений : {db.show_num_mess(message.chat.id)}\n'
            f'💌Чатов : {db.show_num_chat(message.chat.id)}     </em> \n\n'
            f'🎭Ваша карма⤵️\n<em>Лайков 👍 : {db.get_like(message.chat.id)}\n'
            f'Дизлайков 👎 : {db.get_dislike(message.chat.id)}</em>\n\n'
            f'💼Реф. профиль⤵️<em>\nПриглашено юзеров👥: {db.get_reffer(message.chat.id)[0]}\n'
            f'Реферальных баллов💠: {db.get_reffer(message.chat.id)[1]}</em></b>',
            reply_markup=profile_kb_ru
        )
    elif language == 'eng':
        await message.answer(
            f'<b>Your Profile👾 \n\n#️⃣ ID: <em><code>{message.chat.id}</code></em> \n'
            f'📚 Language: English\n'
            f'👫 Gender:  <em>{gender_dict_eng[db.get_gender(message.chat.id)]}</em>\n'
            f'😇 Age: <em>{age_dict_eng[db.get_age(message.chat.id)]}\n\n'
            f'🏆 VIP Status: {vip_eng}\n👑 VIP Nickname: {db.get_vip_name(message.chat.id)}\n\n'
            f'💬 Messages: {db.show_num_mess(message.chat.id)}\n'
            f'💌 Chats: {db.show_num_chat(message.chat.id)}     </em> \n\n'
            f'🎭 Your Karma⤵️\n<em>Likes 👍: {db.get_like(message.chat.id)}\n'
            f'Dislikes 👎: {db.get_dislike(message.chat.id)}</em>\n\n'
            f'💼 Referral Profile⤵️<em>\nInvited Users👥: {db.get_reffer(message.chat.id)[0]}\n'
            f'Referral Points💠: {db.get_reffer(message.chat.id)[1]}</em></b>',
            reply_markup=profile_kb_eng
        )

    elif language == 'ua':
        await message.answer(
            f'<b>Ваш профіль👾 \n\n#️⃣ ID: <em><code>{message.chat.id}</code></em> \n'
            f'📚 Мова: Українська\n'
            f'👫 Стать:  <em>{gender_dict_ua[db.get_gender(message.chat.id)]}</em>\n'
            f'😇 Вік: <em>{age_dict_ua[db.get_age(message.chat.id)]}\n\n'
            f'🏆 VIP статус: {vip_ua}\n👑 VIP нікнейм: {db.get_vip_name(message.chat.id)}\n\n'
            f'💬 Повідомлень: {db.show_num_mess(message.chat.id)}\n'
            f'💌 Чатів: {db.show_num_chat(message.chat.id)}     </em> \n\n'
            f'🎭 Ваша карма⤵️\n<em>Лайків 👍: {db.get_like(message.chat.id)}\n'
            f'Дизлайків 👎: {db.get_dislike(message.chat.id)}</em>\n\n'
            f'💼 Реф. профіль⤵️<em>\nЗапрошено користувачів👥: {db.get_reffer(message.chat.id)[0]}\n'
            f'Реферальних балів💠: {db.get_reffer(message.chat.id)[1]}</em></b>',
            reply_markup=profile_kb_ua
        )

# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp.message(F.text.in_(['VIP СТАТУС💎', 'VIP STATUS💎']))
async def vip(message: Message):
    global username
    username = message.from_user.first_name

    language = db.get_language(message.chat.id)
    
    photo = FSInputFile("vip_photo.jpg")
    if language == 'ru':
        await message.answer_photo(
            photo,
            caption='Преимущества<b> VIP статуса👑⤵️</b>\n\n<em>1️⃣. <b>БАН</b> спам рекламы🛑\n'
                    '2️⃣. Никаких ограничений🤑\n3️⃣. Всегда <b>ПЕРВЫЙ</b> в поиске!!!\n'
                    '4️⃣. Поиск по <b>возрасту</b>🤫(/vip_search)...\n5️⃣. <b>ВСЕ</b> будут видеть твой статус💠\n'
                    '6️⃣. Ты сможешь создать свой ник🔥\n7️⃣. Возможность <b>ПОЖАЛОВАТЬСЯ</b> на плохого собеседника🚫\n'
                    '🎱. И в конце концов ты сможешь получить VIP <b>БЕСПЛАТНО</b>❤️‍🔥\n\n'
                    'Да и ты получишь возможность увидеть себя в <b>топе VIP🏆 активности</b>\n\n'
                    'Любим каждого💕💕💕</em>',
            )
        await message.answer(
            f'<b><em>VIP🏆 статус</em> покупается за баллы в /shop , а здесь можно купить балы по курсу⤵️\n\n'
            f'1 балл💠 - <em>2 рубля или 0,92 гривны\n\n⚠️⚠️ВНИМАНИЕ⚠️⚠️</em>\n'
            f'При покупке баллов вам нужно вставить ваш ID или ID пользователя которому вы хотите сделать подарок '
            f'в поле "Имя" или "Ім`я"  . Тогда покупка будет зарегистрирована и вам придет уведомление/)\n\n'
            f'Ваш ID - <code>{message.chat.id}</code>⚠️\n\n<em>Любим каждого💕💕💕</em></b>',
            reply_markup=vip_kb_ru
        )
    
    if language == 'eng':
        await message.answer_photo(
            photo,
            caption='Advantages of <b>VIP status👑⤵️</b>\n\n<em>1️⃣. <b>BAN</b> for spam advertising🛑\n'
                '2️⃣. No restrictions at all🤑\n3️⃣. Always <b>FIRST</b> in search!!!\n'
                '4️⃣. Search by <b>age</b>🤫(/vip_search)...\n5️⃣. <b>EVERYONE</b> will see your status💠\n'
                '6️⃣. You can create your own nickname🔥\n7️⃣. Ability to <b>REPORT</b> a bad chat partner🚫\n'
                '🎱. And finally, you can get VIP <b>FOR FREE</b>❤️‍🔥\n\n'
                'Plus, you’ll get a chance to see yourself in the <b>top VIP🏆 activity</b>\n\n'
                'We love each of you💕💕💕</em>',
            )
        await message.answer(
            f'<b><em>VIP🏆 status</em> is purchased with points in /shop, and here you can buy points at the rate⤵️\n\n'
            f'1 point💠 - <em>0.1$\n\n⚠️⚠️ATTENTION⚠️⚠️</em>\n'
            f'When purchasing points, you need to enter your ID or the ID of the user you want to gift points to '
            f'in the "Name" field. This will register the purchase, and you will receive a notification.\n\n'
            f'Your ID - <code>{message.chat.id}</code>⚠️\n\n<em>We love each of you💕💕💕</em></b>',
            reply_markup=vip_kb_eng
        )
    elif language == 'ua':
        await message.answer_photo(
            photo,
            caption='Переваги <b>VIP статусу👑⤵️</b>\n\n<em>1️⃣. <b>БАН</b> за спам-рекламу🛑\n'
                '2️⃣. Жодних обмежень🤑\n3️⃣. Завжди <b>ПЕРШИЙ</b> у пошуку!!!\n'
                '4️⃣. Пошук за <b>віком</b>🤫(/vip_search)...\n5️⃣. <b>ВСІ</b> бачитимуть твій статус💠\n'
                '6️⃣. Ти зможеш створити власний нік🔥\n7️⃣. Можливість <b>ПОСКАРЖИТИСЯ</b> на поганого співрозмовника🚫\n'
                '🎱. І, зрештою, ти зможеш отримати VIP <b>БЕЗКОШТОВНО</b>❤️‍🔥\n\n'
                'А також матимеш шанс побачити себе в <b>топі VIP🏆 активності</b>\n\n'
                'Любимо кожного💕💕💕</em>',
            )
        await message.answer(
            f'<b><em>VIP🏆 статус</em> купується за бали в /shop, а тут можна купити бали за курсом⤵️\n\n'
            f'1 бал💠 - <em>2 рублі або 0,92 гривні\n\n⚠️⚠️УВАГА⚠️⚠️</em>\n'
            f'При купівлі балів вам потрібно вказати ваш ID або ID користувача, якому хочете зробити подарунок, '
            f'у полі "Ім’я". Тоді покупка буде зареєстрована, і вам прийде повідомлення.\n\n'
            f'Ваш ID - <code>{message.chat.id}</code>⚠️\n\n<em>Любимо кожного💕💕💕</em></b>',
            reply_markup=vip_kb_ua
        )



# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp.message(F.text.in_(['Главное меню📋', 'Головне меню📋', 'Main menu📋']))
async def menu(message: Message):
    language = db.get_language(message.chat.id)
    if language == 'ru':
        await message.answer('<b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>', reply_markup=all_kb_ru)
    elif language == 'ua':
        await message.answer('<b>\nㅤㅤ↓ <em> Головне меню📋 </em>↓</b>', reply_markup=all_kb_ua)
    elif language == 'eng':
        await message.answer('<b>\nㅤㅤ↓ <em> Main menu📋 </em>↓</b>', reply_markup=all_kb_eng)

# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp.message(F.text.in_(['Обмен → 💠', 'Обмін → 💠', 'Exchange → 💠']))
async def exchange_shop(message: Message):
    language = db.get_language(message.chat.id)
    global username
    username = message.from_user.first_name
    if language == 'ru':
        await message.answer(
            f'<b>Наш магазин для обмена баллов💠⤵️\n\n'
            f'Ваших баллов: {db.get_reffer(message.chat.id)[1]}💎\n\n'
            f'Как получить баллы, вы можете узнать в <em>Мой профиль📖</em> → <em>📬Реферальная система</em></b>', 
            reply_markup=shop_kb_ru
        )
    elif language == 'ua':
        await message.answer(
            f'<b>Наш магазин для обміну балів💠⤵️\n\n'
            f'Ваших балів: {db.get_reffer(message.chat.id)[1]}💎\n\n'
            f'Як отримати бали, ви можете дізнатися в <em>Мій профіль📖</em> → <em>📬Реферальна система</em></b>', 
            reply_markup=shop_kb_ua
        )
    elif language == 'eng':
        await message.answer(
            f'<b>Our shop for exchanging points💠⤵️\n\n'
            f'Your points: {db.get_reffer(message.chat.id)[1]}💎\n\n'
            f'How to get points? Check <em>My Profile📖</em> → <em>📬Referral System</em></b>', 
            reply_markup=shop_kb_eng
        )

# ############################################################################################################################################
# ############################################################################################################################################




# # _______________команди і функції_______________
# # ############################################################################################################################################

@dp.message(Command('stats_bbtqqrl'))
async def stop_search(message: Message):
    await message.answer(f'Кількість людей: {db.get_activ()}')      



@dp.message(Command('start'))

async def start(message: Message):
    if not db.get_active_chat(message.chat.id):
            
        if db.check_user(message.chat.id):
            language = db.get_language(message.chat.id)
            await message.answer_sticker(sticker='CAACAgIAAxkBAAEI4-tkV4lOb3MNjmu-FuZ6TBl1daqalQACZAEAAntOKhAOzIvWIO0fji8E')
            if language == 'eng': 
                await message.answer(text=f'<b>Снова здраствуй в нашем анонимном чат боте🤗 \n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb_ru)
            elif language == 'ua':
                await message.answer(text=f'<b>Привіт тобі знову в нашому анонімному чат-боті🤗 \n ↓<em>Меню📋</em>↓</b>', reply_markup=all_kb_ua)
            elif language == 'ru':
                await message.answer(text=f'<b>Welcome back to our anonymous chat bot🤗 \n ↓<em>Menu📋</em>↓</b>', reply_markup=all_kb_eng)

        else:
            global reffer_id
            try:
                reffer_id = int(message.text[7:])
            except:
                reffer_id = False
            await message.answer(f'<b>Hello, user!\nPlease choose your language📚⤵️</b>', reply_markup=language_kb)


    else:
        language = db.get_language(message.chat.id)
        if language == 'ru':
            await message.answer(f'<b>Вы не можете отправлять команды в чате, что бы его остановить используйте команду /stop</b>', reply_markup= chat_kb_ru)
        elif language == 'ua':
            await message.answer(f'<b>Ви не можете відправляти команди в чаті, щоб його зупинити використовуйте команду /stop</b>', reply_markup=chat_kb_ua)
        elif language == 'eng':
            await message.answer(f'<b>You cannot send commands in the chat, to stop it use the command /stop</b>', reply_markup=chat_kb_eng)     




@dp.message(Command('stop_search'))
async def stop_search(message: Message):
    language = db.get_language(message.chat.id)
    if not db.get_active_chat(message.chat.id):
        global last_start_mes
        if not db.check_queue(message.chat.id):
            db.del_queue(message.chat.id)
            try:
                await bot.delete_message(message.chat.id, last_start_mes.message_id)
                last_start_mes = None
            except:
                pass
            if language == 'ru':
                await message.answer(f'<b>ㅤВы остановили поиск😣\nㅤㅤㅤ↓ <em> Главное меню📋 </em>↓</b>', reply_markup=all_kb_ru)
            elif language == 'ua':
                await message.answer(f'<b>ㅤВи зупинили пошук😣\nㅤㅤㅤ↓ <em> Головне меню📋 </em>↓</b>', reply_markup=all_kb_ua)
            elif language == 'eng':
                await message.answer(f'<b>ㅤYou stopped the search😣\nㅤㅤㅤ↓ <em> Main menu📋 </em>↓</b>', reply_markup=all_kb_eng)
        elif db.check_queue(message.chat.id):
            if language == 'ru':
                await message.answer(f'<b>ㅤВы не начали поиск😣\nㅤㅤㅤ↓ <em> Главное меню📋 </em>↓</b>', reply_markup=all_kb_ru)
            elif language == 'ua':
                await message.answer(f'<b>ㅤВи не почали пошук😣\nㅤㅤㅤ↓ <em> Головне меню📋 </em>↓</b>', reply_markup=all_kb_ua)
            elif language == 'eng':
                await message.answer(f'<b>ㅤYou haven\'t started the search😣\nㅤㅤㅤ↓ <em> Main menu📋 </em>↓</b>', reply_markup=all_kb_eng)
    else:
        if language == 'ru':
            await message.answer(f'<b>Вы не можете отправлять команды в активном чате, чтобы его остановить используйте команду /stop</b>', reply_markup=chat_kb_ru)
        elif language == 'ua':
            await message.answer(f'<b>Ви не можете відправляти команди в активному чаті, щоб його зупинити використовуйте команду /stop</b>', reply_markup=chat_kb_ua)
        elif language == 'eng':
            await message.answer(f'<b>You cannot send commands in an active chat, to stop it use the command /stop</b>', reply_markup=chat_kb_eng)

@dp.message(Command('stop'))
async def stop_chat(message: Message):
    global count_mess_1, count_chat_1, count_mess_2, count_chat_2, id_1, id_2
    language = db.get_language(message.chat.id)
    if db.get_active_chat(message.chat.id):        
        try:            
            if message.chat.id == id_2:
                id_2, id_1 = id_1, id_2
            language_1 = db.get_language(message.chat.id)
            language_2 = db.get_language(id_2)
            kb = like_kb
            if db.get_vip(id_2) != '0':
                kb = eval(f"report_kb_{language_2}")
            if language_2 == 'ru':
                await bot.send_message(chat_id=id_2, text=f'<b>Ваш собеседник закончил диалог🤧</b>', reply_markup=menu_kb_ru)
                await bot.send_message(chat_id=id_2, text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup=kb)
            elif language_2 == 'ua':
                await bot.send_message(chat_id=id_2, text=f'<b>Ваш співрозмовник закінчив діалог🤧</b>', reply_markup=menu_kb_ua)
                await bot.send_message(chat_id=id_2, text=f'<b><em>Оцініть співрозмовника👫\n</em> ↓ <em>Або поверніться в меню📋</em>↓</b>', reply_markup=kb)
            elif language_2 == 'eng':
                await bot.send_message(chat_id=id_2, text=f'<b>Your chat partner ended the dialogue🤧</b>', reply_markup=menu_kb_eng)
                await bot.send_message(chat_id=id_2, text=f'<b><em>Rate your chat partner👫\n</em> ↓ <em>Or return to the menu📋</em>↓</b>', reply_markup=kb)
            
            kb = like_kb                
            if db.get_vip(message.chat.id) != '0':
                kb = eval(f"report_kb_{language_1}")
            if language_1 == 'ru':
                await bot.send_message(chat_id=message.chat.id, text=f'<b>Вы закончили диалог🤧</b>', reply_markup=menu_kb_ru)
                await bot.send_message(chat_id=message.chat.id, text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup=kb)
            elif language_1 == 'ua':
                await bot.send_message(chat_id=message.chat.id, text=f'<b>Ви закінчили діалог🤧</b>', reply_markup=menu_kb_ua)
                await bot.send_message(chat_id=message.chat.id, text=f'<b><em>Оцініть співрозмовника👫\n</em> ↓ <em>Або поверніться в меню📋</em>↓</b>', reply_markup=kb)
            elif language_1 == 'eng':
                await bot.send_message(chat_id=message.chat.id, text=f'<b>You ended the dialogue🤧</b>', reply_markup=menu_kb_eng)
                await bot.send_message(chat_id=message.chat.id, text=f'<b><em>Rate your chat partner👫\n</em> ↓ <em>Or return to the menu📋</em>↓</b>', reply_markup=kb)
            db.add_mess_chat(message.chat.id, count_mess_2, count_chat_2 + 1)
            db.add_mess_chat(db.get_active_chat(message.chat.id)[1], count_mess_1, count_chat_1 + 1)  
            db.del_chat(db.get_active_chat(message.chat.id)[0])
            
        except:
            if language == 'ru':
                await message.answer(text=f'<b>Вы не начали чат☹️! \n ↓<em>Меню📋</em>↓</b>', reply_markup=menu_kb_ru)
            elif language == 'ua':
                await message.answer(text=f'<b>Ви не почали чат☹️! \n ↓<em>Меню📋</em>↓</b>', reply_markup=menu_kb_ua)
            elif language == 'eng':
                await message.answer(text=f'<b>You haven\'t started a chat☹️! \n ↓<em>Menu📋</em>↓</b>', reply_markup=menu_kb_eng)

    else:
        if language == 'ru':
            await message.answer(text=f'<b>Вы не начали чат☹️! \n ↓<em>Меню📋</em>↓</b>', reply_markup=menu_kb_ru)
        elif language == 'ua':
            await message.answer(text=f'<b>Ви не почали чат☹️! \n ↓<em>Меню📋</em>↓</b>', reply_markup=menu_kb_ua)
        elif language == 'eng':
            await message.answer(text=f'<b>You haven\'t started a chat☹️! \n ↓<em>Menu📋</em>↓</b>', reply_markup=menu_kb_eng)


@dp.message(Command('alert_text'))
async def start(message: Message):
    global marker
    if message.chat.id == 1135699139:
        marker = 'alert_text'
    
@dp.message(Command('alert_photo'))
async def start(message: Message):
    global marker
    if message.chat.id == 1135699139 or message.chat.id == '1135699139' or message.from_user.username == 'bbtqqrl':
        marker = 'alert_photo'
        
@dp.message(Command('alert_photo'))
async def start(message: Message):
    global marker
    if message.chat.id == 1135699139 or message.chat.id == '1135699139' or message.from_user.username == 'bbtqqrl':
        marker = 'alert_photo'
        
@dp.message(Command('menu'))
async def command_start_search(message: Message):
    language = db.get_language(message.chat.id)
    if not db.get_active_chat(message.chat.id):
        if not check_vip(message.chat.id):
            if language == 'ru':
                await message.answer(text='<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>')
            elif language == 'ua':
                await message.answer(text='<b>На жаль, ваш <em>VIP статус🏆</em> закінчився...\n\nЯкщо вам сподобалось, ви можете обміняти <em>бали💠</em> на <em>VIP статус🏆</em>(/shop) або купити командою (/vip)\n\n<em>Гарних вам співрозмовників💋👥</em></b>')
            elif language == 'eng':
                await message.answer(text='<b>Unfortunately, your <em>VIP status🏆</em> has expired...\n\nIf you liked it, you can exchange <em>points💠</em> for <em>VIP status🏆</em>(/shop) or buy it with the command (/vip)\n\n<em>Have great conversations💋👥</em></b>')
            return
        else:
            pass
        if language == 'ru':
            await message.answer(f'<b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>', reply_markup=all_kb_ru)
        elif language == 'ua':
            await message.answer(f'<b>\nㅤㅤ↓ <em> Головне меню📋 </em>↓</b>', reply_markup=all_kb_ua)
        elif language == 'eng':
            await message.answer(f'<b>\nㅤㅤ↓ <em> Main menu📋 </em>↓</b>', reply_markup=all_kb_eng)
    else:
        if language == 'ru':
            await message.answer(f'<b>Вы не можете отправлять команды в чате, чтобы его остановить используйте команду /stop</b>', reply_markup=chat_kb_ru)
        elif language == 'ua':
            await message.answer(f'<b>Ви не можете відправляти команди в чаті, щоб його зупинити використовуйте команду /stop</b>', reply_markup=chat_kb_ua)
        elif language == 'eng':
            await message.answer(f'<b>You cannot send commands in the chat, to stop it use the command /stop</b>', reply_markup=chat_kb_eng)

@dp.message(Command('vip'))
async def vip(message: Message):
    language = db.get_language(message.chat.id)
    if not db.get_active_chat(message.chat.id):
        global username
        username = message.from_user.first_name
        photo = FSInputFile("vip_photo.jpg")
        if language == 'ru':
            await message.answer_photo(photo, caption='Преимущества<b> VIP статуса👑⤵️</b>\n\n<em>1️⃣. <b>БАН</b> спам рекламы🛑\n2️⃣. Никаких ограничений🤑\n3️⃣. Всегда <b>ПЕРВЫЙ</b> в поиске!!!\n4️⃣. Поиск по <b>возрасту</b>🤫(/vip_search)...\n5️⃣. <b>ВСЕ</b> будут видеть твой статус💠\n6️⃣. Ты сможешь создать свой ник🔥\n7️⃣. Возможность <b>ПОЖАЛОВАТЬСЯ</b> на плохого собеседника🚫\n🎱. И в конце концов ты сможешь получить VIP <b>БЕСПЛАТНО</b>❤️‍🔥\n\nДа и ты получишь возможность увидеть себя в <b>топе VIP🏆 активности</b>\n\nЛюбим каждого💕💕💕</em>')
            await message.answer(text=f'<b><em>VIP🏆 статус</em> покупается за баллы в /shop , а здесь можно купить балы по курсу⤵️\n\n1 балл💠 - <em>2 рубля или 0,92 гривны\n\n⚠️⚠️ВНИМАНИЕ⚠️⚠️</em>\nПри покупке баллов вам нужно вставить ваш ID или ID пользователя которому вы хотите сделать подарок в поле "Имя" или "Ім`я"  . Тогда покупка будет зарегистрирована и вам придет уведомление/)\n\nВаш ID - <code>{message.chat.id}</code>⚠️\n\n<em>Любим каждого💕💕💕</em></b>', reply_markup=vip_kb_ru)
        elif language == 'ua':
            await message.answer_photo(photo, caption='Переваги<b> VIP статусу👑⤵️</b>\n\n<em>1️⃣. <b>БАН</b> спам реклами🛑\n2️⃣. Жодних обмежень🤑\n3️⃣. Завжди <b>ПЕРШИЙ</b> у пошуку!!!\n4️⃣. Пошук за <b>віком</b>🤫(/vip_search)...\n5️⃣. <b>ВСІ</b> бачитимуть твій статус💠\n6️⃣. Ти зможеш створити свій нік🔥\n7️⃣. Можливість <b>ПОСКАРЖИТИСЯ</b> на поганого співрозмовника🚫\n🎱. І врешті-решт ти зможеш отримати VIP <b>БЕЗКОШТОВНО</b>❤️‍🔥\n\nТа й ти отримаєш можливість побачити себе в <b>топі VIP🏆 активності</b>\n\nЛюбимо кожного💕💕💕</em>')
            await message.answer(text=f'<b><em>VIP🏆 статус</em> купується за бали в /shop , а тут можна купити бали за курсом⤵️\n\n1 бал💠 - <em>2 рублі або 0,92 гривні\n\n⚠️⚠️УВАГА⚠️⚠️</em>\nПри купівлі балів вам потрібно вставити ваш ID або ID користувача, якому ви хочете зробити подарунок у поле "Ім\'я" або "Имя". Тоді покупка буде зареєстрована і вам прийде повідомлення/)\n\nВаш ID - <code>{message.chat.id}</code>⚠️\n\n<em>Любимо кожного💕💕💕</em></b>', reply_markup=vip_kb_ua)
        elif language == 'eng':
            await message.answer_photo(photo, caption='Benefits of<b> VIP status👑⤵️</b>\n\n<em>1️⃣. <b>BAN</b> spam ads🛑\n2️⃣. No limitations🤑\n3️⃣. Always <b>FIRST</b> in search!!!\n4️⃣. Search by <b>age</b>🤫(/vip_search)...\n5️⃣. <b>EVERYONE</b> will see your status💠\n6️⃣. You can create your own nickname🔥\n7️⃣. Ability to <b>REPORT</b> a bad interlocutor🚫\n🎱. And finally, you can get VIP <b>FOR FREE</b>❤️‍🔥\n\nAnd you\'ll have the opportunity to see yourself in the <b>top VIP🏆 activity</b>\n\nWe love everyone💕💕💕</em>')
            await message.answer(text=f'<b><em>VIP🏆 status</em> is purchased with points in /shop , and here you can buy points at the rate⤵️\n\n1 point💠 - <em>2 rubles or 0.92 hryvnia\n\n⚠️⚠️ATTENTION⚠️⚠️</em>\nWhen buying points, you need to insert your ID or the ID of the user you want to gift in the "Name" field. Then the purchase will be registered and you will receive a notification/)\n\nYour ID - <code>{message.chat.id}</code>⚠️\n\n<em>We love everyone💕💕💕</em></b>', reply_markup=vip_kb_eng)
    else:
        if language == 'ru':
            await message.answer(f'<b>Вы не можете отправлять команды в чате, чтобы его остановить используйте команду /stop</b>', reply_markup=chat_kb_ru)
        elif language == 'ua':
            await message.answer(f'<b>Ви не можете відправляти команди в чаті, щоб його зупинити використовуйте команду /stop</b>', reply_markup=chat_kb_ua)
        elif language == 'eng':
            await message.answer(f'<b>You cannot send commands in the chat, to stop it use command /stop</b>', reply_markup=chat_kb_eng)

@dp.message(Command('shop'))
async def shop(message: Message):
    language = db.get_language(message.chat.id)
    if not db.get_active_chat(message.chat.id):
        if language == 'ru':
            await message.answer(f'<b>\nНаш магазин для обмена баллов💠⤵️\n\n А как получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em></b>', reply_markup=shop_kb_ru)
        elif language == 'ua':
            await message.answer(f'<b>\nНаш магазин для обміну балів💠⤵️\n\n А як отримати бали ви можете дізнатися в <em> Мій профіль📖</em>  →  <em>📬Реферальна система </em></b>', reply_markup=shop_kb_ua)
        elif language == 'eng':
            await message.answer(f'<b>\nOur shop for exchanging points💠⤵️\n\n You can learn how to get points in <em> My profile📖</em>  →  <em>📬Referral system </em></b>', reply_markup=shop_kb_eng)
    else:
        if language == 'ru':
            await message.answer(f'<b>Вы не можете отправлять команды в чате, чтобы его остановить используйте команду /stop</b>', reply_markup=chat_kb_ru)
        elif language == 'ua':
            await message.answer(f'<b>Ви не можете відправляти команди в чаті, щоб його зупинити використовуйте команду /stop</b>', reply_markup=chat_kb_ua)
        elif language == 'eng':
            await message.answer(f'<b>You cannot send commands in the chat, to stop it use the command /stop</b>', reply_markup=chat_kb_eng)

            
@dp.message(Command('vip_search'))
async def command_start_search(message: Message): 
    language = db.get_language(message.chat.id)
    if not db.get_active_chat(message.chat.id):
        global username
        if not check_vip(message.chat.id):
            if language == 'ru':
                await message.answer(text='<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>')
                return await message.answer(text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb_ru)
            elif language == 'ua':
                await message.answer(text='<b>На жаль, ваш <em>VIP статус🏆</em> закінчився...\n\nЯкщо вам сподобалось, ви можете обміняти <em>бали💠</em> на <em>VIP статус🏆</em>(/shop) або купити командою (/vip)\n\n<em>Гарних вам співрозмовників💋👥</em></b>')
                return await message.answer(text=f'<b>ㅤㅤ↓  Головне меню📋 ↓</b>', reply_markup=all_kb_ua)
            elif language == 'eng':
                await message.answer(text='<b>Unfortunately, your <em>VIP status🏆</em> has expired...\n\nIf you liked it, you can exchange <em>points💠</em> for <em>VIP status🏆</em>(/shop) or buy it with the command (/vip)\n\n<em>Have great conversations💋👥</em></b>')
                return await message.answer(text=f'<b>ㅤㅤ↓  Main menu📋 ↓</b>', reply_markup=all_kb_eng)
        
        if db.get_vip(message.chat.id) != '0':
            if language == 'ru':
                await message.answer(f'<b>Снова здравствуй 🏆VIP пользователь⤵️\nНикнейм: {db.get_vip_name(message.chat.id)}\n\n👑Кого искать👥?</b>', reply_markup=search_gender_kb_ru)
            elif language == 'ua':
                await message.answer(f'<b>Знову вітаю 🏆VIP користувач⤵️\nНікнейм: {db.get_vip_name(message.chat.id)}\n\n👑Кого шукати👥?</b>', reply_markup=search_gender_kb_ua)
            elif language == 'eng':
                await message.answer(f'<b>Hello again 🏆VIP user⤵️\nNickname: {db.get_vip_name(message.chat.id)}\n\n👑Who to search for👥?</b>', reply_markup=search_gender_kb_eng)
        elif db.get_vip(message.chat.id) == '0':
            username = message.from_user.first_name
            photo = FSInputFile("vip_photo.jpg")
            if language == 'ru':
                await message.answer_photo(photo, caption='Преимущества<b> VIP статуса👑⤵️</b>\n\n<em>1️⃣. <b>БАН</b> спам рекламы🛑\n2️⃣. Никаких ограничений🤑\n3️⃣. Всегда <b>ПЕРВЫЙ</b> в поиске!!!\n4️⃣. Поиск по <b>возрасту</b>🤫(/vip_search)...\n5️⃣. <b>ВСЕ</b> будут видеть твой статус💠\n6️⃣. Ты сможешь создать свой ник🔥\n7️⃣. Возможность <b>ПОЖАЛОВАТЬСЯ</b> на плохого собеседника🚫\n🎱. И в конце концов ты сможешь получить VIP <b>БЕСПЛАТНО</b>❤️‍🔥\n\nДа и ты получишь возможность увидеть себя в <b>топе VIP🏆 активности</b>\n\nЛюбим каждого💕💕💕</em>')
                await message.answer(text=f'<b><em>VIP🏆 статус</em> покупается за баллы в /shop , а здесь можно купить балы по курсу⤵️\n\n1 балл💠 - <em>2 рубля или 0,92 гривны\n\n⚠️⚠️ВНИМАНИЕ⚠️⚠️</em>\nПри покупке баллов вам нужно вставить ваш ID или ID пользователя которому вы хотите сделать подарок в поле "Имя" или "Ім`я"  . Тогда покупка будет зарегистрирована и вам придет уведомление/)\n\nВаш ID - <code>{message.chat.id}</code>⚠️\n\n<em>Любим каждого💕💕💕</em></b>', reply_markup=vip_kb_ru)
            elif language == 'ua':
                await message.answer_photo(photo, caption='Переваги<b> VIP статусу👑⤵️</b>\n\n<em>1️⃣. <b>БАН</b> спам реклами🛑\n2️⃣. Жодних обмежень🤑\n3️⃣. Завжди <b>ПЕРШИЙ</b> у пошуку!!!\n4️⃣. Пошук за <b>віком</b>🤫(/vip_search)...\n5️⃣. <b>ВСІ</b> бачитимуть твій статус💠\n6️⃣. Ти зможеш створити свій нік🔥\n7️⃣. Можливість <b>ПОСКАРЖИТИСЯ</b> на поганого співрозмовника🚫\n🎱. І врешті-решт ти зможеш отримати VIP <b>БЕЗКОШТОВНО</b>❤️‍🔥\n\nТа й ти отримаєш можливість побачити себе в <b>топі VIP🏆 активності</b>\n\nЛюбимо кожного💕💕💕</em>')
                await message.answer(text=f'<b><em>VIP🏆 статус</em> купується за бали в /shop , а тут можна купити бали за курсом⤵️\n\n1 бал💠 - <em>2 рублі або 0,92 гривні\n\n⚠️⚠️УВАГА⚠️⚠️</em>\nПри купівлі балів вам потрібно вставити ваш ID або ID користувача, якому ви хочете зробити подарунок у поле "Ім\'я" або "Имя". Тоді покупка буде зареєстрована і вам прийде повідомлення/)\n\nВаш ID - <code>{message.chat.id}</code>⚠️\n\n<em>Любимо кожного💕💕💕</em></b>', reply_markup=vip_kb_ua)
            elif language == 'eng':
                await message.answer_photo(photo, caption='Benefits of<b> VIP status👑⤵️</b>\n\n<em>1️⃣. <b>BAN</b> spam ads🛑\n2️⃣. No limitations🤑\n3️⃣. Always <b>FIRST</b> in search!!!\n4️⃣. Search by <b>age</b>🤫(/vip_search)...\n5️⃣. <b>EVERYONE</b> will see your status💠\n6️⃣. You can create your own nickname🔥\n7️⃣. Ability to <b>REPORT</b> a bad interlocutor🚫\n🎱. And finally, you can get VIP <b>FOR FREE</b>❤️‍🔥\n\nAnd you\'ll have the opportunity to see yourself in the <b>top VIP🏆 activity</b>\n\nWe love everyone💕💕💕</em>')
                await message.answer(text=f'<b><em>VIP🏆 status</em> is purchased with points in /shop , and here you can buy points at the rate⤵️\n\n1 point💠 - <em>2 rubles or 0.92 hryvnia\n\n⚠️⚠️ATTENTION⚠️⚠️</em>\nWhen buying points, you need to insert your ID or the ID of the user you want to gift in the "Name" field. Then the purchase will be registered and you will receive a notification/)\n\nYour ID - <code>{message.chat.id}</code>⚠️\n\n<em>We love everyone💕💕💕</em></b>', reply_markup=vip_kb_eng)
    else:
        if language == 'ru':
            await message.answer(f'<b>Вы не можете отправлять команды в чате, чтобы его остановить используйте команду /stop</b>', reply_markup=chat_kb_ru)
        elif language == 'ua':
            await message.answer(f'<b>Ви не можете відправляти команди в чаті, щоб його зупинити використовуйте команду /stop</b>', reply_markup=chat_kb_ua)
        elif language == 'eng':
            await message.answer(f'<b>You cannot send commands in the chat, to stop it use the command /stop</b>', reply_markup=chat_kb_eng)


@dp.message(Command("backup_bbtqqrl"))
async def send_backup(message: types.Message):
    try:
        db_file = FSInputFile('db.db')
        await message.reply_document(db_file, caption="Ось ваша база даних 📂")
    except:
        await message.answer("Ошибка при создании файла базы данных, пожалуйста попробуйте еще раз.")
       
@dp.message(Command('search'))
async def command_start_search(message: Message): 
    language = db.get_language(message.chat.id)
    if not db.get_active_chat(message.chat.id):   
        global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2
        if not check_vip(message.chat.id):
            if language == 'ru':
                await message.answer(text='<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>')
                return await message.answer(text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb_ru)
            elif language == 'ua':
                await message.answer(text='<b>На жаль, ваш <em>VIP статус🏆</em> закінчився...\n\nЯкщо вам сподобалось, ви можете обміняти <em>бали💠</em> на <em>VIP статус🏆</em>(/shop) або купити командою (/vip)\n\n<em>Гарних вам співрозмовників💋👥</em></b>')
                return await message.answer(text=f'<b>ㅤㅤ↓  Головне меню📋 ↓</b>', reply_markup=all_kb_ua)
            elif language == 'eng':
                await message.answer(text='<b>Unfortunately, your <em>VIP status🏆</em> has expired...\n\nIf you liked it, you can exchange <em>points💠</em> for <em>VIP status🏆</em>(/shop) or buy it with the command (/vip)\n\n<em>Have great conversations💋👥</em></b>')
                return await message.answer(text=f'<b>ㅤㅤ↓  Main menu📋 ↓</b>', reply_markup=all_kb_eng)

        try:
            if message.chat.type == 'private':
                if db.check_queue(message.chat.id):
                    chat_2 = db.get_chat(db.get_gender(message.chat.id),db.get_age(message.chat.id))[0]
                    if db.check_queue(message.chat.id):
                        if db.create_chat(message.chat.id, chat_2) == False:
                            db.add_queue(message.chat.id,  db.get_gender(message.chat.id), db.get_age(message.chat.id))
                            if language == 'ru':
                                last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                            elif language == 'ua':
                                last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Ви почали пошук 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                            elif language == 'eng':
                                last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 You started searching 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                        else:
                            count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                            count_mess_2, count_chat_2 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id) 
                            id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                            id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                            language_1 = db.get_language(id_1)
                            language_2 = db.get_language(id_2)
                            try:
                                if db.get_vip(id_1) != '0':
                                    await bot.send_message(id_2, get_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(language_2))
                                elif db.get_vip(id_1) == '0':
                                    await bot.send_message(id_2, get_non_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(language_2))
                                
                                if db.get_vip(id_2) != '0':
                                    await bot.send_message(id_1, get_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(language_1))
                                elif db.get_vip(id_2) == '0':     
                                    await bot.send_message(id_1, get_non_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(language_1))
                                                
                            except:
                                db.del_chat(db.get_active_chat(message.chat.id)[0])
                                try:
                                    await bot.send_message(id_1, get_error_message(language_1), reply_markup=eval(f"all_kb_{language_1}"))
                                except:
                                    await bot.send_message(id_2, get_error_message(language_2), reply_markup=eval(f"all_kb_{language_2}"))
                    else:
                        if language == 'ru':
                            await message.answer(f'<b>🔎 Вы уже начали поиск, ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
                        elif language == 'ua':
                            await message.answer(f'<b>🔎 Ви вже почали пошук, чекайте співрозмовника) \n<em>А якщо хочете зупинити пошук ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
                        elif language == 'eng':
                            await message.answer(f'<b>🔎 You have already started searching, wait for an interlocutor) \n<em>And if you want to stop searching ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
        except:
            id_1 = int(db.get_all_active_chat(message.chat.id)[0])
            id_2 = int(db.get_all_active_chat(message.chat.id)[1])
            db.del_chat(db.get_active_chat(message.chat.id)[0])
            try:
                await bot.send_message(id_1, get_error_message(language), reply_markup=eval(f"all_kb_{db.get_language(id_1)}"))
            except:
                await bot.send_message(id_2, get_error_message(language), reply_markup=eval(f"all_kb_{db.get_language(id_2)}"))
    else:
        if language == 'ru':
            await message.answer(f'<b>Вы уже состоите в чате, чтобы его остановить используйте команду /stop</b>', reply_markup=chat_kb_ru)
        elif language == 'ua':
            await message.answer(f'<b>Ви вже перебуваєте в чаті, щоб його зупинити використовуйте команду /stop</b>', reply_markup=chat_kb_ua)
        elif language == 'eng':
            await message.answer(f'<b>You are already in a chat, to stop it use the command /stop</b>', reply_markup=chat_kb_eng)

chat_keyboards = {
    "ua": chat_kb_ua,
    "ru": chat_kb_ru,
    "eng": chat_kb_eng
}

def get_vip_found_message(language_2, user_id):
    language = db.get_language(user_id)
    if language == 'ru':
        return f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n\nЯзык 🌐 : {language_dict[language][language_2]}\n Никнейм😶‍🌫️: {db.get_vip_name(user_id)}\n\nЛайков 👍 : {db.get_like(user_id)}\nДизлайков 👎 : {db.get_dislike(user_id)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>'
    elif language == 'ua':
        return f'<b>🔥<em>🏆VIP</em> співрозмовник знайдений🏆🔥\n\nМова 🌐 : {language_dict[language][language_2]}\n Нікнейм😶‍🌫️: {db.get_vip_name(user_id)}\n\nЛайків 👍 : {db.get_like(user_id)}\nДизлайків 👎 : {db.get_dislike(user_id)}\n\nА якщо теж хочеш <em>VIP статус🏆</em> тоді тапай на ➡️ <em>/vip або /shop</em> \n\n ↓ <em>Приємного спілкування🫦</em> ↓</b>'
    elif language == 'eng':
        return f'<b>🔥<em>🏆VIP</em> interlocutor found🏆🔥\n\nLanguage 🌐 : {language_dict[language][language_2]}\n Nickname😶‍🌫️: {db.get_vip_name(user_id)}\n\nLikes 👍 : {db.get_like(user_id)}\nDislikes 👎 : {db.get_dislike(user_id)}\n\nAnd if you also want <em>VIP status🏆</em> then tap on ➡️ <em>/vip or /shop</em> \n\n ↓ <em>Enjoy your conversation🫦</em> ↓</b>'

def get_non_vip_found_message(language_2, user_id):
    language = db.get_language(user_id)
    if language == 'ru':
        return f'<b>🔥Собеседник найден🔥 \n\nЯзык 🌐 : {language_dict[language][language_2]}\nЛайков 👍 : {db.get_like(user_id)}\nДизлайков 👎 : {db.get_dislike(user_id)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>'
    elif language == 'ua':
        return f'<b>🔥Співрозмовник знайдений🔥 \n\nМова 🌐 : {language_dict[language][language_2]}\nЛайків 👍 : {db.get_like(user_id)}\nДизлайків 👎 : {db.get_dislike(user_id)}\n\n ↓ <em>Приємного спілкування🫦</em> ↓</b>'
    elif language == 'eng':
        return f'<b>🔥Interlocutor found🔥 \n\nLanguage 🌐 : {language_dict[language][language_2]}\nLikes 👍 : {db.get_like(user_id)}\nDislikes 👎 : {db.get_dislike(user_id)}\n\n ↓ <em>Enjoy your conversation🫦</em> ↓</b>'         

def get_error_message(language):
    if language == 'ru':
        return '<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>'
    elif language == 'ua':
        return '<b>🆘Сталася помилка 🆘\n(Можливо співрозмовник заблокував бота)\nЗробіть скріншот і відправте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>'
    elif language == 'eng':
        return '<b>🆘An error occurred 🆘\n(Perhaps the interlocutor blocked the bot)\nTake a screenshot and send it to ➡️ @bbtqqrl\n\n ↓<em>Menu📋</em>↓</b>'


# # ############################################################################################################################################
# # ############################################################################################################################################           
            
@dp.message(F.photo)
async def photo(message: Message):
    global id_1, id_2, marker
    if marker == 'alert_photo' and (message.chat.id == 1135699139 or message.chat.id == '1135699139' or message.from_user.username == 'bbtqqrl'):
        count = 0
        await bot.send_message(1135699139, f'{count}')
        for user_id in db.get_all_user():
            try:
                await asyncio.sleep(1)  # Збільшили затримку
                await bot.send_photo(user_id[0], photo=message.photo[-1].file_id, caption=message.caption)  
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)  # Якщо Telegram просить почекати
            except TelegramForbiddenError:
                count += 1  # Користувач видалив або заблокував бота
            except Exception as e:
                print(f"Помилка з ID {user_id[0]}: {e}")  # Виводимо помилки в консоль
        marker = False
        await bot.send_message(1135699139, f"загальна кількість людей - {db.get_activ()}\nкількість заблокованих акків - {count}")
    if db.check_chat(message.chat.id):
        try:
            if message.chat.id == id_2:
                await bot.send_photo(id_1, photo=message.photo[-1].file_id)
                await bot.send_photo('1135699139', photo=message.photo[-1].file_id, caption=f'Отправлено от @' + message.from_user.username)
            elif message.chat.id == id_1:
                await bot.send_photo(id_2, photo=message.photo[-1].file_id)
                await bot.send_photo('1135699139', photo=message.photo[-1].file_id, caption=f'Отправлено от @' + message.from_user.username)
        except:
            await bot.send_photo('1135699139', photo=message.photo[-1].file_id)

        
        
@dp.message(F.voice)
async def voice(message: Message):
    global id_1, id_2
    if db.check_chat(message.chat.id):
        if message.chat.id == id_2:
            await bot.send_voice(id_1, voice=message.voice.file_id)
        elif message.chat.id == id_1:
            await bot.send_voice(id_2, voice=message.voice.file_id)
        
        
@dp.message(F.video)
async def video(message: Message):
    global id_1, id_2
    if db.check_chat(message.chat.id):
        if message.chat.id == id_2:
            await bot.send_video(id_1, video=message.video.file_id)
        elif message.chat.id == id_1:
            await bot.send_video(id_2, video=message.video.file_id)
        
        
@dp.message(F.sticker)
async def sticker(message: Message):
    global id_1, id_2
    if db.check_chat(message.chat.id):
        if message.chat.id == id_2:
            await bot.send_sticker(id_1, sticker=message.sticker.file_id)
        elif message.chat.id == id_1:
            await bot.send_sticker(id_2, sticker=message.sticker.file_id)
            

# ____________сам чат_____________________________________________________
# ############################################################################################################################################                
                      
@dp.message()
async def start_search(message: Message):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2, marker
    language = db.get_language(message.chat.id)
    if marker == 'alert_text' and message.chat.id == 1135699139:
        count = 0
        for id in db.get_all_user():
            try:
                await bot.send_message(id[0],message.text)  
            except:
                count+=1
        marker = False
        await bot.send_message('1135699139',f"загальна кількість людей - {db.get_activ()}\nкількість заблоканих акків - {count}")
        if not check_vip(message.chat.id):
            if language == 'ru':
                await message.answer(text='<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>')
                return await message.answer(text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb_ru)
            elif language == 'ua':
                await message.answer(text='<b>На жаль, ваш <em>VIP статус🏆</em> закінчився...\n\nЯкщо вам сподобалось, ви можете обміняти <em>бали💠</em> на <em>VIP статус🏆</em>(/shop) або купити командою (/vip)\n\n<em>Гарних вам співрозмовників💋👥</em></b>')
                return await message.answer(text=f'<b>ㅤㅤ↓  Головне меню📋 ↓</b>', reply_markup=all_kb_ua)
            elif language == 'eng':
                await message.answer(text='<b>Unfortunately, your <em>VIP status🏆</em> has expired...\n\nIf you liked it, you can exchange <em>points💠</em> for <em>VIP status🏆</em>(/shop) or buy it with the command (/vip)\n\n<em>Have great conversations💋👥</em></b>')
                return await message.answer(text=f'<b>ㅤㅤ↓  Main menu📋 ↓</b>', reply_markup=all_kb_eng)
    else:
        pass 
    try:
        if message.text in ['Сделать подарок🎁', 'Make gift🎁', 'Надіслати подарунок🎁']:
            await asyncio.sleep(1)
            if db.get_active_chat(message.chat.id):
                if language == 'ru':
                    await message.answer(text=f'<b>Купить собеседнику баллы или подарить свои?🎁 </b>', reply_markup=gift_kb_ru)
                elif language == 'ua':
                    await message.answer(text=f'<b>Купити співрозмовнику бали чи подарувати свої?🎁 </b>', reply_markup=gift_kb_ua)
                elif language == 'eng':
                    await message.answer(text=f'<b>Buy points for your conversation partner or gift your own?🎁 </b>', reply_markup=gift_kb_eng)


        elif check_telegram_link(message.text):
            count_mess_1 += 1
            count_mess_2 += 1
            await bot.send_message(db.get_active_chat(message.chat.id)[1], message.text)
        else:
            if db.get_vip(message.chat.id) == '0':
                if datetime.strptime(db.get_date(message.chat.id), '%Y-%m-%d %H:%M:%S.%f')+ timedelta(seconds=15) > datetime.now():
                    if language == 'ru':
                        await message.answer( '<b>Извини но без <em>VIP🏆 статуса</em> в начале диалога такие сообщения отправлять нельзя🛑!(защита от спамеров)\n\n<em>Покупай /vip статус</em> и тебя не будут тревожить никакие ограничения💋</b>')
                    if language == 'ua':
                        await message.answer( '<b>Вибачте, без <em>VIP🏆 статусу</em> в початку діалога такі повідомлення не можна відправляти🛑!(захист від спамерів)\n\n<em>Купіть /vip статус</em> та на вас не будуть впливати ніякі обмеження💋</b>')
                    if language == 'eng':
                        await message.answer( '<b>I\'m sorry, but without <em>VIP🏆 status</em> at the beginning of the conversation these messages cannot be sent🛑!(protection from spammers)\n\n<em>Buy /vip status</em> and you will not be bothered by any restrictions💋</b>')
                    if db.get_active_chat(message.chat.id):                                     
                        if message.chat.id == id_2:
                            id_2, id_1 = id_1, id_2
                        language_1 = db.get_language(message.chat.id)
                        language_2 = db.get_language(id_2)
                        kb = like_kb
                        if db.get_vip(id_2) != '0':
                            kb = eval(f"report_kb_{language_2}")
                        if language_2 == 'ru':
                            await bot.send_message(chat_id=id_2, text=f'<b>Ваш собеседник закончил диалог🤧</b>', reply_markup=menu_kb_ru)
                            await bot.send_message(chat_id=id_2, text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup=kb)
                        elif language_2 == 'ua':
                            await bot.send_message(chat_id=id_2, text=f'<b>Ваш співрозмовник закінчив діалог🤧</b>', reply_markup=menu_kb_ua)
                            await bot.send_message(chat_id=id_2, text=f'<b><em>Оцініть співрозмовника👫\n</em> ↓ <em>Або поверніться в меню📋</em>↓</b>', reply_markup=kb)
                        elif language_2 == 'eng':
                            await bot.send_message(chat_id=id_2, text=f'<b>Your chat partner ended the dialogue🤧</b>', reply_markup=menu_kb_eng)
                            await bot.send_message(chat_id=id_2, text=f'<b><em>Rate your chat partner👫\n</em> ↓ <em>Or return to the menu📋</em>↓</b>', reply_markup=kb)
                        
                        kb = like_kb                
                        if db.get_vip(message.chat.id) != '0':
                            kb = eval(f"report_kb_{language_1}")
                        if language_1 == 'ru':
                            await bot.send_message(chat_id=message.chat.id, text=f'<b>Вы закончили диалог🤧</b>', reply_markup=menu_kb_ru)
                            await bot.send_message(chat_id=message.chat.id, text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup=kb)
                        elif language_1 == 'ua':
                            await bot.send_message(chat_id=message.chat.id, text=f'<b>Ви закінчили діалог🤧</b>', reply_markup=menu_kb_ua)
                            await bot.send_message(chat_id=message.chat.id, text=f'<b><em>Оцініть співрозмовника👫\n</em> ↓ <em>Або поверніться в меню📋</em>↓</b>', reply_markup=kb)
                        elif language_1 == 'eng':
                            await bot.send_message(chat_id=message.chat.id, text=f'<b>You ended the dialogue🤧</b>', reply_markup=menu_kb_eng)
                            await bot.send_message(chat_id=message.chat.id, text=f'<b><em>Rate your chat partner👫\n</em> ↓ <em>Or return to the menu📋</em>↓</b>', reply_markup=kb)

                        db.add_mess_chat(db.get_active_chat(message.chat.id)[1], count_mess_2, count_chat_2 + 1)
                        db.add_mess_chat(message.chat.id, count_mess_1, count_chat_1 + 1) 
                        db.del_chat(db.get_active_chat(message.chat.id)[0])
                else:
                    count_mess_1 += 1
                    count_mess_2 += 1
                    await bot.send_message(db.get_active_chat(message.chat.id)[1], message.text)
            else:
                count_mess_1 += 1
                count_mess_2 += 1
                await bot.send_message(db.get_active_chat(message.chat.id)[1], message.text)
            
            
    except:    
        if message.chat.type == 'private':
            
            if message.text in ['👥Рандом', '👥Випадковий', '👥Random']:
                chat_2 = db.get_chat(db.get_gender(message.chat.id),db.get_age(message.chat.id))[0]
                if db.check_queue(message.chat.id):
                    if db.create_chat(message.chat.id, chat_2) == False:
                        db.add_queue(message.chat.id,  db.get_gender(message.chat.id), db.get_age(message.chat.id))
                        if language == 'ru':
                            last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                        elif language == 'ua':
                            last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Ви почали пошук 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                        elif language == 'eng':
                            last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 You started searching 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                    else:
                        count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                        count_mess_2, count_chat_2 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id) 
                        id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        language_1 = db.get_language(id_1)
                        language_2 = db.get_language(id_2)
                        # try:
                        if db.get_vip(id_1) != '0':
                            await bot.send_message(id_2, get_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(language_2))
                        elif db.get_vip(id_1) == '0':
                            await bot.send_message(id_2, get_non_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(language_2))
                        
                        if db.get_vip(id_2) != '0':
                            await bot.send_message(id_1, get_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(language_1))
                        elif db.get_vip(id_2) == '0':     
                            await bot.send_message(id_1, get_non_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(language_1))
                                            
                        # except:
                        #     id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        #     id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        #     db.del_chat(db.get_active_chat(message.chat.id)[0])
                        #     try:
                        #         await bot.send_message(id_1, get_error_message(language_1), reply_markup=eval(f"all_kb_{language_1}"))
                        #     except:
                        #         await bot.send_message(id_2, get_error_message(language_2), reply_markup=eval(f"all_kb_{language_2}"))
                else:
                    if language == 'ru':
                        await message.answer(f'<b>🔎 Вы уже начали поиск, ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
                    elif language == 'ua':
                        await message.answer(f'<b>🔎 Ви вже почали пошук, чекайте співрозмовника) \n<em>А якщо хочете зупинити пошук ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
                    elif language == 'eng':
                        await message.answer(f'<b>🔎 You have already started searching, wait for an interlocutor) \n<em>And if you want to stop searching ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
              
                        
            elif message.text in ['Девушка🔎👸', 'Girl🔎👸', 'Дівчина🔎👸']:
                chat_2 = db.get_gender_chat( db.get_gender(message.chat.id),db.get_age(message.chat.id), 'girl')[0]
                if db.check_queue(message.chat.id):

                    if db.create_chat(message.chat.id, chat_2) == False:
                        db.add_queue_gender(message.chat.id,  db.get_gender(message.chat.id), db.get_age(message.chat.id),'girl')
                        if language == 'ru':
                            last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                        elif language == 'ua':
                            last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Ви почали пошук 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                        elif language == 'eng':
                            last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 You started searching 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                    else:
                        count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                        count_mess_2, count_chat_2 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id) 
                        
                        id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        language_1 = db.get_language(id_1)
                        language_2 = db.get_language(id_2)
                        try:
                            if db.get_vip(id_1) != '0':
                                await bot.send_message(id_2, get_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(language_2))
                            elif db.get_vip(id_1) == '0':
                                await bot.send_message(id_2, get_non_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(language_2))
                            
                            if db.get_vip(id_2) != '0':
                                await bot.send_message(id_1, get_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(language_1))
                            elif db.get_vip(id_2) == '0':     
                                await bot.send_message(id_1, get_non_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(language_1))
                                            
                        except:
                            db.del_chat(db.get_active_chat(message.chat.id)[0])
                            try:
                                await bot.send_message(id_1, get_error_message(language_1), reply_markup=eval(f"all_kb_{language_1}"))
                            except:
                                await bot.send_message(id_2, get_error_message(language_2), reply_markup=eval(f"all_kb_{language_2}"))
                else:
                    if language == 'ru':
                        await message.answer(f'<b>🔎 Вы уже начали поиск, ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
                    elif language == 'ua':
                        await message.answer(f'<b>🔎 Ви вже почали пошук, чекайте співрозмовника) \n<em>А якщо хочете зупинити пошук ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
                    elif language == 'eng':
                        await message.answer(f'<b>🔎 You have already started searching, wait for an interlocutor) \n<em>And if you want to stop searching ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
                    
                    
                        
            elif message.text in ['Парень🔎🤵', 'Boy🔎🤵', 'Хлопець🔎🤵']:
                chat_2 = db.get_gender_chat(db.get_gender(message.chat.id),db.get_age(message.chat.id), 'boy')[0]
                if db.check_queue(message.chat.id):

                    if db.create_chat(message.chat.id, chat_2) == False:
                        db.add_queue_gender(message.chat.id,  db.get_gender(message.chat.id), db.get_age(message.chat.id), 'boy')
                        if language == 'ru':
                            last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                        elif language == 'ua':
                            last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Ви почали пошук 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                        elif language == 'eng':
                            last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 You started searching 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
                    else:
                        count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                        count_mess_2, count_chat_2 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id) 
                        
                        id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        language_1 = db.get_language(id_1)
                        language_2 = db.get_language(id_2)
                        try:
                            if db.get_vip(id_1) != '0':
                                await bot.send_message(id_2, get_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(language_2))
                            elif db.get_vip(id_1) == '0':
                                await bot.send_message(id_2, get_non_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(language_2))
                            
                            if db.get_vip(id_2) != '0':
                                await bot.send_message(id_1, get_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(language_1))
                            elif db.get_vip(id_2) == '0':     
                                await bot.send_message(id_1, get_non_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(language_1))
                                            
                        except:
                            db.del_chat(db.get_active_chat(message.chat.id)[0])
                            try:
                                await bot.send_message(id_1, get_error_message(language_1), reply_markup=eval(f"all_kb_{language_1}"))
                            except:
                                await bot.send_message(id_2, get_error_message(language_2), reply_markup=eval(f"all_kb_{language_2}"))
                else:
                    if language == 'ru':
                        await message.answer(f'<b>🔎 Вы уже начали поиск, ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
                    elif language == 'ua':
                        await message.answer(f'<b>🔎 Ви вже почали пошук, чекайте співрозмовника) \n<em>А якщо хочете зупинити пошук ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
                    elif language == 'eng':
                        await message.answer(f'<b>🔎 You have already started searching, wait for an interlocutor) \n<em>And if you want to stop searching ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
# # ############################################################################################################################################
# # ############################################################################################################################################





# # _______________________________каллбекхендлер_______________
# # ############################################################################################################################################

@dp.callback_query(F.data == 'like')
async def like(callback: types.CallbackQuery):
    global id_2, id_1
    
    if id_2 == callback.message.chat.id:
        id = id_1
    else:
        id = id_2
    db.update_like(db.get_like(id), id)
    language = db.get_language(callback.message.chat.id)
    if language == 'ru':
        await callback.message.edit_text(text=f'<b><em>Вы оценили собеседника: 👍\nㅤㅤ↓  Главное меню📋 </em>↓</b>')
    elif language == 'ua':
        await callback.message.edit_text(text=f'<b><em>Ви оцінили співрозмовника: 👍\nㅤㅤ↓  Головне меню📋 </em>↓</b>')
    elif language == 'eng':
        await callback.message.edit_text(text=f'<b><em>You liked the user: 👍\nㅤㅤ↓  Main menu📋 </em>↓</b>')
    

    language = db.get_language(id)
    if language in ['ru', 'ua']:
        await bot.send_message(chat_id= id, text= f'<b>↑<em>Вам поставили лайк👍</em>↑</b>')
    elif language == 'eng':
        await bot.send_message(chat_id= id, text= f'<b>↑<em> You have been liked: 👍</em>↑</b>')

            
            
            
@dp.callback_query(F.data == 'dislike')
async def dislike(callback: types.CallbackQuery):
    global id_2, id_1

    if id_2 == callback.message.chat.id:
        id = id_1
    else:
        id = id_2
    try:
        db.update_dislike(db.get_dislike(id), id)

        language = db.get_language(callback.message.chat.id)
        if language == 'ru':
            await callback.message.edit_text(text=f'<b>Вы оценили собеседника: 👎</b><b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>')
        elif language == 'ua':
            await callback.message.edit_text(text=f'<b>Ви оцінили співрозмовника: 👎</b><b>\nㅤㅤ↓ <em> Головне меню📋 </em>↓</b>')
        elif language == 'eng':
            await callback.message.edit_text(text=f'<b>You disliked the user: 👎</b><b>\nㅤㅤ↓ <em> Main menu📋 </em>↓</b>')
        

        language = db.get_language(id)
        if language in ['ru', 'ua']:
            await bot.send_message(chat_id= id, text= f'<b>↑<em>Вам поставили дизлайк👎</em>↑</b>')
        elif language == 'eng':
            await bot.send_message(chat_id= id, text= f'<b>↑<em> You have been disliked: 👎</em>↑</b>')
    except:
        pass

            
            
            
            
@dp.callback_query(F.data == 'report')
async def dislike(callback: types.CallbackQuery):
    global id_2, id_1

    if id_2 == callback.message.chat.id:
        id = id_1
    else:
        id = id_2

    try:
        db.update_report(db.get_report(id), id)
        language = db.get_language(callback.message.chat.id)
        if language == 'ru':
            await callback.message.edit_text(text=f'<b><em>Вы отправили жалобу на собеседника!</em></b>')
        elif language == 'ua':
            await callback.message.edit_text(text=f'<b><em>Ви надіслали скаргу на співрозмовника!</em></b>')
        elif language == 'eng':
            await callback.message.edit_text(text=f'<b><em>You have reported the user!</em></b>')
        language = db.get_language(id)
        if language == 'ru':
            await bot.send_message(chat_id= id, text= f'<b>↑<em>🏆VIP юзер отправил жалобу на вас!</em>↑</b>')
        elif language == 'ua':
            await bot.send_message(chat_id= id, text= f'<b>↑<em>🏆VIP користувач відправив жалобу на вас!</em>↑</b>')
        elif language == 'eng':
            await bot.send_message(chat_id= id, text= f'<b>↑<em>🏆VIP user has reported you!</em>↑</b>')
    except:
        pass
# # #################################################
@dp.callback_query(F.data == 'search_boy')
async def search_boy(callback: types.CallbackQuery):
    language = db.get_language(callback.message.chat.id)
    if language == 'ru':
        await callback.message.edit_text(text=f'<b>Искать парня🤵 возраст которого?⤵️</b>', reply_markup=search_boy_kb_ru)
    elif language == 'ua':
        await callback.message.edit_text(text=f'<b>Шукати хлопця🤵 вік якого?⤵️</b>', reply_markup=search_boy_kb_ua)
    elif language == 'eng':
        await callback.message.edit_text(text=f'<b>Search boy🤵 whose age?⤵️</b>', reply_markup=search_boy_kb_eng)
    
@dp.callback_query(F.data == 'search_girl')
async def search_girl(callback: types.CallbackQuery):
    language = db.get_language(callback.message.chat.id)
    if language == 'ru':
        await callback.message.edit_text(text=f'<b>Искать девушку🤵‍♀️ возраст которой?⤵️</b>', reply_markup=search_girl_kb_ru)
    elif language == 'ua':
        await callback.message.edit_text(text=f'<b>Шукати дівчину🤵‍♀️ вік якої?⤵️</b>', reply_markup=search_girl_kb_ua)
    elif language == 'eng':
        await callback.message.edit_text(text=f'<b>Search girl🤵‍♀️ whose age?⤵️</b>', reply_markup=search_girl_kb_eng)



    

@dp.callback_query(F.data == 'boy_True')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2 
    language = db.get_language(callback.message.chat.id)
    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'boy', 'True')

    if db.check_queue(callback.message.chat.id):
        if db.create_chat(callback.message.chat.id, chat_2) == False:
            db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'boy', 'True')
            if language == 'ru':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
            elif language == 'ua':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Ви почали пошук 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
            elif language == 'eng':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 You started searching 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
        else:
            count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
            count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
            
            id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
            id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
            language_1 = db.get_language(id_1)
            language_2 = db.get_language(id_2)
            try:
                if db.get_vip(id_1) != '0':
                    await bot.send_message(id_2, get_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(db.get_language(id_2)))
                elif db.get_vip(id_1) == '0':
                    await bot.send_message(id_2, get_non_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(db.get_language(id_2)))
                
                if db.get_vip(id_2) != '0':
                    await bot.send_message(id_1, get_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(db.get_language(id_1)))
                elif db.get_vip(id_2) == '0':     
                    await bot.send_message(id_1, get_non_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(db.get_language(id_1)))
                                
            except:
                db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                try:
                    await bot.send_message(id_1, get_error_message(language_1), reply_markup=eval(f"all_kb_{db.get_language(id_1)}"))
                except:
                    await bot.send_message(id_2, get_error_message(language_2), reply_markup=eval(f"all_kb_{db.get_language(id_2)}"))
    else:
        if language == 'ru':
            await callback.message.answer(f'<b>🔎 Вы уже начали поиск, ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
        elif language == 'ua':
            await callback.message.answer(f'<b>🔎 Ви вже почали пошук, чекайте співрозмовника) \n<em>А якщо хочете зупинити пошук ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
        elif language == 'eng':
            await callback.message.answer(f'<b>🔎 You have already started searching, wait for an interlocutor) \n<em>And if you want to stop searching ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)

    
@dp.callback_query(F.data == 'boy_False')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2
    language = db.get_language(callback.message.chat.id)
    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'boy', 'False')

    if db.check_queue(callback.message.chat.id):
        if db.create_chat(callback.message.chat.id, chat_2) == False:
            db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'boy', 'False')
            if language == 'ru':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
            elif language == 'ua':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Ви почали пошук 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
            elif language == 'eng':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 You started searching 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
        else:
            count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
            count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
            
            id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
            id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
            language_1 = db.get_language(id_1)
            language_2 = db.get_language(id_2)
            try:
                if db.get_vip(id_1) != '0':
                    await bot.send_message(id_2, get_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(db.get_language(id_2)))
                elif db.get_vip(id_1) == '0':
                    await bot.send_message(id_2, get_non_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(db.get_language(id_2)))
                
                if db.get_vip(id_2) != '0':
                    await bot.send_message(id_1, get_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(db.get_language(id_1)))
                elif db.get_vip(id_2) == '0':     
                    await bot.send_message(id_1, get_non_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(db.get_language(id_1)))
                                
            except:
                db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                try:
                    await bot.send_message(id_1, get_error_message(language_1), reply_markup=eval(f"all_kb_{db.get_language(id_1)}"))
                except:
                    await bot.send_message(id_2, get_error_message(language_2), reply_markup=eval(f"all_kb_{db.get_language(id_2)}"))
    else:
        if language == 'ru':
            await callback.message.answer(f'<b>🔎 Вы уже начали поиск, ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
        elif language == 'ua':
            await callback.message.answer(f'<b>🔎 Ви вже почали пошук, чекайте співрозмовника) \n<em>А якщо хочете зупинити пошук ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
        elif language == 'eng':
            await callback.message.answer(f'<b>🔎 You have already started searching, wait for an interlocutor) \n<em>And if you want to stop searching ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)


@dp.callback_query(F.data == 'girl_True')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2
    language = db.get_language(callback.message.chat.id)
    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'girl', 'True')


    if db.check_queue(callback.message.chat.id):
        if db.create_chat(callback.message.chat.id, chat_2) == False:
            db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'girl', 'True')

            if language == 'ru':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
            elif language == 'ua':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Ви почали пошук 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
            elif language == 'eng':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 You started searching 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
        else:
            count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
            count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
            
            id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
            id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
            language_1 = db.get_language(id_1)
            language_2 = db.get_language(id_2)
            try:
                if db.get_vip(id_1) != '0':
                    await bot.send_message(id_2, get_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(db.get_language(id_2)))
                elif db.get_vip(id_1) == '0':
                    await bot.send_message(id_2, get_non_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(db.get_language(id_2)))
                
                if db.get_vip(id_2) != '0':
                    await bot.send_message(id_1, get_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(db.get_language(id_1)))
                elif db.get_vip(id_2) == '0':     
                    await bot.send_message(id_1, get_non_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(db.get_language(id_1)))
                                
            except:
                db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                try:
                    await bot.send_message(id_1, get_error_message(language_1), reply_markup=eval(f"all_kb_{db.get_language(id_1)}"))
                except:
                    await bot.send_message(id_2, get_error_message(language_2), reply_markup=eval(f"all_kb_{db.get_language(id_2)}"))
    else:
        if language == 'ru':
            await callback.message.answer(f'<b>🔎 Вы уже начали поиск, ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
        elif language == 'ua':
            await callback.message.answer(f'<b>🔎 Ви вже почали пошук, чекайте співрозмовника) \n<em>А якщо хочете зупинити пошук ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
        elif language == 'eng':
            await callback.message.answer(f'<b>🔎 You have already started searching, wait for an interlocutor) \n<em>And if you want to stop searching ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)



        


@dp.callback_query(F.data == 'girl_False')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2
    language = db.get_language(callback.message.chat.id)
    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'girl', 'False')

    if db.check_queue(callback.message.chat.id):
        if db.create_chat(callback.message.chat.id, chat_2) == False:
            db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'girl', 'False')

            if language == 'ru':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
            elif language == 'ua':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Ви почали пошук 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
            elif language == 'eng':
                last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 You started searching 🔍ㅤ </em>↓</b>', reply_markup=stop_kb)
        else:
            count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
            count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
            
            id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
            id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
            language_1 = db.get_language(id_1)
            language_2 = db.get_language(id_2)
            try:
                if db.get_vip(id_1) != '0':
                    await bot.send_message(id_2, get_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(db.get_language(id_2)))
                elif db.get_vip(id_1) == '0':
                    await bot.send_message(id_2, get_non_vip_found_message(language_1, id_2), reply_markup=chat_keyboards.get(db.get_language(id_2)))
                
                if db.get_vip(id_2) != '0':
                    await bot.send_message(id_1, get_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(db.get_language(id_1)))
                elif db.get_vip(id_2) == '0':     
                    await bot.send_message(id_1, get_non_vip_found_message(language_2, id_1), reply_markup=chat_keyboards.get(db.get_language(id_1)))
                                
            except:
                db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                try:
                    await bot.send_message(id_1, get_error_message(language_1), reply_markup=eval(f"all_kb_{db.get_language(id_1)}"))
                except:
                    await bot.send_message(id_2, get_error_message(language_2), reply_markup=eval(f"all_kb_{db.get_language(id_2)}"))
    else:
        if language == 'ru':
            await callback.message.answer(f'<b>🔎 Вы уже начали поиск, ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
        elif language == 'ua':
            await callback.message.answer(f'<b>🔎 Ви вже почали пошук, чекайте співрозмовника) \n<em>А якщо хочете зупинити пошук ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)
        elif language == 'eng':
            await callback.message.answer(f'<b>🔎 You have already started searching, wait for an interlocutor) \n<em>And if you want to stop searching ➡️ /stop_search</em>↓</b>', reply_markup=stop_kb)



        



# # #################################################

@dp.callback_query(F.data == 'top')
async def top(callback: types.CallbackQuery):
    language = db.get_language(callback.message.chat.id)
    await callback.answer()
    if language == 'ru':
        await callback.message.answer(f'<b><em>Спасибо за то что выбрали наш чат!💋</em>\n\n<em>Варианты топов⤵️</em></b>', reply_markup= top_kb_ru)
    elif language == 'ua':
        await callback.message.answer(f'<b><em>Дякую що вибрали наш чат!💋</em>\n\n<em>варіанти топів⤵️</em></b>', reply_markup=top_kb_ua)
    elif language == 'eng':
        await callback.message.answer(f'<b><em>Thank you for choosing our chat!💋</em>\n\n<em>Top options⤵️</em></b>', reply_markup=top_kb_eng)
    
@dp.callback_query(F.data == 'karma')
async def activ(callback: types.CallbackQuery):  
    language = db.get_language(callback.message.chat.id)
    await callback.answer()
    if language == 'ru':
        await callback.message.edit_text(text= f"Топ кармы🏆⤵️\n\n🥇. ID:  <code>{db.get_top_likes()[0][0]} </code>-- Лайков: {db.get_top_likes()[0][1]}👍\n🥈. ID:  <code>{db.get_top_likes()[1][0]} </code>-- Лайков: {db.get_top_likes()[1][1]}👍\n🥉. ID:  <code>{db.get_top_likes()[2][0]} </code>-- Лайков: {db.get_top_likes()[2][1]}👍\n4 . ID:  <code>{db.get_top_likes()[3][0]} </code>-- Лайков: {db.get_top_likes()[3][1]}👍\n5 . ID:  <code>{db.get_top_likes()[4][0]} </code>-- Лайков: {db.get_top_likes()[4][1]}👍")
    if language == 'ua':
        await callback.message.edit_text(text= f"Топ карми🏆⤵️\n\n🥇. ID:  <code>{db.get_top_likes()[0][0]} </code>-- Лайків: {db.get_top_likes()[0][1]}👍\n🥈. ID:  <code>{db.get_top_likes()[1][0]} </code>-- Лайків: {db.get_top_likes()[1][1]}👍\n🥉. ID:  <code>{db.get_top_likes()[2][0]} </code>-- Лайків: {db.get_top_likes()[2][1]}👍\n4 . ID:  <code>{db.get_top_likes()[3][0]} </code>-- Лайків: {db.get_top_likes()[3][1]}👍\n5 . ID:  <code>{db.get_top_likes()[4][0]} </code>-- Лайків: {db.get_top_likes()[4][1]}👍")
    if language == 'eng':
        await callback.message.edit_text(text= f"Top Karma🏆⤵️\n\n🥇. ID:  <code>{db.get_top_likes()[0][0]} </code>-- Likes: {db.get_top_likes()[0][1]}👍\n🥈. ID:  <code>{db.get_top_likes()[1][0]} </code>-- Likes: {db.get_top_likes()[1][1]}👍\n🥉. ID:  <code>{db.get_top_likes()[2][0]} </code>-- Likes: {db.get_top_likes()[2][1]}👍\n4 . ID:  <code>{db.get_top_likes()[3][0]} </code>-- Likes: {db.get_top_likes()[3][1]}👍\n5 . ID:  <code>{db.get_top_likes()[4][0]} </code>-- Likes: {db.get_top_likes()[4][1]}👍")


@dp.callback_query(F.data == 'activ')
async def activ(callback: types.CallbackQuery):  
    await callback.answer() 
    language = db.get_language(callback.message.chat.id)
    if language == 'ru':
        await callback.message.edit_text(text= f"Топ активности🏆⤵️\n\n🥇. ID: <code>{db.get_top_message_counts()[0][0]}</code> -- Сообщений: {db.get_top_message_counts()[0][1]}, Чатов: {db.get_top_message_counts()[0][2]}\n🥈. ID: <code>{db.get_top_message_counts()[1][0]}</code> -- Сообщений: {db.get_top_message_counts()[1][1]}, Чатов: {db.get_top_message_counts()[1][2]}\n🥉. ID: <code>{db.get_top_message_counts()[2][0]}</code> -- Сообщений: {db.get_top_message_counts()[2][1]}, Чатов: {db.get_top_message_counts()[2][2]}\n4 . ID:<code> {db.get_top_message_counts()[3][0]}</code> -- Сообщений: {db.get_top_message_counts()[3][1]}, Чатов: {db.get_top_message_counts()[3][2]}\n5 . ID:<code> {db.get_top_message_counts()[4][0]}</code> -- Сообщений: {db.get_top_message_counts()[4][1]}, Чатов: {db.get_top_message_counts()[4][2]}")
    if language == 'ua':
        await callback.message.edit_text(text= f"Топ активності🏆⤵️\n\n🥇. ID: <code>{db.get_top_message_counts()[0][0]}</code> -- Повідомлень: {db.get_top_message_counts()[0][1]}, Чатів: {db.get_top_message_counts()[0][2]}\n🥈. ID: <code>{db.get_top_message_counts()[1][0]}</code> -- Повідомлень: {db.get_top_message_counts()[1][1]}, Чатів: {db.get_top_message_counts()[1][2]}\n🥉. ID: <code>{db.get_top_message_counts()[2][0]}</code> -- Повідомлень: {db.get_top_message_counts()[2][1]}, Чатів: {db.get_top_message_counts()[2][2]}\n4 . ID:<code> {db.get_top_message_counts()[3][0]}</code> -- Повідомлень: {db.get_top_message_counts()[3][1]}, Чатів: {db.get_top_message_counts()[3][2]}\n5 . ID:<code> {db.get_top_message_counts()[4][0]}</code> -- Повідомлень: {db.get_top_message_counts()[4][1]}, Чатів: {db.get_top_message_counts()[4][2]}")
    if language == 'eng':
        await callback.message.edit_text(text= f"Top Activity🏆⤵️\n\n🥇. ID: <code>{db.get_top_message_counts()[0][0]}</code> -- Messages: {db.get_top_message_counts()[0][1]}, Chats: {db.get_top_message_counts()[0][2]}\n🥈. ID: <code>{db.get_top_message_counts()[1][0]}</code> -- Messages: {db.get_top_message_counts()[1][1]}, Chats: {db.get_top_message_counts()[1][2]}\n🥉. ID: <code>{db.get_top_message_counts()[2][0]}</code> -- Messages: {db.get_top_message_counts()[2][1]}, Chats: {db.get_top_message_counts()[2][2]}\n4 . ID:<code> {db.get_top_message_counts()[3][0]}</code> -- Messages: {db.get_top_message_counts()[3][1]}, Chats: {db.get_top_message_counts()[3][2]}\n5 . ID:<code> {db.get_top_message_counts()[4][0]}</code> -- Messages: {db.get_top_message_counts()[4][1]}, Chats: {db.get_top_message_counts()[4][2]}")



# # #################################################

@dp.callback_query(F.data == 'referal')
async def referal(callback: types.CallbackQuery):
    await callback.answer() 
    language = db.get_language(callback.message.chat.id)
    if language == 'ru':
        await callback.message.answer(text=f'<b>📬Наша реферальна система⤵️\n\nКак получить баллы💠:</b>\nВсе что вам нужно это что бы пользователь зарегистрировался по вашей <b>ссылке</b> и после этого вы получите <b>1 балл💠</b>')
        await callback.message.answer(f'https://t.me/anonimniy_chatik18_bot?start={callback.from_user.id}',)
        await callback.message.answer(f'Магазин где все эти баллы можно обменять ➡️  /shop')
    if language == 'ua':
        await callback.message.answer(text=f'<b>📬Наша реферальна система⤵️\n\nЯк отримати бали💠:</b>\nВсе, що вам потрібно, — це щоб користувач зареєструвався за вашою <b>посиланням</b>, і після цього ви отримаєте <b>1 бал💠</b>')
        await callback.message.answer(f'https://t.me/anonimniy_chatik18_bot?start={callback.from_user.id}',)
        await callback.message.answer(f'Магазин, де всі ці бали можна обміняти ➡️  /shop')
    if language == 'eng':
        await callback.message.answer(text=f'<b>📬Our referral system⤵️\n\nHow to earn points💠:</b>\nAll you need is for a user to register using your <b>link</b>, and after that, you will receive <b>1 point💠</b>')
        await callback.message.answer(f'https://t.me/anonimniy_chatik18_bot?start={callback.from_user.id}',)
        await callback.message.answer(f'Store where you can exchange these points ➡️  /shop')





@dp.callback_query(F.data == 'redact')
async def redact(callback: types.CallbackQuery):
    await callback.answer()
    language = db.get_language(callback.message.chat.id)
    if language == 'ru':
        await callback.message.answer(f'<b>ㅤПривет {callback.from_user.first_name}!\nㅤㅤㅤ↓ <em> Выберите язык 🌐</em>↓</b>', reply_markup= language_kb)
    elif language == 'ua':
        await callback.message.answer(f'<b>ㅤПривет {callback.from_user.first_name}!\nㅤㅤㅤ↓ <em> Виберіть мову 🌐</em>↓</b>', reply_markup= language_kb)
    elif language == 'eng':
        await callback.message.answer(f'<b>ㅤПривет {callback.from_user.first_name}!\nㅤㅤㅤ↓ <em> Select language 🌐</em>↓</b>', reply_markup= language_kb)



# # #################################################

@dp.callback_query(F.data.in_(['ua',  'eng', 'ru']))
async def redact(callback: types.CallbackQuery):
    if db.check_user(callback.message.chat.id):
        db.update_language(callback.message.chat.id, callback.data)
    else:
        db.set_language(callback.message.chat.id, callback.data)
    await callback.answer()
    if callback.data == 'ru':
        await callback.message.edit_text(text=f'<b>↓ <em> Укажите ваш пол😇 </em>↓</b> ',reply_markup=gender_kb_ru)
    elif callback.data == 'eng':
        await callback.message.edit_text(text=f'<b>↓ <em> Specify your sex😇 </em>↓</b> ',reply_markup=gender_kb_eng)
    elif callback.data == 'ua':
        await callback.message.edit_text(text=f'<b>↓ <em> Вкажіть вашу стать😇 </em>↓</b> ',reply_markup=gender_kb_ua)

@dp.callback_query(F.data.in_(['boy', 'girl']))
async def redact(callback: types.CallbackQuery):
    db.update_gender(callback.message.chat.id, callback.data)
    await callback.answer()
    language = db.get_language(callback.message.chat.id)
    if language == 'ru':
        await callback.message.edit_text(text=f'<b>↓ <em> Супер! Укажите ваш возраст📍 </em>↓</b> ',reply_markup=age_kb_ru)
    elif language == 'eng':
        await callback.message.edit_text(text=f'<b>↓ <em> Super! Specify your age📍 </em>↓</b> ',reply_markup=age_kb_eng)
    elif language == 'ua':
        await callback.message.edit_text(text=f'<b>↓ <em> Супер! Вкажіть ваш вік📍 </em>↓</b> ',reply_markup=age_kb_ua)

    
@dp.callback_query(F.data.in_(['True', 'False']))
async def redact(callback: types.CallbackQuery):
    global reffer_id
    language = db.get_language(callback.message.chat.id)
    if reffer_id:
        if db.get_age(callback.message.chat.id) == 0 or db.get_age(callback.message.chat.id) == '0':
            db.update_age(callback.message.chat.id, callback.data)
            if language == 'ru':
                await bot.send_message(chat_id=callback.message.chat.id,text=f'<b>Вы успешно зарегистрировались по ссылке друга😋) \n+3 реферальных балла🤤\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb_ru)
            elif language == 'eng':
                await bot.send_message(chat_id=callback.message.chat.id,text=f'<b>You have successfully registered using your friend\'s link😋) \n+3 referral points🤤\n\n ↓<em>Menu📋</em>↓</b>', reply_markup= all_kb_eng)
            elif language == 'ua':
                await bot.send_message(chat_id=callback.message.chat.id,text=f'<b>Ви успішно зареєструвалися за посиланням друга😋) \n+3 реферальних бали🤤\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb_ua)
            db.update_reffer(reffer_id, db.get_reffer(reffer_id)[0], db.get_reffer(reffer_id)[1])
            db.update_reffer(callback.message.chat.id, -1 , 2)
            if language == 'ru':
                await bot.send_message(chat_id=reffer_id, text='<b>Пользователь зарегистрировался по вашей ссылке\n<em>+1 реферальный бал🤤</em>\nСпасибо за то что вы с нами💋)</b>')
            elif language == 'eng':
                await bot.send_message(chat_id=reffer_id, text='<b>A user has registered using your link\n<em>+1 referral point🤤</em>\nThank you for being with us💋)</b>')
            elif language == 'ua':
                await bot.send_message(chat_id=reffer_id, text='<b>Користувач зареєструвався за вашим посиланням\n<em>+1 реферальний бал🤤</em>\nДякуємо за те, що ви з нами💋)</b>')
        else:
            if db.get_vip(callback.message.chat.id) != '0':
                db.update_age(callback.message.chat.id, callback.data)
                if language == 'ru':
                    await callback.message.edit_text(f'<b>Видим что у вас есть 🏆VIP статус, изменить 👑VIP никнейм?⤵️</b> ',reply_markup=redakt_kb_ru)
                elif language == 'eng':
                    await callback.message.edit_text(f'<b>We see that you have 🏆VIP status, change 👑VIP nickname?⤵️</b> ',reply_markup=redakt_kb_eng)
                elif language == 'ua':
                    await callback.message.edit_text(f'<b>Бачимо, що у вас є 🏆VIP статус, змінити 👑VIP нікнейм?⤵️</b> ',reply_markup=redakt_kb_ua)
            else:
                db.update_age(callback.message.chat.id, callback.data)
                if language == 'ru':
                    await callback.message.edit_text(text=f'<b>Вы успешно создали профиль⚙️✅</b> ')
                    await callback.message.answer(text=f'<b><em>Главное меню📋⤵️</em></b> ',reply_markup=all_kb_ru)
                elif language == 'eng':
                    await callback.message.edit_text(text=f'<b>You have successfully created a profile⚙️✅</b> ')
                    await callback.message.answer(text=f'<b><em>Main menu📋⤵️</em></b> ',reply_markup=all_kb_eng)
                elif language == 'ua':
                    await callback.message.edit_text(text=f'<b>Ви успішно створили профіль⚙️✅</b> ')
                    await callback.message.answer(text=f'<b><em>Головне меню📋⤵️</em></b> ',reply_markup=all_kb_ua)

    elif db.get_vip(callback.message.chat.id) != '0':
        db.update_age(callback.message.chat.id, callback.data)
        if language == 'ru':
            await callback.message.edit_text(f'<b>Видим что у вас есть 🏆VIP статус, изменить 👑VIP никнейм?⤵️</b> ',reply_markup=redakt_kb_ru)
        elif language == 'eng':
            await callback.message.edit_text(f'<b>We see that you have 🏆VIP status, change 👑VIP nickname?⤵️</b> ',reply_markup=redakt_kb_eng)
        elif language == 'ua':
            await callback.message.edit_text(f'<b>Бачимо, що у вас є 🏆VIP статус, змінити 👑VIP нікнейм?⤵️</b> ',reply_markup=redakt_kb_ua)
    else:
        db.update_age(callback.message.chat.id, callback.data)
        if language == 'ru':
            await callback.message.edit_text(text=f'<b>Вы успешно создали профиль⚙️✅</b> ')
            await callback.message.answer(text=f'<b><em>Главное меню📋⤵️</em></b> ',reply_markup=all_kb_ru)
        elif language == 'eng':
            await callback.message.edit_text(text=f'<b>You have successfully created a profile⚙️✅</b> ')
            await callback.message.answer(text=f'<b><em>Main menu📋⤵️</em></b> ',reply_markup=all_kb_eng)
        elif language == 'ua':
            await callback.message.edit_text(text=f'<b>Ви успішно створили профіль⚙️✅</b> ')
            await callback.message.answer(text=f'<b><em>Головне меню📋⤵️</em></b> ',reply_markup=all_kb_ua)


@dp.callback_query(F.data.in_(['yes_name_redakt', 'no_name_redakt']))
async def shop_4(callback: types.CallbackQuery):
    global username
    if callback.data == 'yes_name_redakt':
        db.update_vip_name(callback.message.chat.id, f"{username}")
    else:
        db.update_vip_name(callback.message.chat.id,'User')
    language = db.get_language(callback.message.chat.id)
    if language == 'ru':
        await callback.message.edit_text(f'<b>Вы успешно редактировали профиль⚙️✅</b>')
        await callback.message.answer(text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb_ru)
    elif language == 'eng':
        await callback.message.edit_text(f'<b>You have successfully edited your profile⚙️✅</b>')
        await callback.message.answer(text=f'<b>ㅤㅤ↓  Main menu📋 ↓</b>', reply_markup=all_kb_eng)
    elif language == 'ua':
        await callback.message.edit_text(f'<b>Ви успішно змінили профіль⚙️✅</b>')
        await callback.message.answer(text=f'<b>ㅤㅤ↓  Головне меню📋 ↓</b>', reply_markup=all_kb_ua)

# # #################################################

@dp.callback_query(F.data == 'gift')
async def redact(callback: types.CallbackQuery):
    language = db.get_language(callback.message.chat.id)
    if language == 'ru':
        await callback.message.edit_text(text=f'<b>У вас на аккаунте <em><code>{db.get_reffer(callback.message.chat.id)[1]}</code></em> баллов💠\nВыбери сколько хочешь отправить баллов собеседнику⤵️</b> ', reply_markup= present_kb_ru)
    elif language == 'eng':
        await callback.message.edit_text(text=f'<b>On your account <em><code>{db.get_reffer(callback.message.chat.id)[1]}</code></em> points💠\nChoose how many points you want to send to a friend⤵️</b> ', reply_markup=present_kb_eng)
    elif language == 'ua':
        await callback.message.edit_text(text=f'<b>На вашому аккаунті <em><code>{db.get_reffer(callback.message.chat.id)[1]}</code></em> балів💠\nВиберіть скільки балів ви хочете відправити співрозмовнику⤵️</b> ', reply_markup=present_kb_ua)
    
@dp.callback_query(F.data == 'gift_1')
async def redact(callback: types.CallbackQuery):
    if db.get_active_chat(callback.message.chat.id):
        global id_1, id_2
        if callback.message.chat.id == id_1:
            id = id_2    
        elif callback.message.chat.id == id_2:
            id = id_1
        if db.get_reffer(callback.message.chat.id)[1] >= 3:
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1 ,db.get_reffer(callback.message.chat.id)[1] - 4 )
            db.update_reffer(id, db.get_reffer(id)[0] - 1 ,db.get_reffer(id)[1] + 2 )
            language_1, language_2 = db.get_language(callback.message.chat.id), db.get_language(id)
            await callback.message.delete()
            if language_1 == 'ru':
                await callback.message.answer(f'<b>Ваш подарок в <em>3 балла💠 успешно отправлен!✅</em></b>')
            elif language_1 == 'eng':
                await callback.message.answer(f'<b>Your gift worth <em>3 points💠 has been sent successfully!✅</em></b>')
            elif language_1 == 'ua':
                await callback.message.answer(f'<b>Ваш подарунок в <em>3 бали💠 успішно відправлений!✅</em></b>')

            if language_2 == 'ru':
                await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 3 балла💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>')
            elif language_2 == 'eng':
                await bot.send_message(id, f'<b>You have received a <em>gift🎁 3 points💠</em>\n\nYour points: {db.get_reffer(id)[1]}</b>')
            elif language_2 == 'ua':
                await bot.send_message(id, f'<b>Вам надіслали <em>подарунок🎁 3 бали💠</em>\n\nВаші бали: {db.get_reffer(id)[1]}</b>')
        else:
            await callback.message.delete()
            language = db.get_language(callback.message.chat.id)
            if language == 'ru':
                await callback.message.answer(f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>')
            elif language == 'eng':
                await callback.message.answer(f'<b>I\'m sorry, but you have not enough<em> points💠(((</em>\n\nBuy points with the /vip command or with our referral system💋</b>')
            elif language == 'ua':
                await callback.message.answer(f'<b>Вибачте, ви не маєте достатньо<em> балів💠(((</em>\n\nКупити бали можна за допомогою команди /vip або за допомоги нашої реферальної системи💋</b>')
            
            
@dp.callback_query(F.data == 'gift_2')
async def redact(callback: types.CallbackQuery):
    if db.get_active_chat(callback.message.chat.id):
        global id_1, id_2
        if callback.message.chat.id == id_1:
            id = id_2    
        elif callback.message.chat.id == id_2:
            id = id_1
        if db.get_reffer(callback.message.chat.id)[1] >= 10:
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1 ,db.get_reffer(callback.message.chat.id)[1] - 11 )
            db.update_reffer(id, db.get_reffer(id)[0] - 1 ,db.get_reffer(id)[1] + 9 )
            language_1, language_2 = db.get_language(callback.message.chat.id), db.get_language(id)
            await callback.message.delete()
            if language_1 == 'ru':
                await callback.message.answer(f'<b>Ваш подарок в <em>10 баллов💠 успешно отправлен!✅</em></b>')
            elif language_1 == 'eng':
                await callback.message.answer(f'<b>Your gift worth <em>10 points💠 has been sent successfully!✅</em></b>')
            elif language_1 == 'ua':
                await callback.message.answer(f'<b>Ваш подарунок в <em>10 балів💠 успішно відправлений!✅</em></b>')

            if language_2 == 'ru':
                await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 10 баллов💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>')
            elif language_2 == 'eng':
                await bot.send_message(id, f'<b>You have received a <em>gift🎁 10 points💠</em>\n\nYour points: {db.get_reffer(id)[1]}</b>')
            elif language_2 == 'ua':
                await bot.send_message(id, f'<b>Вам надіслали <em>подарунок🎁 10 балів💠</em>\n\nВаші бали: {db.get_reffer(id)[1]}</b>')
        else:
            await callback.message.delete()
            language = db.get_language(callback.message.chat.id)
            if language == 'ru':
                await callback.message.answer(f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>')
            elif language == 'eng':
                await callback.message.answer(f'<b>I\'m sorry, but you have not enough<em> points💠(((</em>\n\nBuy points with the /vip command or with our referral system💋</b>')
            elif language == 'ua':
                await callback.message.answer(f'<b>Вибачте, ви не маєте достатньо<em> балів💠(((</em>\n\nКупити бали можна за допомогою команди /vip або за допомоги нашої реферальної системи💋</b>')


@dp.callback_query(F.data == 'gift_3')
async def redact(callback: types.CallbackQuery):
    if db.get_active_chat(callback.message.chat.id):
        global id_1, id_2
        if callback.message.chat.id == id_1:
            id = id_2    
        elif callback.message.chat.id == id_2:
            id = id_1
        if db.get_reffer(callback.message.chat.id)[1] >= 20:
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1 ,db.get_reffer(callback.message.chat.id)[1] - 21 )
            db.update_reffer(id, db.get_reffer(id)[0] - 1 ,db.get_reffer(id)[1] + 19 )
            language_1, language_2 = db.get_language(callback.message.chat.id), db.get_language(id)
            await callback.message.delete()
            if language_1 == 'ru':
                await callback.message.answer(f'<b>Ваш подарок в <em>20 баллов💠 успешно отправлен!✅</em></b>')
            elif language_1 == 'eng':
                await callback.message.answer(f'<b>Your gift worth <em>20 points💠 has been sent successfully!✅</em></b>')
            elif language_1 == 'ua':
                await callback.message.answer(f'<b>Ваш подарунок в <em>20 балів💠 успішно відправлений!✅</em></b>')

            if language_2 == 'ru':
                await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 20 баллов💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>')
            elif language_2 == 'eng':
                await bot.send_message(id, f'<b>You have received a <em>gift🎁 20 points💠</em>\n\nYour points: {db.get_reffer(id)[1]}</b>')
            elif language_2 == 'ua':
                await bot.send_message(id, f'<b>Вам надіслали <em>подарунок🎁 20 балів💠</em>\n\nВаші бали: {db.get_reffer(id)[1]}</b>')
        else:
            await callback.message.delete()
            language = db.get_language(callback.message.chat.id)
            if language == 'ru':
                await callback.message.answer(f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>')
            elif language == 'eng':
                await callback.message.answer(f'<b>I\'m sorry, but you have not enough<em> points💠(((</em>\n\nBuy points with the /vip command or with our referral system💋</b>')
            elif language == 'ua':
                await callback.message.answer(f'<b>Вибачте, ви не маєте достатньо<em> балів💠(((</em>\n\nКупити бали можна за допомогою команди /vip або за допомоги нашої реферальної системи💋</b>')


@dp.callback_query(F.data == 'gift_4')
async def redact(callback: types.CallbackQuery):
    if db.get_active_chat(callback.message.chat.id):
        global id_1, id_2
        if callback.message.chat.id == id_1:
            id = id_2    
        elif callback.message.chat.id == id_2:
            id = id_1
        if db.get_reffer(callback.message.chat.id)[1] >= 30:
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1 ,db.get_reffer(callback.message.chat.id)[1] - 31 )
            db.update_reffer(id, db.get_reffer(id)[0] - 1 ,db.get_reffer(id)[1] + 29 )
            language_1, language_2 = db.get_language(callback.message.chat.id), db.get_language(id)
            await callback.message.delete()
            if language_1 == 'ru':
                await callback.message.answer(f'<b>Ваш подарок в <em>30 баллов💠 успешно отправлен!✅</em></b>')
            elif language_1 == 'eng':
                await callback.message.answer(f'<b>Your gift worth <em>30 points💠 has been sent successfully!✅</em></b>')
            elif language_1 == 'ua':
                await callback.message.answer(f'<b>Ваш подарунок в <em>30 балів💠 успішно відправлений!✅</em></b>')

            if language_2 == 'ru':
                await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 30 баллов💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>')
            elif language_2 == 'eng':
                await bot.send_message(id, f'<b>You have received a <em>gift🎁 30 points💠</em>\n\nYour points: {db.get_reffer(id)[1]}</b>')
            elif language_2 == 'ua':
                await bot.send_message(id, f'<b>Вам надіслали <em>подарунок🎁 30 балів💠</em>\n\nВаші бали: {db.get_reffer(id)[1]}</b>')
        else:
            await callback.message.delete()
            language = db.get_language(callback.message.chat.id)
            if language == 'ru':
                await callback.message.answer(f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>')
            elif language == 'eng':
                await callback.message.answer(f'<b>I\'m sorry, but you have not enough<em> points💠(((</em>\n\nBuy points with the /vip command or with our referral system💋</b>')
            elif language == 'ua':
                await callback.message.answer(f'<b>Вибачте, ви не маєте достатньо<em> балів💠(((</em>\n\nКупити бали можна за допомогою команди /vip або за допомоги нашої реферальної системи💋</b>')

@dp.callback_query(F.data == 'buy')
async def redact(callback: types.CallbackQuery):
    global id_1, id_2
    language = db.get_language(callback.message.chat.id)
    if callback.message.chat.id == id_1:
        id = id_2    
    elif callback.message.chat.id == id_2:
        id = id_1
    if language == 'ru':
            await callback.message.answer(f'Что бы оплатить тапните <a href="https://donatello.to/anonimniy_chatik18">СЮДА💋</a>\n\n❗️❗️❗️Напоминаем о том что вам нужно вписать ID собеседника : <code>{id}</code>  в \'Имя\' на сайте',disable_web_page_preview=True, reply_markup=vip_bool_kb_ru)
    if language == 'ua':
        await callback.message.answer(f'Щоб оплатити, натисніть <a href="https://donatello.to/anonimniy_chatik18">СЮДИ💋</a>\n\n❗️❗️❗️Нагадуємо, що вам потрібно вказати ID співрозмовника: <code>{id}</code> у полі "Ім’я" на сайті', disable_web_page_preview=True, reply_markup=vip_bool_kb_ua)
    if language == 'eng':
        await callback.message.answer(f'To make a payment, tap <a href="https://donatello.to/anonimniy_chatik18">HERE💋</a>\n\n❗️❗️❗️Reminder: You need to enter the recipient\'s ID: <code>{id}</code> in the "Name" field on the website', disable_web_page_preview=True, reply_markup=vip_bool_kb_eng)


    

# # #################################################
@dp.callback_query(F.data == 'vip_access')
async def shop_1(callback: types.CallbackQuery): 
    await callback.message.delete()
    language = db.get_language(callback.message.chat.id)
    if language == 'ru':
        await callback.message.answer(f'Что бы оплатить тапните <a href="https://donatello.to/anonimniy_chatik18">СЮДА💋</a>\n\nНапоминаем о том что вам нужно вписать ваш ID: <code>{callback.message.chat.id}</code> или чужой ID для подарка в \'Имя\' на сайте',disable_web_page_preview=True, reply_markup=vip_bool_kb_ru)
    if language == 'ua':
        await callback.message.answer(f'Щоб оплатити, натисніть <a href="https://donatello.to/anonimniy_chatik18">СЮДИ💋</a>\n\nНагадуємо, що вам потрібно вказати ваш ID: <code>{callback.message.chat.id}</code> або чужий ID для подарунка в полі "Ім’я" на сайті', disable_web_page_preview=True, reply_markup=vip_bool_kb_ua)
    if language == 'eng':
        await callback.message.answer(f'To make a payment, tap <a href="https://donatello.to/anonimniy_chatik18">HERE💋</a>\n\nReminder: You need to enter your ID: <code>{callback.message.chat.id}</code> or someone else\'s ID for a gift in the "Name" field on the website', disable_web_page_preview=True, reply_markup=vip_bool_kb_eng)


@dp.callback_query(F.data == 'yes_vip')
async def shop_1(callback: types.CallbackQuery): 
    vip = get_vip()
    language = db.get_language(callback.message.chat.id)
    
    if vip != None:
        if int(callback.message.chat.id) == int(vip[1]):
            if vip[2] == 'UAH':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + int((int(vip[0]) * 2.18 / 2))))
            if vip[2] == 'RUB':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + int((int(vip[0]) / 2))))
            
            if language == 'ru':
                await callback.message.edit_text(text=f'<b>Вы успешно пополнили баланс баллов💠 : {db.get_reffer(vip[1])[1]}</b>')
                await bot.send_message(callback.message.chat.id,text=f'<b>ㅤㅤ↓ <em> Главное меню📋 </em>↓</b>', reply_markup=all_kb_ru)
            elif language == 'ua':
                await callback.message.edit_text(text=f'<b>Ви успішно поповнили баланс балів💠 : {db.get_reffer(vip[1])[1]}</b>')
                await bot.send_message(callback.message.chat.id,text=f'<b>ㅤㅤ↓ <em> Головне меню📋 </em>↓</b>', reply_markup=all_kb_ua)
            elif language == 'eng':
                await callback.message.edit_text(text=f'<b>You have successfully topped up your points balance💠 : {db.get_reffer(vip[1])[1]}</b>')
                await bot.send_message(callback.message.chat.id,text=f'<b>ㅤㅤ↓ <em> Main menu📋 </em>↓</b>', reply_markup=all_kb_eng)
        
        elif int(callback.message.chat.id) != int(vip[1]):
            if vip[2] == 'UAH':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + (int(vip[0]) * 2.18 / 2)))
            if vip[2] == 'RUB':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + (int(vip[0]) / 2)))
            
            if language == 'ru':
                await callback.message.edit_text(text=f'<b>Вы успешно сделали подарок другому пользователю!!!</b>')
            elif language == 'ua':
                await callback.message.edit_text(text=f'<b>Ви успішно зробили подарунок іншому користувачеві!!!</b>')
            elif language == 'eng':
                await callback.message.edit_text(text=f'<b>You have successfully made a gift to another user!!!</b>')
            
            if db.get_active_chat(callback.message.chat.id):
                if language == 'ru':
                    await callback.message.answer(text=f'<b>ㅤㅤ↓ <em> Главное меню📋 </em>↓</b>', reply_markup=all_kb_ru)
                elif language == 'ua':
                    await callback.message.answer(text=f'<b>ㅤㅤ↓ <em> Головне меню📋 </em>↓</b>', reply_markup=all_kb_ua)
                elif language == 'eng':
                    await callback.message.answer(text=f'<b>ㅤㅤ↓ <em> Main menu📋 </em>↓</b>', reply_markup=all_kb_eng)            
            try:
                recipient_language = db.get_language(vip[1])
                if recipient_language == 'ru':
                    await bot.send_message(vip[1],text=f'<b>Вам сделал подарок другой пользователь!!!\n\nБаланс баллов💠 : {db.get_reffer(vip[1])[1]}</b>', reply_markup=all_kb_ru)
                elif recipient_language == 'ua':
                    await bot.send_message(vip[1],text=f'<b>Вам зробив подарунок інший користувач!!!\n\nБаланс балів💠 : {db.get_reffer(vip[1])[1]}</b>', reply_markup=all_kb_ua)
                elif recipient_language == 'eng':
                    await bot.send_message(vip[1],text=f'<b>You received a gift from another user!!!\n\nPoints balance💠 : {db.get_reffer(vip[1])[1]}</b>', reply_markup=all_kb_eng)
            except:
                pass
    
        db.update_vip_char(get_donates()[3])
    else:
        if language == 'ru':
            await callback.message.edit_text(text=f'<b>Нам не пришла ваша оплата, если вы уверены что все сделали правильно, напишите <em>@bbtqqrl</em> о ошибке</b>')
        elif language == 'ua':
            await callback.message.edit_text(text=f'<b>Нам не надійшла ваша оплата, якщо ви впевнені, що все зробили правильно, напишіть <em>@bbtqqrl</em> про помилку</b>')
        elif language == 'eng':
            await callback.message.edit_text(text=f'<b>We haven\'t received your payment. If you\'re sure you did everything correctly, please write to <em>@bbtqqrl</em> about the error</b>')

@dp.callback_query(F.data == 'no_vip')
async def shop_1(callback: types.CallbackQuery): 
    await callback.message.delete()
    language = db.get_language(callback.message.chat.id)
    if not db.get_active_chat(callback.message.chat.id):
        if language == 'ru':
            await callback.message.answer(f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb_ru)
        elif language == 'ua':
            await callback.message.answer(f'<b>ㅤㅤ↓  Головне меню📋 ↓</b>', reply_markup=all_kb_ua)
        elif language == 'eng':
            await callback.message.answer(f'<b>ㅤㅤ↓  Main menu📋 ↓</b>', reply_markup=all_kb_eng)#
            

 # #################################################


@dp.callback_query(F.data == 'shop_1')
async def shop_1(callback: types.CallbackQuery): 
    language = db.get_language(callback.message.chat.id)

    if db.get_reffer(callback.message.chat.id)[1] >= 3:
        db.update_dislike(-1, callback.message.chat.id)
        db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 4)
        
        if language == 'ru':
            await callback.message.edit_text(text=f'<b>Вы успешно cбросили дизлайки🤫)</b>')
            await callback.message.answer(text=f'<b>ㅤㅤ↓ <em> Главное меню📋 </em>↓</b>', reply_markup=all_kb_ru)
        elif language == 'ua':
            await callback.message.edit_text(text=f'<b>Ви успішно скинули дизлайки🤫)</b>')
            await callback.message.answer(text=f'<b>ㅤㅤ↓ <em> Головне меню📋 </em>↓</b>', reply_markup=all_kb_ua)
        elif language == 'eng':
            await callback.message.edit_text(text=f'<b>You have successfully reset dislikes🤫)</b>')
            await callback.message.answer(text=f'<b>ㅤㅤ↓ <em> Main menu📋 </em>↓</b>', reply_markup=all_kb_eng)
    else:
        if language == 'ru':
            await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>')
        elif language == 'ua':
            await callback.message.edit_text(text=f'<b>У вас мало балів💠)\n\nЯк отримати бали ви можете дізнатися в <em> Мій профіль📖</em>  →  <em>📬Реферальна система </em> </b>')
        elif language == 'eng':
            await callback.message.edit_text(text=f'<b>You don\'t have enough points💠)\n\nYou can learn how to get points in <em> My profile📖</em>  →  <em>📬Referral system </em> </b>')

@dp.callback_query(F.data == 'shop_2')
async def shop_2(callback: types.CallbackQuery):
    language = db.get_language(callback.message.chat.id)

    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 10:
            db.update_vip(callback.message.chat.id, datetime.now() + timedelta(days=1))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 11)      
            
            if language == 'ru':
                await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 на 1 день\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привилегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>', reply_markup=bool_kb_ru)
            elif language == 'ua':
                await callback.message.edit_text(f'<b>Вітаю🎉 з придбанням <em>VIP статусу🏆 на 1 день\nДякую вам❤️!</em>\n\nТепер вам доступна команда /vip_search <em>(для пошуку за статтю👥 та за віком🔞)</em> і ще купа інших <em>привілеїв💰</em>)\n\nВикористовувати ваше ім\'я в телеграмі як <em>VIP нікнейм🏆?</em></b>', reply_markup=bool_kb_ua)
            elif language == 'eng':
                await callback.message.edit_text(f'<b>Congratulations🎉 on acquiring <em>VIP status🏆 for 1 day\nThank you❤️!</em>\n\nNow you have access to the /vip_search command <em>(for searching by gender👥 and age🔞)</em> and many other <em>privileges💰</em>)\n\nUse your Telegram name as <em>VIP nickname🏆?</em></b>', reply_markup=bool_kb_eng)
        else:
            if language == 'ru':
                await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>')
            elif language == 'ua':
                await callback.message.edit_text(text=f'<b>У вас мало балів💠)\n\nЯк отримати бали ви можете дізнатися в <em> Мій профіль📖</em>  →  <em>📬Реферальна система </em> </b>')
            elif language == 'eng':
                await callback.message.edit_text(text=f'<b>You don\'t have enough points💠)\n\nYou can learn how to get points in <em> My profile📖</em>  →  <em>📬Referral system </em> </b>')
    else:
        if language == 'ru':
            await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>')
        elif language == 'ua':
            await callback.message.edit_text(f'<b>Ви вже купили <em>VIP статус🏆)\nЩе раз дякую вам дуже💋!</em></b>')
        elif language == 'eng':
            await callback.message.edit_text(f'<b>You have already bought <em>VIP status🏆)\nThank you very much again💋!</em></b>')

@dp.callback_query(F.data == 'shop_3')
async def shop_2(callback: types.CallbackQuery):
    language = db.get_language(callback.message.chat.id)

    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 20:
            db.update_vip(callback.message.chat.id,datetime.now() + timedelta(days=3))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 21)      

            
            if language == 'ru':
                await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 на 3 день\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привилегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>', reply_markup=bool_kb_ru)
            elif language == 'ua':
                await callback.message.edit_text(f'<b>Вітаю🎉 з придбанням <em>VIP статусу🏆 на 3 день\nДякую вам❤️!</em>\n\nТепер вам доступна команда /vip_search <em>(для пошуку за статтю👥 та за віком🔞)</em> і ще купа інших <em>привілеїв💰</em>)\n\nВикористовувати ваше ім\'я в телеграмі як <em>VIP нікнейм🏆?</em></b>', reply_markup=bool_kb_ua)
            elif language == 'eng':
                await callback.message.edit_text(f'<b>Congratulations🎉 on acquiring <em>VIP status🏆 for 3 day\nThank you❤️!</em>\n\nNow you have access to the /vip_search command <em>(for searching by gender👥 and age🔞)</em> and many other <em>privileges💰</em>)\n\nUse your Telegram name as <em>VIP nickname🏆?</em></b>', reply_markup=bool_kb_eng)
        else:
            if language == 'ru':
                await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>')
            elif language == 'ua':
                await callback.message.edit_text(text=f'<b>У вас мало балів💠)\n\nЯк отримати бали ви можете дізнатися в <em> Мій профіль📖</em>  →  <em>📬Реферальна система </em> </b>')
            elif language == 'eng':
                await callback.message.edit_text(text=f'<b>You don\'t have enough points💠)\n\nYou can learn how to get points in <em> My profile📖</em>  →  <em>📬Referral system </em> </b>')
    else:
        if language == 'ru':
            await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>')
        elif language == 'ua':
            await callback.message.edit_text(f'<b>Ви вже купили <em>VIP статус🏆)\nЩе раз дякую вам дуже💋!</em></b>')
        elif language == 'eng':
            await callback.message.edit_text(f'<b>You have already bought <em>VIP status🏆)\nThank you very much again💋!</em></b>')

@dp.callback_query(F.data == 'shop_4')
async def shop_2(callback: types.CallbackQuery):
    language = db.get_language(callback.message.chat.id)

    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 30:
            db.update_vip(callback.message.chat.id,datetime.now() + timedelta(days=6))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 31)         

            
            if language == 'ru':
                await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 на 6 день\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привилегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>', reply_markup=bool_kb_ru)
            elif language == 'ua':
                await callback.message.edit_text(f'<b>Вітаю🎉 з придбанням <em>VIP статусу🏆 на 6 день\nДякую вам❤️!</em>\n\nТепер вам доступна команда /vip_search <em>(для пошуку за статтю👥 та за віком🔞)</em> і ще купа інших <em>привілеїв💰</em>)\n\nВикористовувати ваше ім\'я в телеграмі як <em>VIP нікнейм🏆?</em></b>', reply_markup=bool_kb_ua)
            elif language == 'eng':
                await callback.message.edit_text(f'<b>Congratulations🎉 on acquiring <em>VIP status🏆 for 6 day\nThank you❤️!</em>\n\nNow you have access to the /vip_search command <em>(for searching by gender👥 and age🔞)</em> and many other <em>privileges💰</em>)\n\nUse your Telegram name as <em>VIP nickname🏆?</em></b>', reply_markup=bool_kb_eng)
        else:
            if language == 'ru':
                await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>')
            elif language == 'ua':
                await callback.message.edit_text(text=f'<b>У вас мало балів💠)\n\nЯк отримати бали ви можете дізнатися в <em> Мій профіль📖</em>  →  <em>📬Реферальна система </em> </b>')
            elif language == 'eng':
                await callback.message.edit_text(text=f'<b>You don\'t have enough points💠)\n\nYou can learn how to get points in <em> My profile📖</em>  →  <em>📬Referral system </em> </b>')
    else:
        if language == 'ru':
            await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>')
        elif language == 'ua':
            await callback.message.edit_text(f'<b>Ви вже купили <em>VIP статус🏆)\nЩе раз дякую вам дуже💋!</em></b>')
        elif language == 'eng':
            await callback.message.edit_text(f'<b>You have already bought <em>VIP status🏆)\nThank you very much again💋!</em></b>')

@dp.callback_query(F.data == 'shop_5')
async def shop_2(callback: types.CallbackQuery):
    language = db.get_language(callback.message.chat.id)

    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 200:
            db.update_vip(callback.message.chat.id,datetime.now() + relativedelta(years=10))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 201)          

            
            if language == 'ru':
                await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 НАВСЕГДА\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привилегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>', reply_markup=bool_kb_ru)
            elif language == 'ua':
                await callback.message.edit_text(f'<b>Вітаю🎉 з придбанням <em>VIP статусу🏆 НАЗАВЖДИ\nДякую вам❤️!</em>\n\nТепер вам доступна команда /vip_search <em>(для пошуку за статтю👥 та за віком🔞)</em> і ще купа інших <em>привілеїв💰</em>)\n\nВикористовувати ваше ім\'я в телеграмі як <em>VIP нікнейм🏆?</em></b>', reply_markup=bool_kb_ua)
            elif language == 'eng':
                await callback.message.edit_text(f'<b>Congratulations🎉 on acquiring <em>VIP status🏆 FOREVER\nThank you❤️!</em>\n\nNow you have access to the /vip_search command <em>(for searching by gender👥 and age🔞)</em> and many other <em>privileges💰</em>)\n\nUse your Telegram name as <em>VIP nickname🏆?</em></b>', reply_markup=bool_kb_eng)
        else:
            if language == 'ru':
                await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>')
            elif language == 'ua':
                await callback.message.edit_text(text=f'<b>У вас мало балів💠)\n\nЯк отримати бали ви можете дізнатися в <em> Мій профіль📖</em>  →  <em>📬Реферальна система </em> </b>')
            elif language == 'eng':
                await callback.message.edit_text(text=f'<b>You don\'t have enough points💠)\n\nYou can learn how to get points in <em> My profile📖</em>  →  <em>📬Referral system </em> </b>')
    else:
        if language == 'ru':
            await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>')
        elif language == 'ua':
            await callback.message.edit_text(f'<b>Ви вже купили <em>VIP статус🏆)\nЩе раз дякую вам дуже💋!</em></b>')
        elif language == 'eng':
            await callback.message.edit_text(f'<b>You have already bought <em>VIP status🏆)\nThank you very much again💋!</em></b>')


# # #################################################
# #################################################

@dp.callback_query(F.data.in_(['yes_name', 'no_name']))
async def shop_4(callback: types.CallbackQuery):
    global username
    language = db.get_language(callback.message.chat.id)

    if callback.data == 'yes_name':
        db.update_vip_name(callback.message.chat.id, f"@{username}")
    else:
        db.update_vip_name(callback.message.chat.id, 'User')

    if language == 'ru':
        await callback.message.edit_text(text='<b>Супер👏 , теперь ваши собеседники будут видеть такой текст⤵️</b>')
        await callback.message.answer(f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n\nЯзык 🌐 : {language_dict[language][db.get_language(callback.message.chat.id)]} Никнейм😶‍🌫️: {db.get_vip_name(callback.message.chat.id)}\n\nЛайков 👍 : {db.get_like(callback.message.chat.id)}\nДизлайков 👎 : {db.get_dislike(callback.message.chat.id)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>')
        await callback.message.answer(f'<b>Ещё раз спасибо вам большое💋!</b>')
        await callback.message.answer(text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb_ru)
    elif language == 'ua':
        await callback.message.edit_text(text='<b>Супер👏 , тепер ваші співрозмовники будуть бачити такий текст⤵️</b>')
        await callback.message.answer(f'<b>🔥<em>🏆VIP</em> співрозмовник знайдений🏆🔥\n\nМова 🌐 : {language_dict[language][db.get_language(callback.message.chat.id)]} Нікнейм😶‍🌫️: {db.get_vip_name(callback.message.chat.id)}\n\nЛайків 👍 : {db.get_like(callback.message.chat.id)}\nДизлайків 👎 : {db.get_dislike(callback.message.chat.id)}\n\nА якщо теж хочеш <em>VIP статус🏆</em> тоді тапай на ➡️ <em>/vip або /shop</em> \n\n ↓ <em>Приємного спілкування🫦</em> ↓</b>')
        await callback.message.answer(f'<b>Ще раз дуже вам дякую💋!</b>')
        await callback.message.answer(text=f'<b>ㅤㅤ↓  Головне меню📋 ↓</b>', reply_markup=all_kb_ua)
    elif language == 'eng':
        await callback.message.edit_text(text='<b>Great👏 , now your interlocutors will see this text⤵️</b>')
        await callback.message.answer(f'<b>🔥<em>🏆VIP</em> interlocutor found🏆🔥\n\nLanguage 🌐 : {language_dict[language][db.get_language(callback.message.chat.id)]} Nickname😶‍🌫️: {db.get_vip_name(callback.message.chat.id)}\n\nLikes 👍 : {db.get_like(callback.message.chat.id)}\nDislikes 👎 : {db.get_dislike(callback.message.chat.id)}\n\nAnd if you also want <em>VIP status🏆</em> then tap on ➡️ <em>/vip or /shop</em> \n\n ↓ <em>Enjoy your conversation🫦</em> ↓</b>')
        await callback.message.answer(f'<b>Thank you very much again💋!</b>')
        await callback.message.answer(text=f'<b>ㅤㅤ↓  Main menu📋 ↓</b>', reply_markup=all_kb_eng)

# # ############################################################################################################################################
# # ############################################################################################################################################
# # FUNC
    # # ############################################################################################################################################
# # ############################################################################################################################################
# # FUNC



def check_vip(user_id):
    if db.get_vip(user_id) != '0' and db.get_vip(user_id) != 'None' and db.get_vip(user_id) != None:
        if datetime.strptime(db.get_vip(user_id), '%Y-%m-%d %H:%M:%S.%f') < datetime.now():
            db.update_vip(user_id, '0')
            return False
    return True


def get_donates():
    url = 'https://donatello.to/api/v1/donates'
    headers = {'X-Token': '27028dab80971eab9cb24ddc981c8685'}

    response = requests.get(url, headers=headers).json()

    name = response['content'][0]['clientName']
    amount = response['content'][0]['amount']
    currency = response['content'][0]['currency']
    date = response['content'][0]['createdAt']
    return (amount, name, currency, date)

def get_vip():
    result = get_donates()
    if result[3] != db.get_vip_char():
        return (result[0],result[1], result[2])
    else:
        return None

def check_telegram_link(message):
    if  "@" in message or "https://" in message or "link" in message or "ссылка" in message or "ссылке" in message or "ссылку" in message:
        return False
    else:
        return True


# # ############################################################################################################################################
# # ############################################################################################################################################
# # ############################################################################################################################################












async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запуск бота за допомогою asyncio
    asyncio.run(main())