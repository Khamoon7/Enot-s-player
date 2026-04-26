import sqlite3
import getpass

database = sqlite3.connect("users.db")  # Connect users.db, where saves user's favourite music
user = getpass.getuser()
count = 1


def get_music():
    music_list = database.execute("""SELECT music FROM users_music WHERE username = ?""", (user,)).fetchall()
    music_list = music_list[0][0].split(":")
    return music_list


def add_user():
    try:
        user_now = database.execute("""SELECT username FROM users_music WHERE username = ?""", (user,)).fetchall()[0][0]
    except IndexError:
        database.execute("""INSERT INTO users_music VALUES(? , ?, "")""", (count, user))
        database.commit()


def add_to_database(song):
    music_list = database.execute("""SELECT music FROM users_music WHERE username = ?""", (user,)).fetchall()
    music_list = music_list[0][0].split(":")
    if song not in music_list:
        music_list.append(song)
    database.execute("""UPDATE users_music SET music = ? WHERE username = ?""", (":".join(music_list), user))
    database.commit()
    #print(database.execute("""SELECT * FROM users_music""").fetchall())


def remove_from_database(song):
    music_list = database.execute("""SELECT music FROM users_music WHERE username = ?""", (user,)).fetchall()
    music_list = music_list[0][0].split(":")
    music_list.remove(song)
    database.execute("""UPDATE users_music SET music = ? WHERE username = ?""", (":".join(music_list), user))
    database.commit()
    #print(database.execute("""SELECT * FROM users_music""").fetchall())


def check_in_database(song):
    music_list = database.execute("""SELECT music FROM users_music WHERE username = ?""", (user,)).fetchall()
    music_list = music_list[0][0].split(":")
    if song in music_list:
        return True
    return False
