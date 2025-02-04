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


# ____________тут більшість взіх змінн та частково кнопки______
# ############################################################################################################################################


db = Database('db.db')

gender_dict = {
    'boy': 'Мужской🤵',
    'girl': 'Женский👸'
}

age_dict = {
    'True': 'Больше 18🔞🍓',
    'False': 'Меньше 18🫣💋'
}


bot = Bot(token='6060478130:AAEXsnJL7QLvI-aC-gYWDCw98y3wJLnwUjM', default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

count_mess_1, count_mess_2, count_chat_1, count_chat_2, id_1, id_2, username, marker = 0, 0, 0, 0, 0, 0, 0, False
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
all_kb = create_reply_keyboard(['Парень🔎🤵', '👥Рандом', 'Девушка🔎👸', 'Профиль📖', 'VIP СТАТУС💎', 'Обмен → 💠'], adjust=[3, 3])
menu_kb = create_reply_keyboard('Главное меню📋', adjust=[1])
chat_kb = create_reply_keyboard(['Сделать подарок🎁', '/stop'], adjust=[2])
stop_kb = create_reply_keyboard('/stop_search', adjust=[1])

# Create inline keyboards
gift_kb = create_inline_keyboard([
    ('Купить баллы💠', 'buy'),
    ('Подарить баллы🎁', 'gift')
], adjust=[1])

present_kb = create_inline_keyboard([
    ('3 балла💠', 'gift_1'),
    ('10 баллов💠', 'gift_2'),
    ('20 баллов💠', 'gift_3'),
    ('30 баллов💠', 'gift_4')
], adjust=[1])

top_kb = create_inline_keyboard([
    ('🏆Топ активности🥊', 'activ'),
    ('🏆Топ кармы🎭', 'karma')
], adjust=[1])

like_kb = create_inline_keyboard([
    ('👍', 'like'),
    ('👎', 'dislike')
], adjust=[2])

report_kb = create_inline_keyboard([    
    ('👍', 'like'),
    ('👎', 'dislike'),
    ('Жалоба⚠️', 'report')]
, adjust=[2, 1])

profile_kb = create_inline_keyboard([
    ('⚙️Редактировать профиль', 'redact'),
    ('📬Реферальная система', 'referal'),
    ('🥇Топы участников', 'top')
], adjust=[1])

gender_kb = create_inline_keyboard([
    ('Парень🤵', 'boy'),
    ('Девушка👸', 'girl')
], adjust=[1])

shop_kb = create_inline_keyboard([
    ('Сброс дизлайков😉 — 3 балла💠', 'shop_1'),
    ('1 день VIP статуса🏆 — 10 баллов💠', 'shop_2'),
    ('3 дня VIP статуса🏆 — 20 баллов💠', 'shop_3'),
    ('6 дней VIP статуса🏆 — 30 баллов💠', 'shop_4'),
    ('VIP статус👑 НАВСЕГДА — 200 баллов💠', 'shop_5')
], adjust=[1])

anon_kb = create_inline_keyboard([
    ('+3 балла💠', 'https://t.me/anonimniy_chatik18_bot?start=1135699139')
], adjust=[1])

fusion_kb = create_inline_keyboard([
    ('+20 балів💠', 'https://t.me/fusion_sh0p_bot?start=1135699139')
], adjust=[1])

vip_kb = create_inline_keyboard([('КУПИТЬ БАЛЛЫ💠', 'vip_access')], adjust=[1])

vip_bool_kb = create_inline_keyboard([
    ('Я оплатил✅', 'yes_vip'),
    ('Отменить❌', 'no_vip')
], adjust=[1])

age_kb = create_inline_keyboard([
    ('Больше 18🔞🍓', 'True'),
    ('Меньше 18🫣💋', 'False')
], adjust=[1])

search_boy_kb = create_inline_keyboard([
    ('Больше 18🔞🍓', 'boy_True'),
    ('Меньше 18🫣💋', 'boy_False')
], adjust=[1])

search_girl_kb = create_inline_keyboard([
    ('Больше 18🔞🍓', 'girl_True'),
    ('Меньше 18🫣💋', 'girl_False')
], adjust=[1])

search_gender_kb = create_inline_keyboard([
    ('Парень🔎🤵', 'search_boy'),
    ('Девушка🔎👸', 'search_girl')
], adjust=[1])

bool_kb = create_inline_keyboard([
    ('ДА✅', 'yes_name'),
    ('НЕТ❌', 'no_name')
], adjust=[1])

redakt_kb = create_inline_keyboard([
    ('ДА✅', 'yes_name_redakt'),
    ('НЕТ❌', 'no_name_redakt')
], adjust=[1])

# ############################################################################################################################################
# ############################################################################################################################################



        
# функцыонал гендеру, меню ы тд_____________________________________
# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp.message(F.text == 'Профиль📖')
async def profile(message: Message):
    global username
    username = message.from_user.first_name
    vip = 'Присутсвует' if db.get_vip(message.chat.id) != '0' else 'Отсутсвует'
    
    await message.answer(
        f'<b>Ваш профиль👾 \n\n#️⃣ ID: <em><code>{message.chat.id}</code></em> \n'
        f'👫 Пол:  <em>{gender_dict[db.get_gender(message.chat.id)]}</em>\n'
        f'😇Возраст: <em>{age_dict[db.get_age(message.chat.id)]}\n\n'
        f'🏆VIP статус: {vip}\n👑VIP никнейм: {db.get_vip_name(message.chat.id)}\n\n'
        f'💬Сообщений : {db.show_num_mess(message.chat.id)}\n'
        f'💌Чатов : {db.show_num_chat(message.chat.id)}     </em> \n\n'
        f'🎭Ваша карма⤵️\n<em>Лайков 👍 : {db.get_like(message.chat.id)}\n'
        f'Дизлайков 👎 : {db.get_dislike(message.chat.id)}</em>\n\n'
        f'💼Реф. профиль⤵️<em>\nПриглашено юзеров👥: {db.get_reffer(message.chat.id)[0]}\n'
        f'Реферальных баллов💠: {db.get_reffer(message.chat.id)[1]}</em></b>',
        reply_markup=profile_kb
    )

# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp.message(F.text == 'VIP СТАТУС💎')
async def vip(message: Message):
    global username
    username = message.from_user.first_name
    
    photo = FSInputFile("vip_photo.jpg")
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
        reply_markup=vip_kb
    )

# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp.message(F.text == 'Главное меню📋')
async def menu(message: Message):
    await message.answer('<b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>', reply_markup=all_kb)
# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp.message(F.text == 'Обмен → 💠')
async def exchange_shop(message: Message):
    global username
    username = message.from_user.first_name
    await message.answer(
        f'<b>Наш магазин для обмена баллов💠⤵️\n\n'
        f'Ваших баллов:   {db.get_reffer(message.chat.id)[1]}💎\n\n'
        f'А как получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em></b>',
        reply_markup=shop_kb
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
        global reffer_id
        try:
            db.del_chat(message.chat.id)
        except:
            pass
        
        try:
            reffer_id = int(message.text[7:])
        except:
            reffer_id = False
            
        if db.check_user(message.chat.id):
            await message.answer_sticker(sticker='CAACAgIAAxkBAAEI4-tkV4lOb3MNjmu-FuZ6TBl1daqalQACZAEAAntOKhAOzIvWIO0fji8E')
            await message.answer(text=f'<b>Снова здраствуй в нашем анонимном чат боте🤗 \n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
        else:
            await message.answer(f'<b>Привет пользователь!\nУкажите ваш пол👰🏻‍♂️</b>', reply_markup=gender_kb)

    else:
        await message.answer(f'<b>Вы не можете отправлять команды в чате, что бы его остановить используйте команду /stop</b>', reply_markup= chat_kb)      




@dp.message(Command('stop_search'))
async def stop_search(message: Message):
    if not db.get_active_chat(message.chat.id):
        global last_start_mes
        if db.del_queue(message.chat.id):
            try:
                await bot.delete_message(message.chat.id, last_start_mes.message_id)
                last_start_mes = None
            except:
                True
            await message.answer(f'<b>ㅤВы остановили поиск😣\nㅤㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',reply_markup=all_kb)
            
        elif not db.del_queue(message.chat.id):
            await message.answer(f'<b>ㅤВы не начали поиск😣\nㅤㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',reply_markup=all_kb)           
    else:
        await message.answer(f'<b>Вы не можете отправлять команды в активном чате, что бы его остановить используйте команду /stop</b>', reply_markup= chat_kb)    
        
        
   
@dp.message(Command('stop'))
async def stop_chat(message: Message):
    global count_mess_1 ,count_chat_1, count_mess_2, count_chat_2, id_1, id_2
    if db.get_active_chat(message.chat.id):        
        try:            
            if id_1 == message.chat.id: 
                kb = like_kb
                if db.get_vip(id_2) != '0':
                    kb = report_kb
                await bot.send_message(chat_id= id_2 ,text=f'<b>Ваш собеседник закончил диалог🤧</b>', reply_markup=menu_kb)
                await bot.send_message(chat_id= id_2 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup= kb)
                kb = like_kb                
                if db.get_vip(message.chat.id) != '0':
                    kb = report_kb
                await bot.send_message(chat_id= id_1  ,text=f'<b>Вы закончили диалог🤧</b>', reply_markup= menu_kb)
                await bot.send_message(chat_id= id_1 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup= kb)
                db.add_mess_chat(message.chat.id, count_mess_2, count_chat_2 + 1)
                db.add_mess_chat(db.get_active_chat(message.chat.id)[1], count_mess_1, count_chat_1 + 1)  
            elif id_2 == message.chat.id:
                kb = like_kb
                if db.get_vip(id_1) != '0':
                    kb = report_kb
                await bot.send_message(chat_id= id_1 ,text=f'<b>Ваш собеседник закончил диалог🤧</b>', reply_markup=menu_kb)
                await bot.send_message(chat_id= id_1 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup= kb)
                kb = like_kb    
                if db.get_vip(message.chat.id) != '0':
                    kb = report_kb
                await bot.send_message(chat_id= id_2  ,text=f'<b>Вы закончили диалог🤧</b>', reply_markup= menu_kb)
                await bot.send_message(chat_id= id_2 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup= kb)
                db.add_mess_chat(db.get_active_chat(message.chat.id)[1], count_mess_2, count_chat_2 + 1)
                db.add_mess_chat(message.chat.id, count_mess_1, count_chat_1 + 1) 

            db.del_chat(db.get_active_chat(message.chat.id)[0])
            
        except:
            await message.answer(text=f'<b>Вы не начали чат☹️! \n ↓<em>Меню📋</em>↓</b>', reply_markup= menu_kb)

    else:
        global last_start_mes
        if db.del_queue(message.chat.id):
            try:
                await bot.delete_message(message.chat.id, last_start_mes.message_id)
                last_start_mes = None
            except:
                True
            await message.answer(f'<b>ㅤВы остановили поиск😣\nㅤㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',reply_markup=all_kb)
            
        else:
            await message.answer(text=f'<b>Вы не начали чат☹️! \n ↓<em>Меню📋</em>↓</b>', reply_markup= menu_kb)         



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


@dp.message(Command('alert_bbtqqrl'))
async def start(message: Message):
    global marker
    if message.chat.id == 1135699139 or message.chat.id == '1135699139' or message.from_user.username == 'bbtqqrl':
        await bot.send_message('1135699139',f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: </b>')
        
@dp.message(Command('menu'))
async def command_start_search(message: Message):
    if not db.get_active_chat(message.chat.id):
        if not check_vip(message.chat.id):
            await message.answer( text= '<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>')
            return await message.answer(text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb)
        else:
            pass
        try:
            db.del_chat(message.chat.id)
        except:
            pass
        await message.answer(f'<b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',reply_markup=all_kb)
    else:
        await message.answer(f'<b>Вы не можете отправлять команды в чате, что бы его остановить используйте команду /stop</b>', reply_markup= chat_kb)  

@dp.message(Command('vip'))
async def vip(message: Message):
    if not db.get_active_chat(message.chat.id):
        global username
        username = message.from_user.first_name
        photo = FSInputFile("vip_photo.jpg")
        await message.answer_photo(photo, caption='Преимущества<b> VIP статуса👑⤵️</b>\n\n<em>1️⃣. <b>БАН</b> спам рекламы🛑\n2️⃣. Никаких ограничений🤑\n3️⃣. Всегда <b>ПЕРВЫЙ</b> в поиске!!!\n4️⃣. Поиск по <b>возрасту</b>🤫(/vip_search)...\n5️⃣. <b>ВСЕ</b> будут видеть твой статус💠\n6️⃣. Ты сможешь создать свой ник🔥\n7️⃣. Возможность <b>ПОЖАЛОВАТЬСЯ</b> на плохого собеседника🚫\n🎱. И в конце концов ты сможешь получить VIP <b>БЕСПЛАТНО</b>❤️‍🔥\n\nДа и ты получишь возможность увидеть себя в <b>топе VIP🏆 активности</b>\n\nЛюбим каждого💕💕💕</em>')
        await message.answer( text= f'<b><em>VIP🏆 статус</em> покупается за баллы в /shop , а здесь можно купить балы по курсу⤵️\n\n1 балл💠 - <em>2 рубля или 0,92 гривны\n\n⚠️⚠️ВНИМАНИЕ⚠️⚠️</em>\nПри покупке баллов вам нужно вставить ваш ID или ID пользователя которому вы хотите сделать подарок в поле "Имя" или "Ім`я"  . Тогда покупка будет зарегистрирована и вам придет уведомление/)\n\nВаш ID - <code>{message.chat.id}</code>⚠️\n\n<em>Любим каждого💕💕💕</em></b>', reply_markup=vip_kb)
    else:
        await message.answer(f'<b>Вы не можете отправлять команды в чате, что бы его остановить используйте команду /stop</b>', reply_markup= chat_kb)  


@dp.message(Command('shop'))
async def shop(message: Message):
    if not db.get_active_chat(message.chat.id):
        await message.answer(f'<b>\nНаш магазин для обмена баллов💠⤵️\n\n А как получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em></b>',reply_markup=shop_kb)
    else:
        await message.answer(f'<b>Вы не можете отправлять команды в чате, что бы его остановить используйте команду /stop</b>', reply_markup= chat_kb)           
            
            
@dp.message(Command('vip_search'))
async def command_start_search(message: Message): 
    if not db.get_active_chat(message.chat.id):
        global username
        if not check_vip(message.chat.id):
            await message.answer( text= '<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>')
            return await message.answer(text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb) 
        
        if db.get_vip(message.chat.id) != '0':
            await message.answer(f'<b>Снова здраствуй 🏆VIP пользователь⤵️\nНикнейм: {db.get_vip_name(message.chat.id)}\n\n👑Кого искать👥?</b>', reply_markup= search_gender_kb)
        elif db.get_vip(message.chat.id) == '0':
            username = message.from_user.first_name
            photo = FSInputFile("vip_photo.jpg")
            await message.answer_photo(photo, caption='Преимущества<b> VIP статуса👑⤵️</b>\n\n<em>1️⃣. <b>БАН</b> спам рекламы🛑\n2️⃣. Никаких ограничений🤑\n3️⃣. Всегда <b>ПЕРВЫЙ</b> в поиске!!!\n4️⃣. Поиск по <b>возрасту</b>🤫(/vip_search)...\n5️⃣. <b>ВСЕ</b> будут видеть твой статус💠\n6️⃣. Ты сможешь создать свой ник🔥\n7️⃣. Возможность <b>ПОЖАЛОВАТЬСЯ</b> на плохого собеседника🚫\n🎱. И в конце концов ты сможешь получить VIP <b>БЕСПЛАТНО</b>❤️‍🔥\n\nДа и ты получишь возможность увидеть себя в <b>топе VIP🏆 активности</b>\n\nЛюбим каждого💕💕💕</em>')
            await message.answer(text= f'<b><em>VIP🏆 статус</em> покупается за баллы в /shop , а здесь можно купить балы по курсу⤵️\n\n1 балл💠 - <em>2 рубля или 0,92 гривны\n\n⚠️⚠️ВНИМАНИЕ⚠️⚠️</em>\nПри покупке баллов вам нужно вставить ваш ID или ID пользователя которому вы хотите сделать подарок в поле "Имя" или "Ім`я"  . Тогда покупка будет зарегистрирована и вам придет уведомление/)\n\nВаш ID - <code>{message.chat.id}</code>⚠️\n\n<em>Любим каждого💕💕💕</em></b>', reply_markup=vip_kb)
    else:
        await message.answer(f'<b>Вы уже состоите в чате, что бы его остановить используйте команду /stop</b>', reply_markup= chat_kb)   

       
       
@dp.message(Command('search'))
async def command_start_search(message: Message): 
    if not db.get_active_chat(message.chat.id):   
        global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2
        if not check_vip(message.chat.id):
            await message.answer( text= '<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>')
            return await message.answer(text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb) 
        else:
            pass

        try:
            if message.chat.type == 'private':
                if db.check_queue(message.chat.id):
                    chat_2 = db.get_chat(db.get_gender(message.chat.id),db.get_age(message.chat.id))[0]
                    if db.create_chat(message.chat.id, chat_2) == False:
                        db.add_queue(message.chat.id,  db.get_gender(message.chat.id), db.get_age(message.chat.id))
                        last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup= stop_kb)
                    else:
                        count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                        count_mess_2, count_chat_2 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id) 
                        
                        id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        try:
                            if db.get_vip(id_1) != '0':
                                await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                                
                            elif db.get_vip(id_1) == '0':
                                await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                            if db.get_vip(id_2) != '0':
                                await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                                
                            elif db.get_vip(id_2) == '0':     
                                await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                                            
                        except:
                            db.del_chat(db.get_active_chat(message.chat.id)[0])
                            try:
                                await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
                            except:
                                await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)

                else:
                    await message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup= stop_kb)

            
        except:    
            await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
    else:
        await message.answer(f'<b>Вы уже состоите в чате, что бы его остановить используйте команду /stop</b>', reply_markup= chat_kb)
        

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
                await bot.send_photo(user_id[0], photo=message.photo[-1].file_id, caption=message.caption, reply_markup=all_kb)  
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
            if message.chat.id == id_2:
                await bot.send_photo(id_1, photo=message.photo[-1].file_id)
                await bot.send_photo('1135699139', photo=message.photo[-1].file_id)
            elif message.chat.id == id_1:
                await bot.send_photo(id_2, photo=message.photo[-1].file_id)
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
        await message.answer( text= '<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>')
        return await message.answer(text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb)
    else:
        pass 
    try:
        if message.text == 'Сделать подарок🎁':
            await asyncio.sleep(1)
            if db.get_active_chat(message.chat.id):
                await message.answer(text=f'<b>Купить собеседнику баллы или подарить свои?🎁 </b>', reply_markup=gift_kb)
                    
        elif check_telegram_link(message.text):
            count_mess_1 += 1
            count_mess_2 += 1
            await bot.send_message(db.get_active_chat(message.chat.id)[1], message.text)
        else:
            if db.get_vip(message.chat.id) == '0':
                if datetime.strptime(db.get_date(message.chat.id), '%Y-%m-%d %H:%M:%S.%f')+ timedelta(seconds=15) > datetime.now():
                    await message.answer( '<b>Извини но без <em>VIP🏆 статуса</em> в начале диалога такие сообщения отправлять нельзя🛑!(защита от спамеров)\n\n<em>Покупай /vip статус</em> и тебя не будут тревожить никакие ограничения💋</b>')
                    if db.get_active_chat(message.chat.id):                          
                        if id_1 == message.chat.id: 
                            kb = like_kb
                            if db.get_vip(id_2) != '0':
                                kb = report_kb
                            await bot.send_message(chat_id= id_2 ,text=f'<b>Ваш собеседник закончил диалог🤧</b>', reply_markup=all_kb)
                            await bot.send_message(chat_id= id_2 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup= kb)
                            kb = like_kb             
                            if db.get_vip(message.chat.id) != '0':
                                kb = report_kb
                            await bot.send_message(chat_id= id_1  ,text=f'<b>Вы закончили диалог🤧</b>', reply_markup= all_kb)
                            await bot.send_message(chat_id= id_1 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup= kb)
                            db.add_mess_chat(message.chat.id, count_mess_2, count_chat_2 + 1)
                            db.add_mess_chat(db.get_active_chat(message.chat.id)[1], count_mess_1, count_chat_1 + 1)  
                        elif id_2 == message.chat.id:
                            kb = like_kb
                            if db.get_vip(id_1) != '0':
                                kb = report_kb
                            await bot.send_message(chat_id= id_1 ,text=f'<b>Ваш собеседник закончил диалог🤧</b>', reply_markup=all_kb)
                            await bot.send_message(chat_id= id_1 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup= kb)
                            kb = like_kb             
                            if db.get_vip(message.chat.id) != '0':
                                kb = report_kb
                            await bot.send_message(chat_id= id_2  ,text=f'<b>Вы закончили диалог🤧</b>', reply_markup= all_kb)
                            await bot.send_message(chat_id= id_2 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>', reply_markup= kb)
                            db.add_mess_chat(db.get_active_chat(message.chat.id)[1], count_mess_2, count_chat_2 + 1)
                            db.add_mess_chat(message.chat.id, count_mess_1, count_chat_1 + 1) 

                        db.del_chat(db.get_active_chat(message.chat.id)[0])
                else:
                    await bot.send_message(db.get_active_chat(message.chat.id)[1], message.text)
            else:
                await bot.send_message(db.get_active_chat(message.chat.id)[1], message.text)   
            
            
    except:    
        
        if message.chat.type == 'private':
            
            if message.text == '👥Рандом':
                chat_2 = db.get_chat(db.get_gender(message.chat.id),db.get_age(message.chat.id))[0]
                if db.check_queue(message.chat.id):

                    if db.create_chat(message.chat.id, chat_2) == False:
                        db.add_queue(message.chat.id,  db.get_gender(message.chat.id), db.get_age(message.chat.id))
                        last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup= stop_kb)
                    else:
                        count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                        count_mess_2, count_chat_2 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id) 
                        
                        id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        try:
                            if db.get_vip(id_1) != '0':
                                await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                                
                            elif db.get_vip(id_1) == '0':
                                await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                            if db.get_vip(id_2) != '0':
                                await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                                
                            elif db.get_vip(id_2) == '0':     
                                await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)

                        except:
                            db.del_chat(db.get_active_chat(message.chat.id)[0])
                            try:
                                await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
                            except:
                                await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
                else:
                    await message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup= stop_kb)                   
                        
            elif message.text == 'Девушка🔎👸':
                chat_2 = db.get_gender_chat( db.get_gender(message.chat.id),db.get_age(message.chat.id), 'girl')[0]
                if db.check_queue(message.chat.id):

                    if db.create_chat(message.chat.id, chat_2) == False:
                        db.add_queue_gender(message.chat.id,  db.get_gender(message.chat.id), db.get_age(message.chat.id),'girl')
                        last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup= stop_kb)
                    else:
                        id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        count_mess_1, count_chat_1 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id)
                        count_mess_2, count_chat_2 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)                     
                        try:
                            if db.get_vip(id_1) != '0':
                                await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                                
                            elif db.get_vip(id_1) == '0':
                                await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                            if db.get_vip(id_2) != '0':
                                await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                                
                            elif db.get_vip(id_2) == '0':     
                                await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                        except:
                            db.del_chat(db.get_active_chat(message.chat.id)[0])
                            try:
                                await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
                            except:
                                await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
                else:
                    await message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup= stop_kb)    
                    
                    
                        
            elif message.text == 'Парень🔎🤵':
                chat_2 = db.get_gender_chat(db.get_gender(message.chat.id),db.get_age(message.chat.id), 'boy')[0]
                if db.check_queue(message.chat.id):

                    if db.create_chat(message.chat.id, chat_2) == False:
                        db.add_queue_gender(message.chat.id,  db.get_gender(message.chat.id), db.get_age(message.chat.id), 'boy')
                        last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup= stop_kb)
                    else:
                        id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        count_mess_1, count_chat_1 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id)
                        count_mess_2, count_chat_2 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)                        
                        kb.keyboard.clear()
                        
                        kb.add(*chat_kb)
                        try:
                            if db.get_vip(id_1) != '0':
                                await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                                
                            elif db.get_vip(id_1) == '0':
                                await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                            if db.get_vip(id_2) != '0':
                                await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                                
                            elif db.get_vip(id_2) == '0':     
                                await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                        except:
                            db.del_chat(db.get_active_chat(message.chat.id)[0])
                            try:
                                await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
                            except:
                                await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
                    
                
                else:
                    await message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup= stop_kb)
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
    try:
        db.update_like(db.get_like(id), id)
        await callback.message.edit_text(text=f'<b><em>Вы оценили собеседника: 👍</em></b><b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>')
        await bot.send_message(chat_id= id, text= f'<b>↑<em>Вам поставили лайк👍</em>↑</b>')
    except:
        await callback.message.edit_text(text=f'<b>Не спамьте пожалуйста🤫 \nШтраф + 5 дизлайков👎</b>')
            
            
            
@dp.callback_query(F.data == 'dislike')
async def dislike(callback: types.CallbackQuery):
    global id_2, id_1

    if id_2 == callback.message.chat.id:
        id = id_1
    else:
        id = id_2
    try:
        db.update_dislike(db.get_dislike(id), id)
        await callback.message.edit_text(text=f'<b><em>Вы оценили собеседника: 👎</em></b><b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>')
        await bot.send_message(chat_id= id, text= f'<b>↑<em>Вам поставили дизлайк👎</em>↑</b>')
    except:
        await callback.message.edit_text(text=f'<b>Не спамьте пожалуйста🤫 \nШтраф + 5 дизлайков👎</b>')
            
            
            
            
@dp.callback_query(F.data == 'report')
async def dislike(callback: types.CallbackQuery):
    global id_2, id_1

    if id_2 == callback.message.chat.id:
        id = id_1
    else:
        id = id_2

    try:
        db.update_report(db.get_report(id), id)
        await callback.message.edit_text(text=f'<b><em>Вы отправили жалобу на собеседника!</em></b>')
        await bot.send_message(chat_id= id, text= f'<b>↑<em>🏆VIP юзер отправил жалобу на вас!</em>↑</b>')
    except:
        await callback.message.edit_text(text=f'<b>Не спамьте пожалуйста🤫 \nШтраф + 5 дизлайков👎</b>')
# # #################################################
@dp.callback_query(F.data == 'search_boy')
async def search_boy(callback: types.CallbackQuery):
    await callback.message.edit_text(text=f'<b>Искать парня🤵 возраст которого?⤵️</b>', reply_markup=search_boy_kb)

    
@dp.callback_query(F.data == 'search_girl')
async def search_girl(callback: types.CallbackQuery):
    await callback.message.edit_text(text=f'<b>Искать девушку🤵‍♀️ возраст которой?⤵️</b>', reply_markup=search_girl_kb)
    

@dp.callback_query(F.data == 'boy_True')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2 

    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'boy', 'True')
        
    try:
        if callback.message.chat.type == 'private':
            if db.check_queue(callback.message.chat.id):                
                if db.create_chat(callback.message.chat.id, chat_2) == False:
                    db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'boy', 'True')
                    last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup= stop_kb)
                else:
                    count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                    count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
                    
                    id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
                    id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
                    
                    try:
                        if db.get_vip(id_1) != '0':
                            await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                        elif db.get_vip(id_1) == '0':
                            await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                        
                        if db.get_vip(id_2) != '0':
                            await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                        elif db.get_vip(id_2) == '0':     
                            await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                    except:
                        db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                        try:
                            await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
                        except:
                            await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)

            else:
                await callback.message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup= stop_kb)

        
    except:    
        await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)

    
@dp.callback_query(F.data == 'boy_False')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2

    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'boy', 'False')
        
    try:
        if callback.message.chat.type == 'private':
            if db.check_queue(callback.message.chat.id):                
                if db.create_chat(callback.message.chat.id, chat_2) == False:
                    db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'boy', 'False')
                    last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup= stop_kb)
                else:
                    count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                    count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
                    
                    id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
                    id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
                    
                    try:
                        if db.get_vip(id_1) != '0':
                            await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                        elif db.get_vip(id_1) == '0':
                            await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                        
                        if db.get_vip(id_2) != '0':
                            await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                        elif db.get_vip(id_2) == '0':     
                            await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                    except:
                        db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                        try:
                            await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
                        except:
                            await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)

            else:
                await callback.message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup= stop_kb)

        
    except:    
        await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)


@dp.callback_query(F.data == 'girl_True')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2

    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'girl', 'True')

    try:
        if callback.message.chat.type == 'private':
            if db.check_queue(callback.message.chat.id):
                if db.create_chat(callback.message.chat.id, chat_2) == False:
                    db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'girl', 'True')
                    last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup= stop_kb)
                else:
                    count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                    count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
                    
                    id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
                    id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
                    
                    try:
                        if db.get_vip(id_1) != '0':
                            await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                        elif db.get_vip(id_1) == '0':
                            await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                        
                        if db.get_vip(id_2) != '0':
                            await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                        elif db.get_vip(id_2) == '0':     
                            await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                    except:
                        db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                        try:
                            await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
                        except:
                            await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)

            else:
                await callback.message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup= stop_kb)

        
    except:    
        await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)


        


@dp.callback_query(F.data == 'girl_False')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2
    
    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'girl', 'False')
    try:
        if callback.message.chat.type == 'private':
            if db.check_queue(callback.message.chat.id):                
                if db.create_chat(callback.message.chat.id, chat_2) == False:
                    
                    db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'girl', 'False')
                    last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>', reply_markup= stop_kb)
                else:
                    count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                    count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
                    
                    id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
                    id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
                    
                    try:
                        if db.get_vip(id_1) != '0':
                            await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                        elif db.get_vip(id_1) == '0':
                            await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                        
                        if db.get_vip(id_2) != '0':
                            await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                            
                        elif db.get_vip(id_2) == '0':     
                            await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>', reply_markup= chat_kb)
                    except:
                        db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                        try:
                            await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
                        except:
                            await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)

            else:
                await callback.message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>', reply_markup= stop_kb)

        
    except:    
        await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)



# # #################################################

@dp.callback_query(F.data == 'top')
async def top(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f'<b><em>Спасибо за то что выбрали наш чат!💋</em>\n\n<em>Варианты топов⤵️</em></b>', reply_markup= top_kb)
    
@dp.callback_query(F.data == 'karma')
async def activ(callback: types.CallbackQuery):   
    await callback.answer()
    await callback.message.edit_text(text= f"Топ кармы🏆⤵️\n\n🥇. ID:  <code>{db.get_top_likes()[0][0]} </code>-- Лайков: {db.get_top_likes()[0][1]}👍\n🥈. ID:  <code>{db.get_top_likes()[1][0]} </code>-- Лайков: {db.get_top_likes()[1][1]}👍\n🥉. ID:  <code>{db.get_top_likes()[2][0]} </code>-- Лайков: {db.get_top_likes()[2][1]}👍\n4 . ID:  <code>{db.get_top_likes()[3][0]} </code>-- Лайков: {db.get_top_likes()[3][1]}👍\n5 . ID:  <code>{db.get_top_likes()[4][0]} </code>-- Лайков: {db.get_top_likes()[4][1]}👍")
    
@dp.callback_query(F.data == 'activ')
async def activ(callback: types.CallbackQuery):  
    await callback.answer() 
    await callback.message.edit_text(text= f"Топ активности🏆⤵️\n\n🥇. ID: <code>{db.get_top_message_counts()[0][0]}</code> -- Сообщений: {db.get_top_message_counts()[0][1]}, Чатов: {db.get_top_message_counts()[0][2]}\n🥈. ID: <code>{db.get_top_message_counts()[1][0]}</code> -- Сообщений: {db.get_top_message_counts()[1][1]}, Чатов: {db.get_top_message_counts()[1][2]}\n🥉. ID: <code>{db.get_top_message_counts()[2][0]}</code> -- Сообщений: {db.get_top_message_counts()[2][1]}, Чатов: {db.get_top_message_counts()[2][2]}\n4 . ID:<code> {db.get_top_message_counts()[3][0]}</code> -- Сообщений: {db.get_top_message_counts()[3][1]}, Чатов: {db.get_top_message_counts()[3][2]}\n5 . ID:<code> {db.get_top_message_counts()[4][0]}</code> -- Сообщений: {db.get_top_message_counts()[4][1]}, Чатов: {db.get_top_message_counts()[4][2]}")
    
# # #################################################

@dp.callback_query(F.data == 'referal')
async def referal(callback: types.CallbackQuery):
    await callback.answer() 
    await callback.message.answer(text=f'<b>📬Наша реферальна система⤵️\n\nКак получить баллы💠:</b>\nВсе что вам нужно это что бы пользователь зарегистрировался по вашей <b>ссылке</b> и после этого вы получите <b>1 балл💠</b>')
    await callback.message.answer(f'https://t.me/anonimniy_chatik18_bot?start={callback.from_user.id}',)
    await callback.message.answer(f'Магазин где все эти баллы можно обменять ➡️  /shop')


@dp.callback_query(F.data == 'redact')
async def redact(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f'<b>ㅤПривет {callback.from_user.first_name}!\nㅤㅤㅤ↓ <em> Укажите ваш пол👰🏻‍♂️ </em>↓</b>', reply_markup= gender_kb)

# # #################################################

@dp.callback_query(F.data.in_(['boy', 'girl']))
async def redact(callback: types.CallbackQuery):
    if db.check_user(callback.message.chat.id):
        db.update_gender(callback.message.chat.id, callback.data)
    else:
        db.set_gender(callback.message.chat.id, callback.data)
    await callback.answer()
    await callback.message.edit_text(text=f'<b>↓ <em> Укажите ваш возраст😇 </em>↓</b> ',reply_markup=age_kb)

    
@dp.callback_query(F.data.in_(['True', 'False']))
async def redact(callback: types.CallbackQuery):
    global reffer_id
    if reffer_id:
        if db.get_age(callback.message.chat.id) == 0 or db.get_age(callback.message.chat.id) == '0':
            db.update_age(callback.message.chat.id, callback.data)
            await bot.send_message(chat_id=callback.message.chat.id,text=f'<b>Вы успешно зарегистрировались по ссылке друга😋) \n+3 реферальных балла🤤\n\n ↓<em>Меню📋</em>↓</b>', reply_markup= all_kb)
            db.update_reffer(reffer_id, db.get_reffer(reffer_id)[0], db.get_reffer(reffer_id)[1])
            db.update_reffer(callback.message.chat.id, -1 , 2)
            await bot.send_message(chat_id=reffer_id, text='<b>Пользователь зарегистрировался по вашей ссылке\n<em>+1 реферальный бал🤤</em>\nСпасибо за то что вы с нами💋)</b>')
            db.update_age(callback.message.chat.id, callback.data)
        else:
            if db.get_vip(callback.message.chat.id) != '0':
                db.update_age(callback.message.chat.id, callback.data)
                await callback.message.edit_text(f'<b>Видим что у вас есть 🏆VIP статус, изменить 👑VIP никнейм?⤵️</b> ',reply_markup=redakt_kb)
            else:
                db.update_age(callback.message.chat.id, callback.data)
                await callback.message.edit_text(text=f'<b>Вы успешно создали профиль⚙️✅</b> ')
                await callback.message.answer(text=f'<b><em>Главное меню📋⤵️</em></b> ',reply_markup=all_kb)

    elif db.get_vip(callback.message.chat.id) != '0':
        db.update_age(callback.message.chat.id, callback.data)
        await callback.message.edit_text(f'<b>Видим что у вас есть 🏆VIP статус, изменить 👑VIP никнейм?⤵️</b> ',reply_markup=redakt_kb)
    else:
        db.update_age(callback.message.chat.id, callback.data)
        await callback.message.edit_text(text=f'<b>Вы успешно создали профиль⚙️✅</b> ')
        await callback.message.answer(text=f'<b><em>Главное меню📋⤵️</em></b> ',reply_markup=all_kb)


@dp.callback_query(F.data.in_(['yes_name_redakt', 'no_name_redakt']))
async def shop_4(callback: types.CallbackQuery):
    global username
    if callback.data == 'yes_name_redakt':
        try:
            db.update_vip_name(callback.message.chat.id, f"@{username}")
        except:
            db.update_vip_name(callback.message.chat.id, f"Пользователь")
            await callback.message.answer(text=f'<b>К сожалению у вас в телеграме не указан ваш июзернейм , поэтому ваш никнейм - Пользователь\nЕсли вы всё же хотите использовать юзернейм телеграма , тогда создайте его и пройдите редактирование профиля в боте еще раз)</b>')
    else:
        db.update_vip_name(callback.message.chat.id,'Пользователь')
    await callback.message.edit_text(f'<b>Вы успешно редактировали профиль⚙️✅</b>')
    await callback.message.answer(text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb)
    
# # #################################################

@dp.callback_query(F.data.in_(['new_girl', 'new_boy']))
async def redact(callback: types.CallbackQuery): 
    if callback.data == 'new_girl':
        db.update_gender(callback.message.chat.id, 'girl')
    else:
        db.update_gender(callback.message.chat.id, 'boy')
    await callback.message.edit_text(text=f'<b>Вы успешно сменили пол на : {gender_dict[callback.data]}</b> ')
    

# # #################################################

@dp.callback_query(F.data == 'gift')
async def redact(callback: types.CallbackQuery):
    await callback.message.edit_text(text=f'<b>У вас на аккаунте <em><code>{db.get_reffer(callback.message.chat.id)[1]}</code></em> баллов💠\nВыбери сколько хочешь отправить баллов собеседнику⤵️</b> ', reply_markup= present_kb)
    
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
            await callback.message.delete()
            await callback.message.answer(f'<b>Ваш подарок в <em>3 балла💠 успешно отправлен!✅</em></b>')
            await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 3 балла💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>')
        else:
            await callback.message.delete()
            await callback.message.answer(f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>')
            

        
            
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
            await callback.message.delete()
            await callback.message.answer(f'<b>Ваш подарок в <em>10 баллов💠 успешно отправлен!✅</em></b>')
            await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 10 баллов💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>')
        else:
            await callback.message.delete()
            await callback.message.answer(f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>')
            
                
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
            await callback.message.delete()
            await callback.message.answer(f'<b>Ваш подарок в <em>20 баллов💠 успешно отправлен!✅</em></b>')
            await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 20 баллов💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>')
        else:
            await callback.message.delete()
            await callback.message.answer(f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>')
            
                
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
            await callback.message.delete()
            await callback.message.answer(f'<b>Ваш подарок в <em>30 баллов💠 успешно отправлен!✅</em></b>')
            await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 30 баллов💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>')
        else:
            await callback.message.delete()
            await callback.message.answer(f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>')
            
                
@dp.callback_query(F.data == 'buy')
async def redact(callback: types.CallbackQuery):
    global id_1, id_2
    if callback.message.chat.id == id_1:
        id = id_2    
    elif callback.message.chat.id == id_2:
        id = id_1
    await callback.message.answer(f'Что бы оплатить тапните <a href="https://donatello.to/anonimniy_chatik18">СЮДА💋</a>\n\n❗️❗️❗️Напоминаем о том что вам нужно вписать ID собеседника : <code>{id}</code>  в \'Имя\' на сайте',disable_web_page_preview=True, reply_markup=vip_bool_kb)

    

# # #################################################
@dp.callback_query(F.data == 'vip_access')
async def shop_1(callback: types.CallbackQuery): 
    await callback.message.delete()
    await callback.message.answer(f'Что бы оплатить тапните <a href="https://donatello.to/anonimniy_chatik18">СЮДА💋</a>\n\nНапоминаем о том что вам нужно вписать ваш ID: <code>{callback.message.chat.id}</code> или чужой ID для подарка в \'Имя\' на сайте',disable_web_page_preview=True, reply_markup=vip_bool_kb)



@dp.callback_query(F.data == 'yes_vip')
async def shop_1(callback: types.CallbackQuery): 

    vip = get_vip()
    if  vip != None:
             
        if int(callback.message.chat.id) == int(vip[1]):
            if vip[2] == 'UAH':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + int((int(vip[0]) * 2.18 / 2))))
            if vip[2] == 'RUB':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + int((int(vip[0]) / 2))))
                
            await callback.message.edit_text(text=f'<b>Вы успешно пополнили баланс баллов💠 : {db.get_reffer(vip[1])[1]}</b>')
            bot.send_message(callback.message.chat.id,text=f'<b>ㅤㅤ↓ <em> Главное меню📋 </em>↓</b>', reply_markup= all_kb)
        elif int(callback.message.chat.id) != int(vip[1]):
            if vip[2] == 'UAH':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + (int(vip[0]) * 2.18 / 2)))
            if vip[2] == 'RUB':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + (int(vip[0]) / 2)))
                
            await callback.message.edit_text(text=f'<b>Вы успешно сделали подарок другому пользователю!!!</b>')
            if db.get_active_chat(callback.message.chat.id):
                await callback.message.answer(text=f'<b>ㅤㅤ↓ <em> Главное меню📋 </em>↓</b>', reply_markup= all_kb)
            try:
                await bot.send_message(vip[1],text=f'<b>Вам сделал подарок другой пользователь!!!\n\nБаланс баллов💠 : {db.get_reffer(vip[1])[1]}</b>', reply_markup= all_kb)
            except:
                pass
    
        db.update_vip_char(get_donates()[3])
    else:
        await callback.message.edit_text(text=f'<b>Нам не пришла ваша оплата, если вы уверены что все сделали правильно, напишите <em>@bbtqqrl</em> о ошибке</b>')

@dp.callback_query(F.data == 'no_vip')
async def shop_1(callback: types.CallbackQuery): 
    await callback.message.delete()
    if not db.get_active_chat(callback.message.chat.id):
        await callback.message.answer(f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb)
# # #################################################


@dp.callback_query(F.data == 'shop_1')
async def shop_1(callback: types.CallbackQuery): 

    if db.get_reffer(callback.message.chat.id)[1] >= 3:
        await callback.message.edit_text(text=f'<b>Вы успешно cбросили дизлайки🤫)</b>')
        await callback.message.answer(text=f'<b>ㅤㅤ↓ <em> Главное меню📋 </em>↓</b>', reply_markup= all_kb)
        db.update_dislike(-1, callback.message.chat.id)
        db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 4)

    else:
        await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>')

@dp.callback_query(F.data == 'shop_2')
async def shop_2(callback: types.CallbackQuery):
    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 10:
            await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 на 1 день\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привелегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>', reply_markup=bool_kb)
            db.update_vip(callback.message.chat.id,datetime.now() + timedelta(days=1))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 11)      
        
        else:
            await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>')
    else:
        await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>')

            

@dp.callback_query(F.data == 'shop_3')
async def shop_3(callback: types.CallbackQuery):
    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 20:
            await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 на 3 дня\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привелегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>', reply_markup=bool_kb)
            db.update_vip(callback.message.chat.id,datetime.now() + timedelta(days=3))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 21)      
        
        else:
            await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>')
    else:
        await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>')
    
@dp.callback_query(F.data == 'shop_4')
async def shop_4(callback: types.CallbackQuery):
    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 30:
            await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 на 6 дней\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привелегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>', reply_markup=bool_kb)
            db.update_vip(callback.message.chat.id,datetime.now() + timedelta(days=6))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 31)      
        
        else:
            await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>')
    else:
        await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>')
        
@dp.callback_query(F.data == 'shop_5')
async def shop_4(callback: types.CallbackQuery):
    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 200:
            await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 НАВСЕГДА\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привелегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>', reply_markup=bool_kb)
            db.update_vip(callback.message.chat.id,datetime.now() + relativedelta(years=10))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 201)      
        
        else:
            await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>')
    else:
        await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>')

# # #################################################
@dp.callback_query(F.data.in_(['yes_name', 'no_name']))
async def shop_4(callback: types.CallbackQuery):
    global username
    if callback.data == 'yes_name':
        db.update_vip_name(callback.message.chat.id, f"@{username}")
    else:
        db.update_vip_name(callback.message.chat.id, 'Пользователь')
    await callback.message.edit_text(text='<b>Супер👏 , теперь ваши собеседники будут видеть такой текст⤵️</b>')
    await callback.message.answer(f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(callback.message.chat.id)}\n\nЛайков 👍 : {db.get_like(callback.message.chat.id)}\nДизлайков 👎 : {db.get_dislike(callback.message.chat.id)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>')
    await callback.message.answer(f'<b>Ещё раз спасибо вам большое💋!</b>')
    await callback.message.answer(text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>', reply_markup=all_kb)
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