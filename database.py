import sqlite3
from datetime import datetime

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