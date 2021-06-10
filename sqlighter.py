import sqlite3

class SQLighter:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
    
    def get_chat(self):
        """Получаем всех активных подписчиков бота"""
        with self.conn:
            return self.cursor.execute('SELECT * FROM user_karma').fetchall()

    def get_group(self):
        with self.conn:
            return self.cursor.execute('SELECT * FROM groups').fetchall()
    
    def get_info_group(self, group_id):
        with self.conn:
            return self.cursor.execute('SELECT * FROM user_karma WHERE group_id = ?', (group_id,)).fetchall()
    
    def user_exists(self, group_id, user_id):
        with self.conn:
            result = self.cursor.execute('SELECT * FROM user_karma WHERE group_id=? AND user_id=?', (group_id, user_id)).fetchall()
            return bool(len(result))
    
    def group_exists(self, group_id):
        with self.conn:
            result = self.cursor.execute('SELECT * FROM groups WHERE group_id=?', (group_id,)).fetchall()
            return bool(len(result))

    def add_user_in_chat(self, group_id, user_id, user_fullname, karma):
        with self.conn:
            return self.cursor.execute('INSERT INTO user_karma (group_id, user_id, user_fullname, karma) VALUES(?,?,?,?)', (group_id, user_id, user_fullname, karma))
    
    def add_group(self, group_id, group_fullname):
        with self.conn:
            return self.cursor.execute('INSERT INTO groups (group_id, group_fullname) VALUES(?,?)', (group_id, group_fullname))

    def get_karma_user(self, group_id, user_id):
        with self.conn:
            result = self.cursor.execute('SELECT karma FROM user_karma WHERE group_id=? AND user_id=?', (group_id, user_id)).fetchall()
            return float('%.2f' % result[0][0])
    
    def update_user_karma(self, group_id, user_id, karma):
        with self.conn:
            return self.cursor.execute(f'UPDATE user_karma SET karma=? WHERE group_id = ? AND user_id = ?', (karma, group_id, user_id))
    
    def update_user_admin(self):
        pass
    
    def save(self):
        """Сохраняем с БД"""
        self.conn.commit()
    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()