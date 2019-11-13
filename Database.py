import sqlite3
import getpass

database = sqlite3.connect("users.db")  # Connect users.db, where saves user's favourite music
user = getpass.getuser()
count = 1


def add_user():
    database.execute("""INSERT INTO users_music VALUES(? ,"Rishat", "Gayporn.mp3:123")""", (count,))
    database.commit()

def add_to_database(song):
    database.execute("""UPDATE users_music SET music = ? WHERE username = ?""", (song, user))
    database.commit()
    print(database.execute("""SELECT * FROM users_music WHERE username = ?""", (user,)).fetchall())


def remove_from_database(song):
    music_list = database.execute("""SELECT music FROM users_music WHERE username = ?""", (user,))

    database.execute("""UPDATE users_music SET music = ? WHERE username = ?""", (song, user))
    database.commit()
    print(database.execute("""SELECT * FROM users_music WHERE username = ?""", (user,)).fetchall())