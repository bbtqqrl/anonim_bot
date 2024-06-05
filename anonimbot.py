import aiogram
import requests
from aiogram import types
from aiogram.utils import exceptions
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# _______________________/////////_______________________________
# _______________________/////////_______________________________
# _______________________/////////_____________________________

class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread = False)   
        self.cursor = self.connection.cursor()
    
    def del_user(self, id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `users` WHERE `chat_id` = ?", (id[0],))

    def add_queue(self, chat_id, gender, age):
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` (`chat_id`, `gender`, `age`) VALUES (?, ?, ?)", (chat_id, gender, age))
        
    def add_queue_gender(self, chat_id, gender, age, search_gender):
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` (`chat_id`, `gender`, `age`, `search_gender`) VALUES (?, ?, ?, ?)", (chat_id, gender, age, search_gender))
        
    def add_queue_age(self, chat_id, gender, age, search_gender, search_age):
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` (`chat_id`, `gender`, `age`, `search_gender`, `search_age`) VALUES (?, ?, ?, ?, ?)", (chat_id, gender, age, search_gender, search_age))

    def del_queue(self, chat_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `queue` WHERE `chat_id`= ? ", (chat_id,))
        
    def del_chat(self, id_chat):
        with self.connection:
            return self.cursor.execute("DELETE FROM `chats` WHERE `id`= ? ", (id_chat,))
           
    def get_chat(self, mygender, myage):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `queue` WHERE (`search_gender` = ? OR `search_gender` IS NULL) AND (`search_age` = ? OR `search_age` IS NULL)", (mygender, myage,)).fetchmany(1)
            if (bool(len(chat))):
                for row in chat:
                    return [row[1], row[2]]
            else:
                return [0]
    
    
    def create_chat(self, chat_1, chat_2):
        with self.connection:
            if chat_2 != 0:
                self.cursor.execute("DELETE FROM `queue` WHERE `chat_id`= ? ", (chat_2,))
                self.cursor.execute("INSERT INTO `chats`(`chat_1`, `chat_2`, `date`) VALUES (?,?,?)", (chat_1, chat_2, datetime.now()))
                return True
            else:
                return False
            
    def check_queue(self, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(*) FROM `queue` WHERE `chat_id` = ?", (chat_id,)).fetchone()[0] < 1

    def get_active_chat(self, chat_id):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_1` = ?", (chat_id,))
            id_chat = 0
            for row in chat:
                id_chat = row[0]
                chat_info = [row[0], row[2]]
            if id_chat == 0:
                chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_2` = ?", (chat_id,))
                for row in chat:
                    id_chat = row[0]
                    chat_info = [row[0], row[1]]
                if id_chat == 0:
                    return False
                else:
                    return chat_info
            else:
                return chat_info

    def check_user(self, chat_id):
        with self.connection:
            return bool(len(self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)))
        
    def get_all_user(self):
        with self.connection:
            self.cursor.execute('SELECT `chat_id` FROM `users`')
            return self.cursor.fetchall()
        
    def get_all_active_chat(self, chat_id):
        with self.connection:
            try:
                chat= self.cursor.execute("SELECT `chat_1`, `chat_2` FROM `chats` WHERE `chat_1` = ?" , (chat_id,))
                for row in chat:
                    return row
            except:
                chat = self.cursor.execute("SELECT `chat_1`, `chat_2` FROM `chats` WHERE `chat_2` = ?" , (chat_id,))
                for row in chat:
                    return row
    
    def check_chat(self, chat_id):
        with self.connection:
            chat= self.cursor.execute("SELECT `chat_1`, `chat_2` FROM `chats` WHERE `chat_1` = ?" , (chat_id,))
            for row in chat:
                if int(row[0]) == chat_id:
                    return True
            chat = self.cursor.execute("SELECT `chat_1`, `chat_2` FROM `chats` WHERE `chat_2` = ?" , (chat_id,))
            for row in chat:
                if int(row[1]) == chat_id:
                    return True
            return False
                
# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

    def get_date(self, chat_id):
        with self.connection:
            chat = self.cursor.execute("SELECT `date` FROM `chats` WHERE `chat_1` = ? OR `chat_2` = ?", (chat_id,chat_id))
            for char in chat:
                return char[0]




# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№
            

# стать гендер 
    def set_gender(self, chat_id, gender):
        with self.connection:
            if bool(len(self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1))) == False:
                self.cursor.execute("INSERT INTO `users` (`chat_id`, `gender`) VALUES (?,?)", (chat_id,gender))
                return True
            else:
                return False
                
                
                
    def get_gender(self, chat_id):
        with self.connection:
            user = self.cursor.execute("SELECT * FROM `users` WHERE `chat_id` = ?", (chat_id,)).fetchmany(1)
            if bool(len(user)):
                for row in user:
                    return row[2]
            else:
                return False
            
    def get_gender_chat(self, mygender,myage, gender):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `queue` WHERE (`search_gender` = ? OR `search_gender` IS NULL) AND (`search_age` = ? OR `search_age` IS NULL) AND `gender` = ?", (mygender, myage, gender,)).fetchmany(1)
            if bool(len(chat)):
                for row in chat:
                    return [row[1], row[2]]
            else:
                return [0]
            
    def update_gender(self,chat_id, gender):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `gender`=? WHERE `chat_id`=?", (gender, chat_id))
        
# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№


# Кількість чатів і повідомленнь
    def add_mess_chat(self, chat_id, count_mess, count_chat):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `count_chat`=?, `count_messages`=? WHERE `chat_id`=?", (count_chat, count_mess, chat_id))
    
    def show_num_chat(self, chat_id):
        with self.connection:
            chat =self.cursor.execute("SELECT `count_chat` FROM `users` WHERE `chat_id` = ?", (chat_id,))
            for row in chat:
                return row[0]
            
    def show_num_mess(self, chat_id):
        with self.connection:    
            mes = self.cursor.execute("SELECT `count_messages` FROM `users` WHERE `chat_id` = ?", (chat_id,))
            for row in mes:
                return row[0]
            
    def get_top_message_counts(self):
        with self.connection:
            messages = self.cursor.execute("SELECT `chat_id`, `count_messages`, `count_chat` FROM `users` ORDER BY `count_messages` DESC LIMIT 5")
            top_counts = []
            for row in messages:
                top_counts.append(row)
            return top_counts


# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№
    
    
# 
    def update_like(self, like, chat_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `like`=? WHERE `chat_id`=?", (like + 1, chat_id))       
    
    def update_dislike(self, dislike, chat_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `dislike`=? WHERE `chat_id`=?", (dislike + 1, chat_id))
        
    def get_like(self, chat_id):
        with self.connection:
            chat =self.cursor.execute("SELECT `like` FROM `users` WHERE `chat_id` = ?", (chat_id,))
            for row in chat:
                return row[0]
               
    def get_dislike(self, chat_id):
        with self.connection:
            chat =self.cursor.execute("SELECT `dislike` FROM `users` WHERE `chat_id` = ?", (chat_id,))
            for row in chat:
                return row[0]     
    
    def straf_update_dislike(self, dislike, chat_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `dislike`=? WHERE `chat_id`=?", (dislike + 5, chat_id))
    
    def get_top_likes(self):
        with self.connection:
            chat = self.cursor.execute("SELECT `chat_id`, `like` FROM `users` ORDER BY `like` DESC LIMIT 5")
            top_likes = []
            for row in chat:
                top_likes.append(row)
            return top_likes
        
    def get_report(self, chat_id):
        with self.connection:
            chat =self.cursor.execute("SELECT `report` FROM `users` WHERE `chat_id` = ?", (chat_id,))
            for row in chat:
                return row[0]     
            
    def update_report(self, report, chat_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `report`=? WHERE `chat_id`=?", (report + 1, chat_id))

# ############################################################################################################################################
    def get_reffer(self, chat_id):
        with self.connection:
            result = self.cursor.execute("SELECT `reffer_count`, `reffer_point` FROM `users` WHERE `chat_id` = ?", (chat_id,))
            char = []
            for row in result:
                char.append(row[0])
                char.append(row[1])
            return char

       
    def update_reffer(self,chat_id, reffer_count, reffer_point):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `reffer_count`=?, `reffer_point`=? WHERE `chat_id`=?", (reffer_count +1 , reffer_point + 1, chat_id))

# ############################################################################################################################################

    def get_vip(self, chat_id):
        with self.connection:
            result = self.cursor.execute("SELECT `vip` FROM `users` WHERE `chat_id` = ?", (chat_id,))
            for row in result:
                return row[0]

       
    def update_vip(self,chat_id, time):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `vip`=? WHERE `chat_id`=?", (time, chat_id))  


    def get_vip_name(self, chat_id):
        with self.connection:
            result = self.cursor.execute("SELECT `vip_name` FROM `users` WHERE `chat_id` = ?", (chat_id,))
            for row in result:
                return row[0]

       
    def update_vip_name(self,chat_id, name):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `vip_name`=? WHERE `chat_id`=?", (name, chat_id))  

# ############################################################################################################################################

    def get_age(self, chat_id):
        with self.connection:
            result = self.cursor.execute("SELECT `age` FROM `users` WHERE `chat_id` = ?", (chat_id,))
            for row in result:
                return row[0]

       
    def update_age(self,chat_id, age):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `age`=? WHERE `chat_id`=?", (age, chat_id))  

    def get_age_chat(self,mygender, myage, gender, age):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `queue` WHERE (`search_gender` = ? OR `search_gender` IS NULL) AND (`search_age` = ? OR `search_age` IS NULL) AND `gender` = ? AND `age` = ?", (mygender, myage, gender, age)).fetchmany(1)
            if bool(len(chat)):
                for row in chat:
                    return row[1]
            else:
                return 0

# ############################################################################################################################################
    def update_vip_char(self,vip):
        with self.connection:
            return self.cursor.execute("UPDATE `vip` SET `char`=?", (vip,))  

    def get_vip_char(self):
        with self.connection:
            char = self.cursor.execute("SELECT `char` FROM `vip`")
            for row in char:
                return row[0]


    def get_activ(self):
        with self.connection:
                chat = self.cursor.execute('SELECT COUNT(*) FROM `users`')
                for char in chat:
                    return char[0]
# ############################################################################################################################################




# ____________тут більшість взіх змінн та частково кнопки______
# ############################################################################################################################################


db = Database('projects/db.db')

gender_dict = {
    'boy': 'Мужской🤵',
    'girl': 'Женский👸'
}

age_dict = {
    'True': 'Больше 18🔞🍓',
    'False': 'Меньше 18🫣💋'
}


bot = aiogram.Bot('6060478130:AAEXsnJL7QLvI-aC-gYWDCw98y3wJLnwUjM')
dp_main = aiogram.Dispatcher(bot)

kb = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
all_kb = aiogram.types.KeyboardButton('Парень🔎🤵'), aiogram.types.KeyboardButton('👥Рандом'), aiogram.types.KeyboardButton('Девушка🔎👸')
vip_kb = aiogram.types.KeyboardButton('Профиль📖'), aiogram.types.KeyboardButton('VIP СТАТУС💎'), aiogram.types.KeyboardButton('Обмен → 💠')
menu_kb = aiogram.types.KeyboardButton('Главное меню📋')
chat_kb = [aiogram.types.KeyboardButton('Сделать подарок🎁'), aiogram.types.KeyboardButton('/stop')]
count_mess_1, count_mess_2, count_chat_1, count_chat_2, id_1, id_2, username, marker = 0, 0, 0, 0, 0, 0, 0, False
reffer_id = 0


ikb = aiogram.types.InlineKeyboardMarkup(row_width= 2, one_time_keyboard=True)
# all_button = [aiogram.types.InlineKeyboardButton(text='👥Поиск собеседника', callback_data='search'), aiogram.types.InlineKeyboardButton(text='Мой профиль📖', callback_data='profile')]
# vip_button = aiogram.types.InlineKeyboardButton(text = '💎VIP СТАТУС💎', callback_data= 'vip')

gift_button = [aiogram.types.InlineKeyboardButton(text='Купить баллы💠', callback_data='buy'), 
               aiogram.types.InlineKeyboardButton(text='Подарить баллы🎁', callback_data='gift')]

present_button = [aiogram.types.InlineKeyboardButton(text='3 балла💠', callback_data='gift_1'), 
                 aiogram.types.InlineKeyboardButton(text='10 баллов💠', callback_data='gift_2'),
                 aiogram.types.InlineKeyboardButton(text='20 баллов💠', callback_data='gift_3'),
                 aiogram.types.InlineKeyboardButton(text=' 30 баллов💠', callback_data='gift_4')]

top_button = [aiogram.types.InlineKeyboardButton(text='🏆Топ активности🥊', callback_data='activ'), 
               aiogram.types.InlineKeyboardButton(text='🏆Топ кармы🎭', callback_data='karma')]

like_button = [aiogram.types.InlineKeyboardButton(text='👍', callback_data='like'), 
               aiogram.types.InlineKeyboardButton(text='👎', callback_data='dislike')]

report_button = aiogram.types.InlineKeyboardButton(text='Жалоба⚠️', callback_data='report')

profile_button = [aiogram.types.InlineKeyboardButton(text='⚙️Редактировать профиль', callback_data='redact'),
                  aiogram.types.InlineKeyboardButton(text='📬Реферальная система', callback_data='referal'),
                  aiogram.types.InlineKeyboardButton(text='🥇Топы участников', callback_data='top')]

gender_button = [aiogram.types.InlineKeyboardButton(text='Парень🤵', callback_data='boy'), 
                 aiogram.types.InlineKeyboardButton(text='Девушка👸', callback_data='girl')]

shop_button = [aiogram.types.InlineKeyboardButton(text='Сброс дизлайков😉 — 3 балла💠', callback_data='shop_1'), 
                 aiogram.types.InlineKeyboardButton(text='1 день VIP статуса🏆 — 10 баллов💠', callback_data='shop_2'),
                 aiogram.types.InlineKeyboardButton(text='3 дня VIP статуса🏆 — 20 баллов💠', callback_data='shop_3'),
                 aiogram.types.InlineKeyboardButton(text='6 дней VIP статуса🏆 — 30 баллов💠', callback_data='shop_4'),
                 aiogram.types.InlineKeyboardButton(text='VIP статус👑 НАВСЕГДА — 200 баллов💠', callback_data='shop_5')]

anon_button = aiogram.types.InlineKeyboardButton(text= '+3 балла💠' , url = 'https://t.me/anonimniy_chatik18_bot?start=1135699139')

fusion_button = aiogram.types.InlineKeyboardButton(text= '+20 балів💠' , url = 'https://t.me/fusion_sh0p_bot?start=1135699139')


vip_button = aiogram.types.InlineKeyboardButton(text='КУПИТЬ БАЛЛЫ💠', callback_data='vip_access')

vip_bool_button = [aiogram.types.InlineKeyboardButton(text='Я оплатил✅', callback_data='yes_vip'), 
                 aiogram.types.InlineKeyboardButton(text='Отменить❌', callback_data='no_vip')]

age_button = [aiogram.types.InlineKeyboardButton(text='Больше 18🔞🍓', callback_data='True'), 
                 aiogram.types.InlineKeyboardButton(text='Меньше 18🫣💋', callback_data='False')]

search_boy_button = [aiogram.types.InlineKeyboardButton(text='Больше 18🔞🍓', callback_data='boy_True'), 
                 aiogram.types.InlineKeyboardButton(text='Меньше 18🫣💋', callback_data='boy_False')]

search_girl_button = [aiogram.types.InlineKeyboardButton(text='Больше 18🔞🍓', callback_data='girl_True'), 
                 aiogram.types.InlineKeyboardButton(text='Меньше 18🫣💋', callback_data='girl_False')]

search_gender_button = [aiogram.types.InlineKeyboardButton(text='Парень🔎🤵', callback_data='search_boy'), 
                 aiogram.types.InlineKeyboardButton(text='Девушка🔎👸', callback_data='search_girl')]

bool_button = [aiogram.types.InlineKeyboardButton(text='ДА✅', callback_data='yes_name'), 
                 aiogram.types.InlineKeyboardButton(text='НЕТ❌', callback_data='no_name')]

redakt_button = [aiogram.types.InlineKeyboardButton(text='ДА✅', callback_data='yes_name_redakt'), 
                 aiogram.types.InlineKeyboardButton(text='НЕТ❌', callback_data='no_name_redakt')]
# ############################################################################################################################################
# ############################################################################################################################################



        
# функцыонал гендеру, меню ы тд_____________________________________
# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp_main.message_handler(text='Профиль📖')
async def profile(message: types.Message):
    global username
    username = message.from_user.first_name
    ikb.inline_keyboard.clear()
    ikb.add(profile_button[0]).add(profile_button[1]).add(profile_button[2])
    if db.get_vip(message.chat.id) == '0':
        vip = 'Отсутсвует'
    else:
        vip = 'Присутсвует'
        
    await bot.send_message(chat_id=message.chat.id,text=f'<b>Ваш профиль👾 \n\n#️⃣ ID: <em><code>{message.chat.id}</code></em> \n👫 Пол:  <em>{gender_dict[db.get_gender(message.chat.id)]}</em>\n😇Возраст: <em>{age_dict[db.get_age(message.chat.id)]}\n\n🏆VIP статус: {vip}\n👑VIP никнейм: {db.get_vip_name(message.chat.id)}\n\n💬Сообщений : {db.show_num_mess(message.chat.id)}\n💌Чатов : {db.show_num_chat(message.chat.id)}     </em> \n\n🎭Ваша карма⤵️\n<em>Лайков 👍 : {db.get_like(message.chat.id)}\nДизлайков 👎 : {db.get_dislike(message.chat.id)}</em>\n\n💼Реф. профиль⤵️<em>\nПриглашено юзеров👥: {db.get_reffer(message.chat.id)[0]}\nРеферальных баллов💠: {db.get_reffer(message.chat.id)[1]}</em></b>'
                           ,parse_mode='HTML',
                           reply_markup= ikb)

# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp_main.message_handler(text='VIP СТАТУС💎')
async def vip(message: types.Message):
    global username
    username = message.from_user.first_name
    ikb.inline_keyboard.clear()
    ikb.add(vip_button)
    with open('projects/vip_photo', 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id, photo= photo, caption='Преимущества<b> VIP статуса👑⤵️</b>\n\n<em>1️⃣. <b>БАН</b> спам рекламы🛑\n2️⃣. Никаких ограничений🤑\n3️⃣. Всегда <b>ПЕРВЫЙ</b> в поиске!!!\n4️⃣. Поиск по <b>возрасту</b>🤫(/vip_search)...\n5️⃣. <b>ВСЕ</b> будут видеть твой статус💠\n6️⃣. Ты сможешь создать свой ник🔥\n7️⃣. Возможность <b>ПОЖАЛОВАТЬСЯ</b> на плохого собеседника🚫\n🎱. И в конце концов ты сможешь получить VIP <b>БЕСПЛАТНО</b>❤️‍🔥\n\nДа и ты получишь возможность увидеть себя в <b>топе VIP🏆 активности</b>\n\nЛюбим каждого💕💕💕</em>',parse_mode='HTML')
    await bot.send_message(message.chat.id, text= f'<b><em>VIP🏆 статус</em> покупается за баллы в /shop , а здесь можно купить балы по курсу⤵️\n\n1 балл💠 - <em>2 рубля или 0,92 гривны\n\n⚠️⚠️ВНИМАНИЕ⚠️⚠️</em>\nПри покупке баллов вам нужно вставить ваш ID или ID пользователя которому вы хотите сделать подарок в поле "Имя" или "Ім`я"  . Тогда покупка будет зарегистрирована и вам придет уведомление/)\n\nВаш ID - <code>{message.chat.id}</code>⚠️\n\n<em>Любим каждого💕💕💕</em></b>',parse_mode='HTML', reply_markup=ikb)
# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp_main.message_handler(text='Главное меню📋')
async def menu(message: types.Message):
    kb.keyboard.clear()
    kb.add(*all_kb).add(*vip_kb)
    await message.answer(f'<b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML',reply_markup=kb)

# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@dp_main.message_handler(text= 'Обмен → 💠')
async def command_start_search(message: types.Message):
    
    global username
    username = message.from_user.first_name
    ikb.inline_keyboard.clear()
    ikb.add(shop_button[0]).add(shop_button[1]).add(shop_button[2]).add(shop_button[3]).add(shop_button[4])

    await message.answer(f'<b>Наш магазин для обмена баллов💠⤵️\n\nВаших баллов:   {db.get_reffer(message.chat.id)[1]}💎\n\n А как получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em></b>',parse_mode='HTML',reply_markup=ikb)
    
# ############################################################################################################################################
# ############################################################################################################################################




# _______________команди і функції_______________
# ############################################################################################################################################

@dp_main.message_handler(commands='stats_bbtqqrl')
async def stop_search(message: types.Message):
    await message.answer(f'Кількість людей: {db.get_activ()}')      




@dp_main.message_handler(commands= 'start')
async def start(message: types.Message):
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
            kb.keyboard.clear()
            kb.add(*all_kb)
            kb.add(*vip_kb)
            await bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEI4-tkV4lOb3MNjmu-FuZ6TBl1daqalQACZAEAAntOKhAOzIvWIO0fji8E')
            await bot.send_message(message.chat.id, text=f'<b>Снова здраствуй в нашем анонимном чат боте🤗 \n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
        else:
            ikb.inline_keyboard.clear()
            ikb.add(*gender_button)
            await message.answer(f'<b>Привет пользователь!\nУкажите ваш пол👰🏻‍♂️</b>', parse_mode='HTML', reply_markup=ikb)

    else:
        kb.keyboard.clear()
        kb.add(*chat_kb)
        await bot.send_message(message.chat.id,f'<b>Вы не можете отправлять команды в чате, что бы его остановить используйте команду /stop</b>',parse_mode='HTML', reply_markup= kb)      




@dp_main.message_handler(commands='stop_search')
async def stop_search(message: types.Message):
    if not db.get_active_chat(message.chat.id):
        global last_start_mes
        kb.keyboard.clear()
        kb.add(*all_kb)
        kb.add(*vip_kb)
        
        if db.del_queue(message.chat.id):
            try:
                await bot.delete_message(message.chat.id, last_start_mes.message_id)
                last_start_mes = None
            except:
                True
            await message.answer(f'<b>ㅤВы остановили поиск😣\nㅤㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML',reply_markup=kb)
            
        elif not db.del_queue(message.chat.id):
            await message.answer(f'<b>ㅤВы не начали поиск поиск😣\nㅤㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML',reply_markup=kb)           
    else:
        kb.keyboard.clear()
        kb.add(*chat_kb)
        await bot.send_message(message.chat.id,f'<b>Вы не можете отправлять команды в активном чате, что бы его остановить используйте команду /stop</b>',parse_mode='HTML', reply_markup= kb)    
        
        
@dp_main.message_handler(commands='porn')
async def start(message: aiogram.types.Message):
    with open(r'photo_2023-08-07_11-45-20.jpg', 'rb') as photo:
        ikb.inline_keyboard.clear()
        ikb.add(anon_button)
        await bot.send_photo(message.chat.id,photo,caption= f'<b>У нас есть кое что для вас💋!</b>\n\nОткройте для себя захватывающий мир общения вместе с нашим ботом💌\n\nНаша система обеспечивает удобный и безопасный способ общения, с единственной среди конкурентов системой баллов💎\n\n<b><em>Присоединяйтесь сегодня и получи 3 балла💠 на свой счёт💼</em></b>', parse_mode= 'HTML', reply_markup= ikb)

     
@dp_main.message_handler(commands='fusion')
async def start(message: aiogram.types.Message):
    if message.chat.id == 1135699139:
        count = 0
        for id in db.get_all_user():
            try:
                ikb.inline_keyboard.clear()
                ikb.add(fusion_button)
                with open(r'projects/doc_2024-04-19_14-26-02.mp4', 'rb') as gif:
                    await bot.send_animation(id[0],gif,caption= f'<b>Маємо щось особливе для вас! 💋</b>\n\nВідкрийте захоплюючий світ шопінгу разом з нашим ботом 💌\n\nНаша система надає зручний та безпечний спосіб покупки одягу, з унікальною системою балів серед конкурентів 💎\n\n<b>Приєднуйтесь сьогодні та <em>отримайте 20 балів 💠 </em>на свій рахунок 💼</b>', parse_mode= 'HTML', reply_markup= ikb)
            except exceptions.BotBlocked:
                db.del_user(id)
                count+=1
            except:
                db.del_user(id)
        await bot.send_message('1135699139',f"загальна кількість людей - {db.get_activ()}\nкількість заблоканих акків - {count}")

   
@dp_main.message_handler(commands='stop')
async def stop_chat(message: types.Message):
    global count_mess_1 ,count_chat_1, count_mess_2, count_chat_2, id_1, id_2
    if db.get_active_chat(message.chat.id):        
        try:
            kb.keyboard.clear()
            kb.add(menu_kb)

            
            if id_1 == message.chat.id: 
                ikb.inline_keyboard.clear()
                ikb.add(*like_button)  
                if db.get_vip(id_2) != '0':
                    ikb.add(report_button)
                await bot.send_message(chat_id= id_2 ,text=f'<b>Ваш собеседник закончил диалог🤧</b>',parse_mode='HTML', reply_markup=kb)
                await bot.send_message(chat_id= id_2 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>',parse_mode='HTML', reply_markup= ikb)
                ikb.inline_keyboard.clear()
                ikb.add(*like_button)                
                if db.get_vip(message.chat.id) != '0':
                    ikb.add(report_button)
                await bot.send_message(chat_id= id_1  ,text=f'<b>Вы закончили диалог🤧</b>',parse_mode='HTML', reply_markup= kb)
                await bot.send_message(chat_id= id_1 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>',parse_mode='HTML', reply_markup= ikb)
                db.add_mess_chat(message.chat.id, count_mess_2, count_chat_2 + 1)
                db.add_mess_chat(db.get_active_chat(message.chat.id)[1], count_mess_1, count_chat_1 + 1)  
            elif id_2 == message.chat.id:
                ikb.inline_keyboard.clear()
                ikb.add(*like_button)
                if db.get_vip(id_1) != '0':
                    ikb.add(report_button)
                await bot.send_message(chat_id= id_1 ,text=f'<b>Ваш собеседник закончил диалог🤧</b>',parse_mode='HTML', reply_markup=kb)
                await bot.send_message(chat_id= id_1 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>',parse_mode='HTML', reply_markup= ikb)
                ikb.inline_keyboard.clear()
                ikb.add(*like_button)
                if db.get_vip(message.chat.id) != '0':
                    ikb.add(report_button)
                await bot.send_message(chat_id= id_2  ,text=f'<b>Вы закончили диалог🤧</b>',parse_mode='HTML', reply_markup= kb)
                await bot.send_message(chat_id= id_2 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>',parse_mode='HTML', reply_markup= ikb)
                db.add_mess_chat(db.get_active_chat(message.chat.id)[1], count_mess_2, count_chat_2 + 1)
                db.add_mess_chat(message.chat.id, count_mess_1, count_chat_1 + 1) 

            db.del_chat(db.get_active_chat(message.chat.id)[0])
            
        except:
            
            kb.keyboard.clear()
            kb.add(*all_kb)
            kb.add(*vip_kb)
            
            await bot.send_message(chat_id=message.chat.id,text=f'<b>Вы не начали чат☹️! \n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)

    else:
        kb.keyboard.clear()
        kb.add(*all_kb)
        kb.add(*vip_kb)
        
        await bot.send_message(chat_id=message.chat.id,text=f'<b>Вы не начали чат☹️! \n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)


@dp_main.message_handler(commands='alert_text')
async def start(message: aiogram.types.Message):
    global marker
    if message.chat.id == 1135699139:
        marker = 'alert_text'
    
@dp_main.message_handler(commands='alert_photo')
async def start(message: aiogram.types.Message):
    global marker
    if message.chat.id == 135699139:
        marker = 'alert_photo'
        
@dp_main.message_handler(commands='menu')
async def command_start_search(message: types.Message):
    if not db.get_active_chat(message.chat.id):
        if not check_vip(message.chat.id):
            kb.keyboard.clear()
            kb.add(*all_kb).add(*vip_kb)
            await bot.send_message(message.chat.id, text= '<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>', parse_mode='HTML')
            return await bot.send_message(message.chat.id,text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>',parse_mode='HTML', reply_markup=kb)
        else:
            pass
        try:
            db.del_chat(message.chat.id)
        except:
            pass
        kb.keyboard.clear()
        kb.add(*all_kb)
        kb.add(*vip_kb)
        await message.answer(f'<b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML',reply_markup=kb)
    else:
        kb.keyboard.clear()
        kb.add(*chat_kb)
        await bot.send_message(message.chat.id,f'<b>Вы не можете отправлять команды в чате, что бы его остановить используйте команду /stop</b>',parse_mode='HTML', reply_markup= kb)  

@dp_main.message_handler(commands='vip')
async def vip(message: types.Message):
    if not db.get_active_chat(message.chat.id):
        global username
        username = message.from_user.first_name
        ikb.inline_keyboard.clear()
        ikb.add(vip_button)
        with open('C:\\Users\\Maks\\.ipython\\profile_default\\vip_photo.png', 'rb') as photo:
            await bot.send_photo(chat_id=message.chat.id, photo= photo, caption='Преимущества<b> VIP статуса👑⤵️</b>\n\n<em>1️⃣. <b>БАН</b> спам рекламы🛑\n2️⃣. Никаких ограничений🤑\n3️⃣. Всегда <b>ПЕРВЫЙ</b> в поиске!!!\n4️⃣. Поиск по <b>возрасту</b>🤫(/vip_search)...\n5️⃣. <b>ВСЕ</b> будут видеть твой статус💠\n6️⃣. Ты сможешь создать свой ник🔥\n7️⃣. Возможность <b>ПОЖАЛОВАТЬСЯ</b> на плохого собеседника🚫\n🎱. И в конце концов ты сможешь получить VIP <b>БЕСПЛАТНО</b>❤️‍🔥\n\nДа и ты получишь возможность увидеть себя в <b>топе VIP🏆 активности</b>\n\nЛюбим каждого💕💕💕</em>',parse_mode='HTML')
        await bot.send_message(message.chat.id, text= f'<b><em>VIP🏆 статус</em> покупается за баллы в /shop , а здесь можно купить балы по курсу⤵️\n\n1 балл💠 - <em>2 рубля или 0,92 гривны\n\n⚠️⚠️ВНИМАНИЕ⚠️⚠️</em>\nПри покупке баллов вам нужно вставить ваш ID или ID пользователя которому вы хотите сделать подарок в поле "Имя" или "Ім`я"  . Тогда покупка будет зарегистрирована и вам придет уведомление/)\n\nВаш ID - <code>{message.chat.id}</code>⚠️\n\n<em>Любим каждого💕💕💕</em></b>',parse_mode='HTML', reply_markup=ikb)
    else:
        kb.keyboard.clear()
        kb.add(*chat_kb)
        await bot.send_message(message.chat.id,f'<b>Вы не можете отправлять команды в чате, что бы его остановить используйте команду /stop</b>',parse_mode='HTML', reply_markup= kb)  


@dp_main.message_handler(commands='shop')
async def shop(message: types.Message):
    if not db.get_active_chat(message.chat.id):
        ikb.inline_keyboard.clear()
        ikb.add(shop_button[0]).add(shop_button[1]).add(shop_button[2]).add(shop_button[3]).add(shop_button[4])
        await message.answer(f'<b>\nНаш магазин для обмена баллов💠⤵️\n\n А как получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em></b>',parse_mode='HTML',reply_markup=ikb)
    else:
        kb.keyboard.clear()
        kb.add(*chat_kb)
        await bot.send_message(message.chat.id,f'<b>Вы не можете отправлять команды в чате, что бы его остановить используйте команду /stop</b>',parse_mode='HTML', reply_markup= kb)         
            
            
@dp_main.message_handler(commands='vip_search')
async def command_start_search(message: types.Message): 
    if not db.get_active_chat(message.chat.id):
        global username
        if not check_vip(message.chat.id):
            kb.keyboard.clear()
            kb.add(*all_kb).add(*vip_kb)
            await bot.send_message(message.chat.id, text= '<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>', parse_mode='HTML')
            return await bot.send_message(message.chat.id,text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>',parse_mode='HTML', reply_markup=kb) 
        
        if db.get_vip(message.chat.id) != '0':
            ikb.inline_keyboard.clear()
            ikb.add(*search_gender_button)
            await bot.send_message(message.chat.id,f'<b>Снова здраствуй 🏆VIP пользователь⤵️\nНикнейм: {db.get_vip_name(message.chat.id)}\n\n👑Кого искать👥?</b>',parse_mode='HTML', reply_markup= ikb)
        elif db.get_vip(message.chat.id) == '0':
            username = message.from_user.first_name
            ikb.inline_keyboard.clear()
            ikb.add(vip_button)
            with open('C:\\Users\\Maks\\.ipython\\profile_default\\vip_photo.png', 'rb') as photo:
                await bot.send_photo(chat_id=message.chat.id, photo= photo, caption='Преимущества<b> VIP статуса👑⤵️</b>\n\n<em>1️⃣. <b>БАН</b> спам рекламы🛑\n2️⃣. Никаких ограничений🤑\n3️⃣. Всегда <b>ПЕРВЫЙ</b> в поиске!!!\n4️⃣. Поиск по <b>возрасту</b>🤫(/vip_search)...\n5️⃣. <b>ВСЕ</b> будут видеть твой статус💠\n6️⃣. Ты сможешь создать свой ник🔥\n7️⃣. Возможность <b>ПОЖАЛОВАТЬСЯ</b> на плохого собеседника🚫\n🎱. И в конце концов ты сможешь получить VIP <b>БЕСПЛАТНО</b>❤️‍🔥\n\nДа и ты получишь возможность увидеть себя в <b>топе VIP🏆 активности</b>\n\nЛюбим каждого💕💕💕</em>',parse_mode='HTML')
            await bot.send_message(message.chat.id, text= f'<b><em>VIP🏆 статус</em> покупается за баллы в /shop , а здесь можно купить балы по курсу⤵️\n\n1 балл💠 - <em>2 рубля или 0,92 гривны\n\n⚠️⚠️ВНИМАНИЕ⚠️⚠️</em>\nПри покупке баллов вам нужно вставить ваш ID или ID пользователя которому вы хотите сделать подарок в поле "Имя" или "Ім`я"  . Тогда покупка будет зарегистрирована и вам придет уведомление/)\n\nВаш ID - <code>{message.chat.id}</code>⚠️\n\n<em>Любим каждого💕💕💕</em></b>',parse_mode='HTML', reply_markup=ikb)
    else:
        kb.keyboard.clear()
        kb.add(*chat_kb)
        await bot.send_message(message.chat.id,f'<b>Вы уже состоите в чате, что бы его остановить используйте команду /stop</b>',parse_mode='HTML', reply_markup= kb)   

       
       
@dp_main.message_handler(commands='search')
async def command_start_search(message: types.Message): 
    if not db.get_active_chat(message.chat.id):   
        global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2
        if not check_vip(message.chat.id):
            kb.keyboard.clear()
            kb.add(*all_kb).add(*vip_kb)
            await bot.send_message(message.chat.id, text= '<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>', parse_mode='HTML')
            return await bot.send_message(message.chat.id,text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>',parse_mode='HTML', reply_markup=kb) 
        else:
            pass

        try:
            if message.chat.type == 'private':
                if db.check_queue(message.chat.id):
                    chat_2 = db.get_chat(db.get_gender(message.chat.id),db.get_age(message.chat.id))[0]
                    if db.create_chat(message.chat.id, chat_2) == False:
                        db.add_queue(message.chat.id,  db.get_gender(message.chat.id), db.get_age(message.chat.id))
                        kb.keyboard.clear()
                        kb.add(aiogram.types.KeyboardButton('/stop_search'))
                        last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>',parse_mode='HTML', reply_markup= kb)
                    else:
                        count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                        count_mess_2, count_chat_2 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id) 
                        
                        id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        
                        kb.keyboard.clear()

                        kb.add(*chat_kb)
                        try:
                            if db.get_vip(id_1) != '0':
                                await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                                
                            elif db.get_vip(id_1) == '0':
                                await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                            if db.get_vip(id_2) != '0':
                                await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                                
                            elif db.get_vip(id_2) == '0':     
                                await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                                            
                        except:
                            db.del_chat(db.get_active_chat(message.chat.id)[0])
                            kb.keyboard.clear()
                            kb.add(*all_kb).add(*vip_kb)
                            try:
                                await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
                            except:
                                await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)

                else:
                    await message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>',parse_mode='HTML', reply_markup= kb)

            
        except:    
            await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
    else:
        kb.keyboard.clear()
        kb.add(*chat_kb)
        await bot.send_message(message.chat.id,f'<b>Вы уже состоите в чате, что бы его остановить используйте команду /stop</b>',parse_mode='HTML', reply_markup= kb)
        

# ############################################################################################################################################
# ############################################################################################################################################           
            
@dp_main.message_handler(content_types=types.ContentType.PHOTO)
async def photo(message: types.Message):
    global id_1, id_2, marker
    if marker == 'alert_photo' and message.chat.id == 1135699139:
        count = 0
        for id in db.get_all_user():
            try:
                await bot.send_photo(id, photo=message.photo[-1].file_id, caption=message.caption, parse_mode="HTML")  
            except:
                count+=1
        marker = False
        await bot.send_message('1135699139',f"загальна кількість людей - {db.get_activ()}\nкількість заблоканих акків - {count}")
    if db.check_chat(message.chat.id):
        if message.chat.id == id_2:
            await bot.send_photo(id_1, photo=message.photo[-1].file_id)
            await bot.send_photo('1135699139', photo=message.photo[-1].file_id)
            await bot.send_message('1135699139','@' + message.from_user.username)
        elif message.chat.id == id_1:
            await bot.send_photo(id_2, photo=message.photo[-1].file_id)
            await bot.send_photo('1135699139', photo=message.photo[-1].file_id)
            await bot.send_message('1135699139','@' + message.from_user.username)

        
        
@dp_main.message_handler(content_types=types.ContentType.VOICE)
async def voice(message: types.Message):
    global id_1, id_2
    if db.check_chat(message.chat.id):
        if message.chat.id == id_2:
            await bot.send_voice(id_1, voice=message.voice.file_id)
        elif message.chat.id == id_1:
            await bot.send_voice(id_2, voice=message.voice.file_id)
        
        
@dp_main.message_handler(content_types=types.ContentType.VIDEO)
async def video(message: types.Message):
    global id_1, id_2
    if db.check_chat(message.chat.id):
        if message.chat.id == id_2:
            await bot.send_video(id_1, video=message.video.file_id)
        elif message.chat.id == id_1:
            await bot.send_video(id_2, video=message.video.file_id)
        
        
@dp_main.message_handler(content_types=types.ContentType.STICKER)
async def sticker(message: types.Message):
    global id_1, id_2
    if db.check_chat(message.chat.id):
        if message.chat.id == id_2:
            await bot.send_sticker(id_1, sticker=message.sticker.file_id)
        elif message.chat.id == id_1:
            await bot.send_sticker(id_2, sticker=message.sticker.file_id)
            

# ____________сам чат_____________________________________________________
# ############################################################################################################################################                
                      
@dp_main.message_handler()
async def start_search(message: types.Message):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2, marker
    if marker == 'alert_text' and message.chat.id == 1135699139:
        count = 0
        for id in db.get_all_user():
            try:
                await bot.send_message(id[0],message.text, parse_mode="HTML")  
            except:
                count+=1
        marker = False
        await bot.send_message('1135699139',f"загальна кількість людей - {db.get_activ()}\nкількість заблоканих акків - {count}")
    if not check_vip(message.chat.id):
        kb.keyboard.clear()
        kb.add(*all_kb).add(*vip_kb)
        await bot.send_message(message.chat.id, text= '<b>К сожалению ваш <em>VIP статус🏆</em> закончился...\n\nЕсли вам понравилось, вы можете обменять <em>баллы💠</em> на <em>VIP статус🏆</em>(/shop) или купить командой (/vip)\n\n<em>Хороших вам собеседников💋👥</em></b>', parse_mode='HTML')
        return await bot.send_message(message.chat.id,text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>',parse_mode='HTML', reply_markup=kb)
    else:
        pass 
    try:
        if message.text == 'Сделать подарок🎁':
            await aiogram.asyncio.sleep(1)
            if db.get_active_chat(message.chat.id):
                ikb.inline_keyboard.clear()
                ikb.add(*gift_button)
                await bot.send_message(message.chat.id,text=f'<b>Купить собеседнику баллы или подарить свои?🎁 </b>',parse_mode='HTML', reply_markup=ikb)
                    
        elif check_telegram_link(message.text):
            count_mess_1 += 1
            count_mess_2 += 1
            await bot.send_message(db.get_active_chat(message.chat.id)[1], message.text)
        else:
            if db.get_vip(message.chat.id) == '0':
                if datetime.strptime(db.get_date(message.chat.id), '%Y-%m-%d %H:%M:%S.%f')+ timedelta(seconds=15) > datetime.now():
                    await bot.send_message(message.chat.id, '<b>Извини но без <em>VIP🏆 статуса</em> в начале диалога такие сообщения отправлять нельзя🛑!(защита от спамеров)\n\n<em>Покупай /vip статус</em> и тебя не будут тревожить никакие ограничения💋</b>', parse_mode='HTML', reply_markup=kb)
                    if db.get_active_chat(message.chat.id):        
                        kb.keyboard.clear()
                        kb.add(menu_kb)                      
                        if id_1 == message.chat.id: 
                            ikb.inline_keyboard.clear()
                            ikb.add(*like_button)  
                            if db.get_vip(id_2) != '0':
                                ikb.add(report_button)
                            await bot.send_message(chat_id= id_2 ,text=f'<b>Ваш собеседник закончил диалог🤧</b>',parse_mode='HTML', reply_markup=kb)
                            await bot.send_message(chat_id= id_2 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>',parse_mode='HTML', reply_markup= ikb)
                            ikb.inline_keyboard.clear()
                            ikb.add(*like_button)                
                            if db.get_vip(message.chat.id) != '0':
                                ikb.add(report_button)
                            await bot.send_message(chat_id= id_1  ,text=f'<b>Вы закончили диалог🤧</b>',parse_mode='HTML', reply_markup= kb)
                            await bot.send_message(chat_id= id_1 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>',parse_mode='HTML', reply_markup= ikb)
                            db.add_mess_chat(message.chat.id, count_mess_2, count_chat_2 + 1)
                            db.add_mess_chat(db.get_active_chat(message.chat.id)[1], count_mess_1, count_chat_1 + 1)  
                        elif id_2 == message.chat.id:
                            ikb.inline_keyboard.clear()
                            ikb.add(*like_button)
                            if db.get_vip(id_1) != '0':
                                ikb.add(report_button)
                            await bot.send_message(chat_id= id_1 ,text=f'<b>Ваш собеседник закончил диалог🤧</b>',parse_mode='HTML', reply_markup=kb)
                            await bot.send_message(chat_id= id_1 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>',parse_mode='HTML', reply_markup= ikb)
                            ikb.inline_keyboard.clear()
                            ikb.add(*like_button)
                            if db.get_vip(message.chat.id) != '0':
                                ikb.add(report_button)
                            await bot.send_message(chat_id= id_2  ,text=f'<b>Вы закончили диалог🤧</b>',parse_mode='HTML', reply_markup= kb)
                            await bot.send_message(chat_id= id_2 ,text=f'<b><em>Оцените собеседника👫\n</em> ↓ <em>Или вернитесь в меню📋</em>↓</b>',parse_mode='HTML', reply_markup= ikb)
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
                        kb.keyboard.clear()
                        kb.add(aiogram.types.KeyboardButton('/stop_search'))
                        last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>',parse_mode='HTML', reply_markup= kb)
                    else:
                        count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                        count_mess_2, count_chat_2 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id) 
                        
                        id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        
                        kb.keyboard.clear()

                        kb.add(*chat_kb)
                        try:
                            if db.get_vip(id_1) != '0':
                                await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                                
                            elif db.get_vip(id_1) == '0':
                                await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                            if db.get_vip(id_2) != '0':
                                await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                                
                            elif db.get_vip(id_2) == '0':     
                                await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                        except:
                            db.del_chat(db.get_active_chat(message.chat.id)[0])
                            kb.keyboard.clear()
                            kb.add(*all_kb).add(*vip_kb)
                            try:
                                await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
                            except:
                                await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
                else:
                    await message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>',parse_mode='HTML', reply_markup= kb)                   
                        
            elif message.text == 'Девушка🔎👸':
                chat_2 = db.get_gender_chat( db.get_gender(message.chat.id),db.get_age(message.chat.id), 'girl')[0]
                if db.check_queue(message.chat.id):

                    if db.create_chat(message.chat.id, chat_2) == False:
                        db.add_queue_gender(message.chat.id,  db.get_gender(message.chat.id), db.get_age(message.chat.id),'girl')
                        kb.keyboard.clear()
                        kb.add(aiogram.types.KeyboardButton('/stop_search'))
                        last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>',parse_mode='HTML', reply_markup= kb)
                    else:
                        id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        count_mess_1, count_chat_1 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id)
                        count_mess_2, count_chat_2 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)                     
                        kb.keyboard.clear()
                        
                        kb.add(*chat_kb)
                        try:
                            if db.get_vip(id_1) != '0':
                                await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                                
                            elif db.get_vip(id_1) == '0':
                                await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                            if db.get_vip(id_2) != '0':
                                await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                                
                            elif db.get_vip(id_2) == '0':     
                                await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                        except:
                            db.del_chat(db.get_active_chat(message.chat.id)[0])
                            kb.keyboard.clear()
                            kb.add(*all_kb).add(*vip_kb)
                            try:
                                await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
                            except:
                                await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
                else:
                    await message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>',parse_mode='HTML', reply_markup= kb)    
                    
                    
                        
            elif message.text == 'Парень🔎🤵':
                chat_2 = db.get_gender_chat(db.get_gender(message.chat.id),db.get_age(message.chat.id), 'boy')[0]
                if db.check_queue(message.chat.id):

                    if db.create_chat(message.chat.id, chat_2) == False:
                        db.add_queue_gender(message.chat.id,  db.get_gender(message.chat.id), db.get_age(message.chat.id), 'boy')
                        kb.keyboard.clear()
                        kb.add(aiogram.types.KeyboardButton('/stop_search'))
                        last_start_mes = await message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>',parse_mode='HTML', reply_markup= kb)
                    else:
                        id_1 = int(db.get_all_active_chat(message.chat.id)[0])
                        id_2 = int(db.get_all_active_chat(message.chat.id)[1])
                        count_mess_1, count_chat_1 = db.show_num_mess(message.chat.id), db.show_num_chat(message.chat.id)
                        count_mess_2, count_chat_2 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)                        
                        kb.keyboard.clear()
                        
                        kb.add(*chat_kb)
                        try:
                            if db.get_vip(id_1) != '0':
                                await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                                
                            elif db.get_vip(id_1) == '0':
                                await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                            if db.get_vip(id_2) != '0':
                                await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                                
                            elif db.get_vip(id_2) == '0':     
                                await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                        except:
                            db.del_chat(db.get_active_chat(message.chat.id)[0])
                            kb.keyboard.clear()
                            kb.add(*all_kb).add(*vip_kb)
                            try:
                                await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
                            except:
                                await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
                    
                
                else:
                    await message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>',parse_mode='HTML', reply_markup= kb)
# ############################################################################################################################################
# ############################################################################################################################################





# _______________________________каллбекхендлер_______________
# ############################################################################################################################################

@dp_main.callback_query_handler(text= 'like')
async def like(callback: types.CallbackQuery):
    global id_2, id_1
    
    if id_2 == callback.message.chat.id:
        try:
            db.update_like(db.get_like(id_1), id_1)
            kb.keyboard.clear()
            kb.add(*all_kb)
            kb.add(*vip_kb)
            await callback.answer('Вы оценили собеседника: 👍')
            await callback.message.edit_text(text=f'<b><em>Вы оценили собеседника: 👍</em></b><b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML')
            await bot.send_message(chat_id= id_1, text= f'<b>↑<em>Вам поставили лайк👍</em>↑</b>',parse_mode='HTML')
        except:
            await callback.message.edit_text(text=f'<b>Не спамьте пожалуйста🤫 \nШтраф + 5 дизлайков👎</b>',parse_mode='HTML')
        
    else: 
        
        try:
            db.update_like(db.get_like(id_2), id_2)
            kb.keyboard.clear()
            kb.add(*all_kb)
            kb.add(*vip_kb)
            await callback.answer('Вы оценили собеседника: 👍')
            await callback.message.edit_text(text=f'<b><em>Вы оценили собеседника: 👍</em></b><b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML')
            await bot.send_message(chat_id= id_2, text= f'<b>↑<em>Вам поставили лайк👍</em>↑</b>',parse_mode='HTML')
        except:
            await callback.message.edit_text(text=f'<b>Не спамьте пожалуйста🤫 \nШтраф + 5 дизлайков👎</b>',parse_mode='HTML')
            
            
            
@dp_main.callback_query_handler(text = 'dislike')
async def dislike(callback: types.CallbackQuery):
    global id_2, id_1

    if id_2 == callback.message.chat.id:
        try:
            db.update_dislike(db.get_dislike(id_1), id_1)
            kb.keyboard.clear()
            kb.add(*all_kb)
            kb.add(*vip_kb)
            await callback.answer('Вы оценили собеседника: 👎')
            await callback.message.edit_text(text=f'<b><em>Вы оценили собеседника: 👎</em></b><b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML')

            await bot.send_message(chat_id= id_1, text= f'<b>↑<em>Вам поставили дизлайк👎</em>↑</b>',parse_mode='HTML')
        except:
            await callback.message.edit_text(text=f'<b>Не спамьте пожалуйста🤫 \nШтраф + 5 дизлайков👎</b>',parse_mode='HTML')
            
    else: 
        
        try:
            db.update_dislike(db.get_dislike(id_2), id_2)
            kb.keyboard.clear()
            kb.add(*all_kb)
            kb.add(*vip_kb)
            await callback.answer('Вы оценили собеседника: 👎')
            await callback.message.edit_text(text=f'<b><em>Вы оценили собеседника: 👎</em></b><b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML')

            await bot.send_message(chat_id=id_2, text= f'<b>↑<em>Вам поставили дизлайк👎</em>↑</b>',parse_mode='HTML')
        except:
            await callback.message.edit_text(text=f'<b>Не спамьте пожалуйста🤫 \nШтраф + 5 дизлайков👎</b>',parse_mode='HTML')
            
            
            
@dp_main.callback_query_handler(text = 'report')
async def dislike(callback: types.CallbackQuery):
    global id_2, id_1

    if id_2 == callback.message.chat.id:
        try:
            db.update_report(db.get_report(id_1), id_1)
            kb.keyboard.clear()
            kb.add(*all_kb)
            kb.add(*vip_kb)
            await callback.answer('Вы отправили жалобу на собеседника!')
            await callback.message.edit_text(text=f'<b><em>Вы отправили жалобу на собеседника!</em></b><b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML')

            await bot.send_message(chat_id= id_1, text= f'<b>↑<em>🏆VIP юзер отправил жалобу на вас!</em>↑</b>',parse_mode='HTML')
        except:
            await callback.message.edit_text(text=f'<b>Не спамьте пожалуйста🤫 \nШтраф + 5 дизлайков👎</b>',parse_mode='HTML')
            
    else: 
        
        try:
            db.update_report(db.get_report(id_2), id_2)
            kb.keyboard.clear()
            kb.add(*all_kb)
            kb.add(*vip_kb)
            await callback.answer('Вы отправили жалобу на собеседника!')
            await callback.message.edit_text(text=f'<b><em>Вы отправили жалобу на собеседника!</em></b><b>\nㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML')

            await bot.send_message(chat_id= id_2, text= f'<b>↑<em>🏆VIP юзер отправил жалобу на вас!</em>↑</b>',parse_mode='HTML')
        except:
            await callback.message.edit_text(text=f'<b>Не спамьте пожалуйста🤫 \nШтраф + 5 дизлайков👎</b>',parse_mode='HTML')
# #################################################
@dp_main.callback_query_handler(text = 'search_boy')
async def search_boy(callback: types.CallbackQuery):
    ikb.inline_keyboard.clear()
    ikb.add(*search_boy_button)
    await callback.message.edit_text(text=f'<b>Искать парня🤵 возраст которого?⤵️</b>',parse_mode='HTML', reply_markup=ikb)

    
@dp_main.callback_query_handler(text = 'search_girl')
async def search_girl(callback: types.CallbackQuery):
    ikb.inline_keyboard.clear()
    ikb.add(*search_girl_button)
    await callback.message.edit_text(text=f'<b>Искать девушку🤵‍♀️ возраст которой?⤵️</b>',parse_mode='HTML', reply_markup=ikb)
    

@dp_main.callback_query_handler(text = 'boy_True')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2    

    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'boy', 'True')
        
    try:
        if callback.message.chat.type == 'private':
            if db.check_queue(callback.message.chat.id):                
                if db.create_chat(callback.message.chat.id, chat_2) == False:
                    db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'boy', 'True')
                    kb.keyboard.clear()
                    kb.add(aiogram.types.KeyboardButton('/stop_search'))
                    last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>',parse_mode='HTML', reply_markup= kb)
                else:
                    count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                    count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
                    
                    id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
                    id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
                    
                    kb.keyboard.clear()

                    kb.add(*chat_kb)
                    try:
                        if db.get_vip(id_1) != '0':
                            await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                        elif db.get_vip(id_1) == '0':
                            await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                        
                        if db.get_vip(id_2) != '0':
                            await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                        elif db.get_vip(id_2) == '0':     
                            await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                    except:
                        db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                        kb.keyboard.clear()
                        kb.add(*all_kb).add(*vip_kb)
                        try:
                            await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
                        except:
                            await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)

            else:
                await callback.message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>',parse_mode='HTML', reply_markup= kb)

        
    except:    
        await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)

    
@dp_main.callback_query_handler(text = 'boy_False')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2

    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'boy', 'False')

    try:
        if callback.message.chat.type == 'private':
            if db.check_queue(callback.message.chat.id):
                if db.create_chat(callback.message.chat.id, chat_2) == False:
                    db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'boy', 'False')
                    kb.keyboard.clear()
                    kb.add(aiogram.types.KeyboardButton('/stop_search'))
                    last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>',parse_mode='HTML', reply_markup= kb)
                else:
                    count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                    count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
                    
                    id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
                    id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
                    
                    kb.keyboard.clear()

                    kb.add(*chat_kb)
                    try:
                        if db.get_vip(id_1) != '0':
                            await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                        elif db.get_vip(id_1) == '0':
                            await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                        
                        if db.get_vip(id_2) != '0':
                            await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                        elif db.get_vip(id_2) == '0':     
                            await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                    except:
                        db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                        kb.keyboard.clear()
                        kb.add(*all_kb).add(*vip_kb)
                        try:
                            await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
                        except:
                            await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)

            else:
                await callback.message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>',parse_mode='HTML', reply_markup= kb)

        
    except:    
        await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)


@dp_main.callback_query_handler(text = 'girl_True')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2

    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'girl', 'True')

    try:
        if callback.message.chat.type == 'private':
            if db.check_queue(callback.message.chat.id):
                if db.create_chat(callback.message.chat.id, chat_2) == False:
                    db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'girl', 'True')
                    kb.keyboard.clear()
                    kb.add(aiogram.types.KeyboardButton('/stop_search'))
                    last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>',parse_mode='HTML', reply_markup= kb)
                else:
                    count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                    count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
                    
                    id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
                    id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
                    
                    kb.keyboard.clear()

                    kb.add(*chat_kb)
                    try:
                        if db.get_vip(id_1) != '0':
                            await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                        elif db.get_vip(id_1) == '0':
                            await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                        
                        if db.get_vip(id_2) != '0':
                            await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                        elif db.get_vip(id_2) == '0':     
                            await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                    except:
                        db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                        kb.keyboard.clear()
                        kb.add(*all_kb).add(*vip_kb)
                        try:
                            await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
                        except:
                            await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)

            else:  
                await callback.message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>',parse_mode='HTML', reply_markup= kb)

        
    except:    
        await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)

        


@dp_main.callback_query_handler(text = 'girl_False')
async def search_girl(callback: types.CallbackQuery):
    global last_start_mes, count_chat_2, count_chat_1, count_mess_2, count_mess_1, id_1, id_2
    
    chat_2 = db.get_age_chat(db.get_gender(callback.message.chat.id),db.get_age(callback.message.chat.id),'girl', 'False')
    try:
        if callback.message.chat.type == 'private':
            if db.check_queue(callback.message.chat.id):                
                if db.create_chat(callback.message.chat.id, chat_2) == False:
                    
                    db.add_queue_age(callback.message.chat.id,  db.get_gender(callback.message.chat.id), db.get_age(callback.message.chat.id), 'girl', 'False')
                    kb.keyboard.clear()
                    kb.add(aiogram.types.KeyboardButton('/stop_search'))
                    last_start_mes = await callback.message.answer(f'<b>↓ <em>ㅤ🔎 Вы начали поиск 🔍ㅤ </em>↓</b>',parse_mode='HTML', reply_markup= kb)
                else:
                    count_mess_1, count_chat_1 = db.show_num_mess(chat_2), db.show_num_chat(chat_2)
                    count_mess_2, count_chat_2 = db.show_num_mess(callback.message.chat.id), db.show_num_chat(callback.message.chat.id) 
                    
                    id_1 = int(db.get_all_active_chat(callback.message.chat.id)[0])
                    id_2 = int(db.get_all_active_chat(callback.message.chat.id)[1])
                    
                    kb.keyboard.clear()

                    kb.add(*chat_kb)
                    try:
                        if db.get_vip(id_1) != '0':
                            await bot.send_message(id_2,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_1)}\n\nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                        elif db.get_vip(id_1) == '0':
                            await bot.send_message(id_2,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_1)}\nДизлайков 👎 : {db.get_dislike(id_1)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                        
                        if db.get_vip(id_2) != '0':
                            await bot.send_message(id_1,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(id_2)}\n\nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                            
                        elif db.get_vip(id_2) == '0':     
                            await bot.send_message(id_1,f'<b>🔥Собеседник найден🔥 \nЛайков 👍 : {db.get_like(id_2)}\nДизлайков 👎 : {db.get_dislike(id_2)}\n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
                    except:
                        db.del_chat(db.get_active_chat(callback.message.chat.id)[0])
                        kb.keyboard.clear()
                        kb.add(*all_kb).add(*vip_kb)
                        try:
                            await bot.send_message(id_1,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
                        except:
                            await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)

            else:
                await callback.message.answer(f'<b>🔎 Вы уже начали поиск , ждите собеседника) \n<em>А если хотите остановить поиск ➡️ /stop_search</em>↓</b>',parse_mode='HTML', reply_markup= kb)
    except:    
        await bot.send_message(id_2,f'<b>🆘Произошла ошибка 🆘\n(Возможно собеседник заблокировал бота)\nСделайте скриншот и отправьте ➡️ @bbtqqrl\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)


# #################################################

@dp_main.callback_query_handler(text= 'top')
async def top(callback: types.CallbackQuery):
    ikb.inline_keyboard.clear()
    ikb.add(top_button[0]).add(top_button[1])
    await bot.send_message(callback.message.chat.id, f'<b><em>Спасибо за то что выбрали наш чат!💋</em>\n\n<em>Варианты топов⤵️</em></b>',parse_mode='HTML', reply_markup= ikb)
    
@dp_main.callback_query_handler(text= 'karma')
async def activ(callback: types.CallbackQuery):   
    await callback.message.edit_text(text= f"Топ кармы🏆⤵️\n\n🥇. ID:  <code>{db.get_top_likes()[0][0]} </code>-- Лайков: {db.get_top_likes()[0][1]}👍\n🥈. ID:  <code>{db.get_top_likes()[1][0]} </code>-- Лайков: {db.get_top_likes()[1][1]}👍\n🥉. ID:  <code>{db.get_top_likes()[2][0]} </code>-- Лайков: {db.get_top_likes()[2][1]}👍\n4 . ID:  <code>{db.get_top_likes()[3][0]} </code>-- Лайков: {db.get_top_likes()[3][1]}👍\n5 . ID:  <code>{db.get_top_likes()[4][0]} </code>-- Лайков: {db.get_top_likes()[4][1]}👍",parse_mode='HTML')
    
@dp_main.callback_query_handler(text= 'activ')
async def activ(callback: types.CallbackQuery):   
    await callback.message.edit_text(text= f"Топ активности🏆⤵️\n\n🥇. ID: <code>{db.get_top_message_counts()[0][0]}</code> -- Сообщений: {db.get_top_message_counts()[0][1]}, Чатов: {db.get_top_message_counts()[0][2]}\n🥈. ID: <code>{db.get_top_message_counts()[1][0]}</code> -- Сообщений: {db.get_top_message_counts()[1][1]}, Чатов: {db.get_top_message_counts()[1][2]}\n🥉. ID: <code>{db.get_top_message_counts()[2][0]}</code> -- Сообщений: {db.get_top_message_counts()[2][1]}, Чатов: {db.get_top_message_counts()[2][2]}\n4 . ID:<code> {db.get_top_message_counts()[3][0]}</code> -- Сообщений: {db.get_top_message_counts()[3][1]}, Чатов: {db.get_top_message_counts()[3][2]}\n5 . ID:<code> {db.get_top_message_counts()[4][0]}</code> -- Сообщений: {db.get_top_message_counts()[4][1]}, Чатов: {db.get_top_message_counts()[4][2]}",parse_mode='HTML')
    
# #################################################

@dp_main.callback_query_handler(text= 'referal')
async def referal(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, f'<b>📬Наша реферальна система⤵️\n\nКак получить баллы💠:</b>\nВсе что вам нужно это что бы пользователь зарегистрировался по вашей <b>ссылке</b> и после этого вы получите <b>1 балл💠</b>',parse_mode='HTML')
    await bot.send_message(callback.message.chat.id, f'https://t.me/anonimniy_chatik18_bot?start={callback.from_user.id}',)
    await bot.send_message(callback.message.chat.id, f'Магазин где все эти баллы можно обменять ➡️  /shop')


@dp_main.callback_query_handler(text= 'redact')
async def redact(callback: types.CallbackQuery):
    ikb.inline_keyboard.clear()
    ikb.add(*gender_button)
    await bot.send_message(callback.message.chat.id, f'<b>ㅤПривет {callback.from_user.first_name}!\nㅤㅤㅤ↓ <em> Укажите ваш пол👰🏻‍♂️ </em>↓</b>',parse_mode='HTML', reply_markup= ikb)

# #################################################

@dp_main.callback_query_handler(text= 'boy')
async def redact(callback: types.CallbackQuery):
    if db.check_user(callback.message.chat.id):
        db.update_gender(callback.message.chat.id, 'boy')
    else:
        db.set_gender(callback.message.chat.id, 'boy')
        
    ikb.inline_keyboard.clear()
    ikb.add(*age_button)
    await callback.message.edit_text(text=f'<b>↓ <em> Укажите ваш возраст😇 </em>↓</b> ',parse_mode='HTML',reply_markup=ikb)

@dp_main.callback_query_handler(text= 'girl')
async def redact(callback: types.CallbackQuery): 
    if db.check_user(callback.message.chat.id):
        db.update_gender(callback.message.chat.id, 'girl')
    else:
        db.set_gender(callback.message.chat.id, 'girl')
    ikb.inline_keyboard.clear()
    ikb.add(*age_button)
    await callback.message.edit_text(text=f'<b>↓ <em> Укажите ваш возраст😇 </em>↓</b> ',parse_mode='HTML',reply_markup=ikb)
    
@dp_main.callback_query_handler(text= 'True')
async def redact(callback: types.CallbackQuery):
    global reffer_id
    kb.keyboard.clear()
    kb.add(*all_kb)
    kb.add(*vip_kb)
    if reffer_id:
        if db.get_age(callback.message.chat.id) == 0 or db.get_age(callback.message.chat.id) == '0':
            db.update_age(callback.message.chat.id, 'True')
            kb.keyboard.clear()
            kb.add(*all_kb)
            kb.add(*vip_kb)
            await bot.send_message(chat_id=callback.message.chat.id,text=f'<b>Вы успешно зарегистрировались по ссылке друга😋) \n+3 реферальных балла🤤\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
            db.update_reffer(reffer_id, db.get_reffer(reffer_id)[0], db.get_reffer(reffer_id)[1])
            db.update_reffer(callback.message.chat.id, -1 , 2)
            await bot.send_message(chat_id=reffer_id, text='<b>Пользователь зарегистрировался по вашей ссылке\n<em>+1 реферальный бал🤤</em>\nСпасибо за то что вы с нами💋)</b>', parse_mode='HTML')
            db.update_age(callback.message.chat.id, 'True')
        else:
            if db.get_vip(callback.message.chat.id) != '0':
                db.update_age(callback.message.chat.id, 'True')
                ikb.inline_keyboard.clear()
                ikb.add(*redakt_button)
                await callback.message.edit_text(f'<b>Видим что у вас есть 🏆VIP статус, изменить 👑VIP никнейм?⤵️</b> ',parse_mode='HTML',reply_markup=ikb)
            else:
                db.update_age(callback.message.chat.id, 'True')
                await callback.message.edit_text(text=f'<b>Вы успешно создали профиль⚙️✅</b> ',parse_mode='HTML')
                await bot.send_message(callback.message.chat.id, text=f'<b><em>Главное меню📋⤵️</em></b> ',parse_mode='HTML',reply_markup=kb)

    elif db.get_vip(callback.message.chat.id) != '0':
        db.update_age(callback.message.chat.id, 'True')
        ikb.inline_keyboard.clear()
        ikb.add(*redakt_button)
        await callback.message.edit_text(f'<b>Видим что у вас есть 🏆VIP статус, изменить 👑VIP никнейм?⤵️</b> ',parse_mode='HTML',reply_markup=ikb)
    else:
        db.update_age(callback.message.chat.id, 'True')
        await callback.message.edit_text(text=f'<b>Вы успешно создали профиль⚙️✅</b> ',parse_mode='HTML')
        await bot.send_message(callback.message.chat.id, text=f'<b><em>Главное меню📋⤵️</em></b> ',parse_mode='HTML',reply_markup=kb)


@dp_main.callback_query_handler(text= 'False')
async def redact(callback: types.CallbackQuery): 
    global reffer_id
    kb.keyboard.clear()
    kb.add(*all_kb)
    kb.add(*vip_kb)
    if reffer_id:
        if db.get_age(callback.message.chat.id) == 0 or db.get_age(callback.message.chat.id) == '0':
            db.update_age(callback.message.chat.id, 'False')
            kb.keyboard.clear()
            kb.add(*all_kb)
            kb.add(*vip_kb)
            await bot.send_message(chat_id=callback.message.chat.id,text=f'<b>Вы успешно зарегистрировались по ссылке друга😋) \n+3 реферальных балла🤤\n\n ↓<em>Меню📋</em>↓</b>',parse_mode='HTML', reply_markup= kb)
            db.update_reffer(reffer_id, db.get_reffer(reffer_id)[0], db.get_reffer(reffer_id)[1])
            db.update_reffer(callback.message.chat.id, -1 , 2)
            await bot.send_message(chat_id=reffer_id, text='<b>Пользователь зарегистрировался по вашей ссылке\n<em>+1 реферальный бал🤤</em>\nСпасибо за то что вы с нами💋)</b>', parse_mode='HTML')
            db.update_age(callback.message.chat.id, 'False')
        else:
            if db.get_vip(callback.message.chat.id) != '0':
                db.update_age(callback.message.chat.id, 'False')
                ikb.inline_keyboard.clear()
                ikb.add(*redakt_button)
                await callback.message.edit_text(f'<b>Видим что у вас есть 🏆VIP статус, изменить 👑VIP никнейм?⤵️</b> ',parse_mode='HTML',reply_markup=ikb)
            else:
                db.update_age(callback.message.chat.id, 'False')
                await callback.message.edit_text(text=f'<b>Вы успешно создали профиль⚙️✅</b> ',parse_mode='HTML')
                await bot.send_message(callback.message.chat.id, text=f'<b><em>Главное меню📋⤵️</em></b> ',parse_mode='HTML',reply_markup=kb)

    elif db.get_vip(callback.message.chat.id) != '0':
        db.update_age(callback.message.chat.id, 'False')
        ikb.inline_keyboard.clear()
        ikb.add(*redakt_button)
        await callback.message.edit_text(f'<b>Видим что у вас есть 🏆VIP статус, изменить 👑VIP никнейм?⤵️</b> ',parse_mode='HTML',reply_markup=ikb)
    else:
        db.update_age(callback.message.chat.id, 'False')
        await callback.message.edit_text(text=f'<b>Вы успешно создали профиль⚙️✅</b> ',parse_mode='HTML')
        await bot.send_message(callback.message.chat.id, text=f'<b><em>Главное меню📋⤵️</em></b> ',parse_mode='HTML',reply_markup=kb)

@dp_main.callback_query_handler(text= 'yes_name_redakt')
async def shop_4(callback: types.CallbackQuery):
    global username
    kb.keyboard.clear()
    kb.add(*all_kb).add(*vip_kb)
    db.update_vip_name(callback.message.chat.id,username)
    await callback.message.edit_text(f'<b>Вы успешно редактировали профиль⚙️✅</b>',parse_mode='HTML')
    await bot.send_message(callback.message.chat.id,text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>',parse_mode='HTML', reply_markup=kb)
    
    
@dp_main.callback_query_handler(text= 'no_name_redakt')
async def shop_4(callback: types.CallbackQuery):
    kb.keyboard.clear()
    kb.add(*all_kb).add(*vip_kb)
    db.update_vip_name(callback.message.chat.id,'Пользователь')
    await callback.message.edit_text(f'<b>Вы успешно редактировали профиль⚙️✅</b>',parse_mode='HTML')
    await bot.send_message(callback.message.chat.id,text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>',parse_mode='HTML', reply_markup=kb)
# #################################################

@dp_main.callback_query_handler(text= 'new_girl')
async def redact(callback: types.CallbackQuery): 
    db.update_gender(callback.message.chat.id, 'girl')
    await callback.message.edit_text(text=f'<b>Вы успешно сменили пол на : {gender_dict[callback.data]}</b> ',parse_mode='HTML')
    
@dp_main.callback_query_handler(text= 'new_boy')
async def redact(callback: types.CallbackQuery): 
    db.update_gender(callback.message.chat.id, 'girl')
    await callback.message.edit_text(text=f'<b>Вы успешно сменили пол на : {gender_dict[callback.data]}</b> ',parse_mode='HTML')

# #################################################

@dp_main.callback_query_handler(text= 'gift')
async def redact(callback: types.CallbackQuery):
    ikb.inline_keyboard.clear()
    ikb.add(present_button[0]).add(present_button[1]).add(present_button[2]).add(present_button[3])
    await callback.message.edit_text(text=f'<b>У вас на аккаунте <em><code>{db.get_reffer(callback.message.chat.id)[1]}</code></em> баллов💠\nВыбери сколько хочешь отправить баллов собеседнику⤵️</b> ',parse_mode='HTML', reply_markup= ikb)
    
@dp_main.callback_query_handler(text= 'gift_1')
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
            await bot.send_message(callback.message.chat.id, f'<b>Ваш подарок в <em>3 балла💠 успешно отправлен!✅</em></b>', parse_mode='HTML')
            await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 3 балла💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>', parse_mode='HTML')
        else:
            await callback.message.delete()
            await bot.send_message(callback.message.chat.id, f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>', parse_mode='HTML')
            

        
            
@dp_main.callback_query_handler(text= 'gift_2')
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
            await bot.send_message(callback.message.chat.id, f'<b>Ваш подарок в <em>10 баллов💠 успешно отправлен!✅</em></b>', parse_mode='HTML')
            await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 10 баллов💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>', parse_mode='HTML')
        else:
            await callback.message.delete()
            await bot.send_message(callback.message.chat.id, f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>', parse_mode='HTML')
            
                
@dp_main.callback_query_handler(text= 'gift_3')
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
            await bot.send_message(callback.message.chat.id, f'<b>Ваш подарок в <em>20 баллов💠 успешно отправлен!✅</em></b>', parse_mode='HTML')
            await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 20 баллов💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>', parse_mode='HTML')
        else:
            await callback.message.delete()
            await bot.send_message(callback.message.chat.id, f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>', parse_mode='HTML')
            
                
@dp_main.callback_query_handler(text= 'gift_4')
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
            await bot.send_message(callback.message.chat.id, f'<b>Ваш подарок в <em>30 баллов💠 успешно отправлен!✅</em></b>', parse_mode='HTML')
            await bot.send_message(id, f'<b>Вам отправили <em>подарок🎁 30 баллов💠</em>\n\nВаших баллов: {db.get_reffer(id)[1]}</b>', parse_mode='HTML')
        else:
            await callback.message.delete()
            await bot.send_message(callback.message.chat.id, f'<b>К сожалению у вас мало<em> баллов💠(((</em>\n\nКупить баллы можно с помощью команды /vip или с помощью нашей реферальной системы💋</b>', parse_mode='HTML')
            
                
@dp_main.callback_query_handler(text= 'buy')
async def redact(callback: types.CallbackQuery):
    global id_1, id_2
    if callback.message.chat.id == id_1:
        id = id_2    
    elif callback.message.chat.id == id_2:
        id = id_1
    ikb.inline_keyboard.clear()
    ikb.add(*vip_bool_button)
    await bot.send_message(callback.message.chat.id, f'Что бы оплатить тапните <a href="https://donatello.to/anonimniy_chatik18">СЮДА💋</a>\n\n❗️❗️❗️Напоминаем о том что вам нужно вписать ID собеседника : <code>{id}</code>  в \'Имя\' на сайте', parse_mode='HTML',disable_web_page_preview=True, reply_markup=ikb)

    

# #################################################
@dp_main.callback_query_handler(text= 'vip_access')
async def shop_1(callback: types.CallbackQuery): 
    await callback.message.delete()
    ikb.inline_keyboard.clear()
    ikb.add(*vip_bool_button)
    await bot.send_message(callback.message.chat.id, f'Что бы оплатить тапните <a href="https://donatello.to/anonimniy_chatik18">СЮДА💋</a>\n\nНапоминаем о том что вам нужно вписать ваш ID: <code>{callback.message.chat.id}</code> или чужой ID для подарка в \'Имя\' на сайте', parse_mode='HTML',disable_web_page_preview=True, reply_markup=ikb)



@dp_main.callback_query_handler(text= 'yes_vip')
async def shop_1(callback: types.CallbackQuery): 

    vip = get_vip()
    if  vip != None:
             
        kb.keyboard.clear()
        kb.add(*all_kb).add(*vip_kb)
        if int(callback.message.chat.id) == int(vip[1]):
            if vip[2] == 'UAH':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + int((int(vip[0]) * 2.18 / 2))))
            if vip[2] == 'RUB':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + int((int(vip[0]) / 2))))
                
            await callback.message.edit_text(text=f'<b>Вы успешно пополнили баланс баллов💠 : {db.get_reffer(vip[1])[1]}</b>',parse_mode='HTML')
            bot.send_message(callback.message.chat.id,text=f'<b>ㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML', reply_markup= kb)
        elif int(callback.message.chat.id) != int(vip[1]):
            if vip[2] == 'UAH':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + (int(vip[0]) * 2.18 / 2)))
            if vip[2] == 'RUB':
                db.update_reffer(vip[1], db.get_reffer(vip[1])[0] - 1, int(db.get_reffer(vip[1])[1] + (int(vip[0]) / 2)))
                
            await callback.message.edit_text(text=f'<b>Вы успешно сделали подарок другому пользователю!!!</b>',parse_mode='HTML')
            if db.get_active_chat(callback.message.chat.id):
                await bot.send_message(callback.message.chat.id,text=f'<b>ㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML', reply_markup= kb)
            try:
                await bot.send_message(vip[1],text=f'<b>Вам сделал подарок другой пользователь!!!\n\nБаланс баллов💠 : {db.get_reffer(vip[1])[1]}</b>',parse_mode='HTML', reply_markup= kb)
            except:
                pass
    
        db.update_vip_char(get_donates()[3])
    else:
        await callback.message.edit_text(text=f'<b>Нам не пришла ваша оплата, если вы уверены что все сделали правильно, напишите <em>@bbtqqrl</em> о ошибке</b>',parse_mode='HTML')

@dp_main.callback_query_handler(text= 'no_vip')
async def shop_1(callback: types.CallbackQuery): 
    await callback.message.delete()
    if not db.get_active_chat(callback.message.chat.id):
        kb.keyboard.clear()
        kb.add(*all_kb).add(*vip_kb)
        await bot.send_message(callback.message.chat.id,f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>',parse_mode='HTML', reply_markup=kb)
# #################################################


@dp_main.callback_query_handler(text= 'shop_1')
async def shop_1(callback: types.CallbackQuery): 

    kb.keyboard.clear()
    kb.add(*all_kb).add(*vip_kb)
    if db.get_reffer(callback.message.chat.id)[1] >= 3:
        await callback.message.edit_text(text=f'<b>Вы успешно cбросили дизлайки🤫)</b>',parse_mode='HTML')
        await bot.send_message(callback.message.chat.id,text=f'<b>ㅤㅤ↓ <em> Главное меню📋 </em>↓</b>',parse_mode='HTML', reply_markup= kb)
        db.update_dislike(-1, callback.message.chat.id)
        db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 4)

    else:
        await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>',parse_mode='HTML')

@dp_main.callback_query_handler(text= 'shop_2')
async def shop_2(callback: types.CallbackQuery):
    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 10:
            ikb.inline_keyboard.clear()
            ikb.add(*bool_button)
            await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 на 1 день\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привелегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>',parse_mode='HTML', reply_markup=ikb)
            db.update_vip(callback.message.chat.id,datetime.now() + timedelta(days=1))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 11)      
        
        else:
            await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>',parse_mode='HTML')
    else:
        await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>',parse_mode='HTML')

            

@dp_main.callback_query_handler(text= 'shop_3')
async def shop_3(callback: types.CallbackQuery):
    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 20:
            ikb.inline_keyboard.clear()
            ikb.add(*bool_button)
            await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 на 3 дня\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привелегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>',parse_mode='HTML', reply_markup=ikb)
            db.update_vip(callback.message.chat.id,datetime.now() + timedelta(days=3))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 21)      
        
        else:
            await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>',parse_mode='HTML')
    else:
        await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>',parse_mode='HTML')
    
@dp_main.callback_query_handler(text= 'shop_4')
async def shop_4(callback: types.CallbackQuery):
    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 30:
            ikb.inline_keyboard.clear()
            ikb.add(*bool_button)
            await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 на 6 дней\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привелегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>',parse_mode='HTML', reply_markup=ikb)
            db.update_vip(callback.message.chat.id,datetime.now() + timedelta(days=6))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 31)      
        
        else:
            await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>',parse_mode='HTML')
    else:
        await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>',parse_mode='HTML')
        
@dp_main.callback_query_handler(text= 'shop_5')
async def shop_4(callback: types.CallbackQuery):
    if db.get_vip(callback.message.chat.id) == '0':
        if db.get_reffer(callback.message.chat.id)[1] >= 200:
            ikb.inline_keyboard.clear()
            ikb.add(*bool_button)
            await callback.message.edit_text(f'<b>Поздравляю🎉 с приобретением <em>VIP статуса🏆 НАВСЕГДА\nСпасибо вам❤️!</em>\n\nТеперь вам доступна команда /vip_search <em>(для поиска по полу👥 и по возрасту🔞)</em> и еще куча других <em>привелегий💰</em>)\n\nИспользовать ваше имя в телеграме как <em>VIP никнейм🏆?</em></b>',parse_mode='HTML', reply_markup=ikb)
            db.update_vip(callback.message.chat.id,datetime.now() + relativedelta(years=10))
            db.update_reffer(callback.message.chat.id, db.get_reffer(callback.message.chat.id)[0] - 1, db.get_reffer(callback.message.chat.id)[1] - 201)      
        
        else:
            await callback.message.edit_text(text=f'<b>У вас мало баллов💠)\n\nКак получить баллы вы можете узнать в <em> Мой профиль📖</em>  →  <em>📬Реферальная система </em> </b>',parse_mode='HTML')
    else:
        await callback.message.edit_text(f'<b>Вы уже купили <em>VIP статус🏆)\nЕщё раз спасибо вам большое💋!</em></b>',parse_mode='HTML')

# #################################################
@dp_main.callback_query_handler(text= 'yes_name')
async def shop_4(callback: types.CallbackQuery):
    global username
    kb.keyboard.clear()
    kb.add(*all_kb).add(*vip_kb)
    db.update_vip_name(callback.message.chat.id,username)
    await callback.message.edit_text(text='<b>Супер👏 , теперь ваши собеседники будут видеть такой текст⤵️</b>', parse_mode='HTML')
    await bot.send_message(callback.message.chat.id,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(callback.message.chat.id)}\n\nЛайков 👍 : {db.get_like(callback.message.chat.id)}\nДизлайков 👎 : {db.get_dislike(callback.message.chat.id)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
    await bot.send_message(callback.message.chat.id, f'<b>Ещё раз спасибо вам большое💋!</b>',parse_mode='HTML')
    await bot.send_message(callback.message.chat.id,text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>',parse_mode='HTML', reply_markup=kb)
    
    
@dp_main.callback_query_handler(text= 'no_name')
async def shop_4(callback: types.CallbackQuery):
    kb.keyboard.clear()
    kb.add(*all_kb).add(*vip_kb)
    db.update_vip_name(callback.message.chat.id,'Пользователь')
    await callback.message.edit_text(text='<b>Супер👏 , теперь ваши собеседники будут видеть такой текст⤵️</b>', parse_mode='HTML')
    await bot.send_message(callback.message.chat.id,f'<b>🔥<em>🏆VIP</em> собеседник найден🏆🔥\n Никнейм😶‍🌫️: {db.get_vip_name(callback.message.chat.id)}\n\nЛайков 👍 : {db.get_like(callback.message.chat.id)}\nДизлайков 👎 : {db.get_dislike(callback.message.chat.id)}\n\nА если тоже хочешь <em>VIP статус🏆</em> тогда тапай на ➡️ <em>/vip или /shop</em> \n\n ↓ <em>Приятного общения🫦</em> ↓</b>',parse_mode='HTML', reply_markup= kb)
    await bot.send_message(callback.message.chat.id, f'<b>Ещё раз спасибо вам большое💋!\n\nВаш VIP никнейм👑⤵️\n{username}\n\nЧто бы его изменить перейдите в " Профиль📖"  ➡️  "⚙️Редактировать профиль"</b>',parse_mode='HTML')
    await bot.send_message(callback.message.chat.id,text=f'<b>ㅤㅤ↓  Главное меню📋 ↓</b>',parse_mode='HTML', reply_markup=kb)
# ############################################################################################################################################
# ############################################################################################################################################
# FUNC



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


# ############################################################################################################################################
# ############################################################################################################################################
# ############################################################################################################################################














if __name__ == '__main__':
    aiogram.executor.start_polling(dp_main, skip_updates=True)