import sqlite3

class SQLighter:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
    
    def get_chat(self):
        """Получаем всех активных подписчиков бота"""
        with self.conn:
            return self.cursor.execute('SELECT * FROM groups').fetchall()
    def user_exists(self, group_id, user_id):
        with self.conn:
            result = self.cursor.execute('SELECT * FROM groups WHERE group_id=? AND user_id=?', (group_id, user_id)).fetchall()
            return bool(len(result))
    def add_user_in_chat(self, group_id, user_id, group_fullname, user_fullname, karma):
        with self.conn:
            return self.cursor.execute('INSERT INTO groups (group_id, user_id, group_fullname, user_fullname, karma) VALUES(?,?,?,?,?)', (group_id, user_id, group_fullname, user_fullname, karma))
    def get_karma_user(self, group_id, user_id):
        with self.conn:
            result = self.cursor.execute('SELECT karma FROM groups WHERE group_id=? AND user_id=?', (group_id, user_id)).fetchall()
            return float('%.2f' % result[0][0])
    def update_user_karma(self, group_id, user_id, karma):
        with self.conn:
            return self.cursor.execute(f'UPDATE groups SET karma=? WHERE group_id = ? AND user_id = ?', (karma, group_id, user_id))
    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()