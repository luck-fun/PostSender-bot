from database.tables import db, cursor

class Methods():
    def __init__(self, user_id, user_name, channel_id):
        self.user_id = user_id
        self.user_name = user_name
        self.channel_id = channel_id

    def add_channel(self):
        cursor.execute("INSERT INTO main_table VALUES (?, ?, ?)", [self.user_id, self.user_name, self.channel_id])
        db.commit()

    def delete_channel(self):
        cursor.execute("DELETE FROM main_table WHERE user_id = ?", [self.user_id])
        db.commit()