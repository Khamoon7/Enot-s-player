import sqlite3

database = sqlite3.connect("users.db")  # Connect users.db, where saves user's favourite music


def add_to_database(song):
    database.execute("""UPDATE users_music SET music = ? """, ("123.mp3",))
    database.commit()
    print(database.execute("""SELECT * FROM users_music""").fetchall())
