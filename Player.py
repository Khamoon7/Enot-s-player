# Enot's player v1.0

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


def main():
    app = QApplication(sys.argv)
    player = Player()
    sys.exit(app.exec())


class Player(QMainWindow):  # Main window
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.user_action = -1  # 1 = playing, -1 = paused
        self.flag = True  # Check song playing
        self.songs = []  # Songs list
        self.repeat_flag = False  # Repeat mode check

        self.setFixedSize(1100, 500)  # Main window
        self.center()
        self.setWindowTitle("Enot's player")
        self.setWindowIcon(QIcon("icons\\good.jpg"))

        self.player_create()  # Create player

        self.logo()  # Image in the widget

        self.lists()  # Create lists of songs and folders

        self.time()  # Time labels

        self.names()  # Name labels

        self.slider()  # Create slider

        self.buttons()  # Create buttons

        self.menubar_create()  # Create menubar

        self.find_all_func()  # Show music

        self.show()

    def center(self):  # Set window in the center of monitor
        window = self.frameGeometry()
        user = QDesktopWidget().availableGeometry().center()
        window.moveCenter(user)
        self.move(window.topLeft())

    def player_create(self):
        self.player = QMediaPlayer()  # Create player
        self.player.setVolume(50)
        self.playlist = QMediaPlaylist()  # Create playlist
        self.player.positionChanged.connect(self.change_time)
        self.player.stateChanged.connect(self.change_butt)

    def logo(self):  # Creation logo
        self.image = QPushButton(self)
        self.image.resize(300, 300)
        self.image.move(570, 50)
        self.image.setIcon(QIcon("icons\\good.jpg"))
        self.image.setIconSize(QSize(300, 300))

    def lists(self):  # Function that creates lists with songs
        self.list_of_folder = QListWidget(self)  # List of Folders with .mp3 files
        self.list_of_folder.setGeometry(QRect(0, 20, 230, 500))
        self.list_of_folder.currentTextChanged.connect(self.getfiles)

        self.list_of_songs = QListWidget(self)  # List of .mp3 files in each Folder
        self.list_of_songs.setGeometry(QRect(230, 20, 230, 500))
        self.list_of_songs.currentTextChanged.connect(self.play_from_list)

    def time(self):  # Create time labels
        self.time_now = QLabel(self)  # Time of song
        self.time_now.move(490, 390)
        self.time_now.resize(35, 20)
        self.time_now.setStyleSheet("QLabel {font-size: 15px}")
        self.time_now.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.duration = QLabel(self)  # Duration of song
        self.duration.move(735, 390)
        self.duration.resize(35, 20)
        self.duration.setStyleSheet("QLabel {font-size: 15px}")
        self.duration.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def names(self):  # Create title and author labels
        self.name = QLabel(self)
        self.name.move(785, 430)
        self.name.resize(300, 20)
        self.name.setStyleSheet("QLabel {font-size: 17px}")
        self.name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.author = QLabel(self)
        self.author.move(785, 460)
        self.author.resize(300, 20)
        self.author.setStyleSheet("QLabel {font-size: 14px}")
        self.author.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def slider(self):
        self.slider_dur = QSlider(self)
        self.slider_dur.setOrientation(Qt.Horizontal)
        self.slider_dur.hide()
        self.slider_dur.move(540, 390)
        self.slider_dur.resize(165, 20)
        self.slider_dur.setMaximum(100)
        self.slider_dur.setMinimum(0)
        self.slider_dur.setTracking(False)
        self.slider_dur.sliderMoved.connect(self.slider_pos)

    def buttons(self):
        self.play = QPushButton(self)  # Play button
        self.play.resize(35, 35)
        self.play.move(585, 440)
        self.play.setIcon(QIcon("icons\\play-button.png"))
        self.play.setIconSize(QSize(35, 35))
        self.play.clicked.connect(self.func_play)

        self.volume_up = QPushButton(self)  # Volume_up button
        self.volume_up.resize(35, 35)
        self.volume_up.move(735, 440)
        self.volume_up.setIcon(QIcon("icons\\volume_up.png"))
        self.volume_up.setIconSize(QSize(35, 35))
        self.volume_up.clicked.connect(self.inc_volume)

        self.volume_down = QPushButton(self)  # Volume_down button
        self.volume_down.resize(35, 35)
        self.volume_down.move(685, 440)
        self.volume_down.setIcon(QIcon("icons\\volume_down.png"))
        self.volume_down.setIconSize(QSize(35, 35))
        self.volume_down.clicked.connect(self.dec_volume)

        self.next = QPushButton(self)  # Next song
        self.next.resize(35, 35)
        self.next.move(635, 440)
        self.next.setIcon(QIcon("icons\\next.png"))
        self.next.setIconSize(QSize(35, 35))
        self.next.clicked.connect(self.next_func)

        self.prev = QPushButton(self)  # Previous song or song to the beginning
        self.prev.resize(35, 35)
        self.prev.move(535, 440)
        self.prev.setIcon(QIcon("icons\\back.png"))
        self.prev.setIconSize(QSize(35, 35))
        self.prev.clicked.connect(self.prev_func)

        self.repeat = QPushButton(self)  # Repeat playlist
        self.repeat.resize(35, 35)
        self.repeat.move(485, 440)
        self.repeat.setIcon(QIcon("icons\\non-replay.png"))
        self.repeat.setIconSize(QSize(35, 35))
        self.repeat.clicked.connect(self.repeat_func)

    def menubar_create(self):  # Create menubar
        menubar = self.menuBar()
        menu = menubar.addMenu("File")
        menu.addAction(self.exit_action())
        menu.addAction(self.music_info())
        menu.addAction(self.open_song())
        menu.addAction(self.find_all())
        menu.addAction(self.change_logo())

    def exit_action(self):  # Menubar exit action
        exit_act = QAction("&Exit", self)
        exit_act.setShortcut("Ctrl+Q")
        exit_act.setStatusTip("Exit App")
        exit_act.triggered.connect(self.closeEvent)
        return exit_act

    def closeEvent(self, event):  # Exit player
        reply = QMessageBox.question(self, "Exit",
                                     "Are you sure to leave the best player ever", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            qApp.quit()
        else:
            try:
                event.ignore()
            except AttributeError:
                pass

    def music_info(self):  # Menubar song info action
        info_act = QAction("Music Info", self)
        info_act.setShortcut("Ctrl+I")
        info_act.setStatusTip("Displays Current Music Information")
        info_act.triggered.connect(self.display_info)
        return info_act

    def display_info(self):  # Music info
        metadata = self.player.availableMetaData()
        text = "<table><tr><th>Property</th><th>Value</th></tr> "  # Fulltext is html table
        for key in metadata:
            value = self.player.metaData(key)
            text = text + f"<tr><td>{key}</td><td>{str(value)}</td></tr>"
        text += "</table>"
        info_message = QMessageBox(self)
        info_message.setWindowTitle("Music Information")
        info_message.setText(text)
        info_message.addButton("OK", QMessageBox.AcceptRole)
        info_message.show()

    def open_song(self):  # Open song menubar action
        open_song_act = QAction("&Open file", self)
        open_song_act.setShortcut("Ctrl+M")
        open_song_act.setStatusTip("Open song")
        open_song_act.triggered.connect(self.open_song_func)
        return open_song_act

    def open_song_func(self):  # Open song function
        filename = QFileDialog.getOpenFileName(self, "Choose song",
                                               "", "Song(*.mp3)")[0]
        media = QUrl.fromLocalFile(filename)
        content = QMediaContent(media)
        self.playlist.clear()
        self.playlist.addMedia(content)
        self.player.setPlaylist(self.playlist)
        self.song()

    def find_all(self):  # Find all songs menubar action
        find_all_act = QAction("&Find all songs", self)
        find_all_act.setShortcut("Ctrl+J")
        find_all_act.setStatusTip("Find all")
        find_all_act.triggered.connect(self.find_all_func)
        return find_all_act

    def find_all_func(self):  # Find all songs function
        try:
            begin_dir_1 = open("dir.txt")
            begin_dir = begin_dir_1.readlines()[0]
            begin_dir_1.close()
            if os.path.exists(begin_dir):
                pass
            else:
                info_message = QMessageBox(self)
                info_message.setWindowTitle("Error Information")
                info_message.setText("Please enter existing starting direction in the dir.txt file")
                info_message.addButton("OK", QMessageBox.AcceptRole)
                info_message.show()
                return

        except FileNotFoundError:
            info_message = QMessageBox(self)
            info_message.setWindowTitle("Error Information")
            info_message.setText("Please create and enter starting direction in the dir.txt file")
            info_message.addButton("OK", QMessageBox.AcceptRole)
            info_message.show()
            return

        self.files = []
        self.folders = []

        for root, dirs, files in os.walk(begin_dir):
            for file in files:
                if file.endswith(".mp3"):
                    self.files.append(os.path.join(root, file))
                    self.folders.append(os.path.join(root, file).split("\\")[-2])

        self.folders = dict(zip(self.folders, self.folders)).values()
        self.list_of_songs.clear()
        self.list_of_folder.clear()

        for i in self.folders:
            self.list_of_folder.addItem(i.strip())

    def getfiles(self):  # Function of adding songs to list
        self.flag = False
        self.songs = []
        self.list_of_songs.clear()
        try:
            name_folder = self.list_of_folder.currentItem().text()

            for i in self.files:
                folder_1 = i.split('\\')[-2]
                if name_folder == folder_1.strip():
                    self.songs.append(i)
                    self.list_of_songs.addItem(i.split('\\')[-1])

        except AttributeError:
            pass
        self.flag = True

    def change_logo(self):  # Change logo menubar action
        change_act = QAction("&Change logo", self)
        change_act.setShortcut("Ctrl+B")
        change_act.setStatusTip("Change logo")
        change_act.triggered.connect(self.change_logo_action)
        return change_act

    def change_logo_action(self):  # Function that will change logo
        filename = QFileDialog.getOpenFileName(self, "Choose image",
                                               "", "Image(*.png, *.jpeg, *.bmp, *.jpg)")[0]
        if filename == "":
            pass
        else:
            self.image.setIcon(QIcon(filename))
            self.image.setIconSize(QSize(300, 300))

    def song(self):  # Displays song info
        self.time_now.setText("0:00")
        self.duration.setText(
            f"{int(self.player.duration() / 60000)}:{str(int((self.player.duration() / 1000) % 60)).rjust(2, '0')}")
        self.slider_dur.setRange(0, self.player.duration())
        self.title()

    def title(self):  # Title function
        metadata = self.player.availableMetaData()
        name = False
        author = False

        for key in metadata:
            if key == "Title":
                value = self.player.metaData(key)
                name = True
                self.name.setText(str(value))
            elif key == "Author":
                value = self.player.metaData(key)
                author = True
                self.author.setText(str(value[0]))

        if not name:
            self.name.setText(self.player.currentMedia().canonicalRequest().url().fileName())
        if not author:
            self.author.setText("Unknown")

    def play_from_list(self):  # Play songs from folder
        if self.flag:
            self.playlist.clear()
            selected_song = self.list_of_songs.currentRow()
            songs = self.songs[selected_song:] + self.songs[:selected_song]
            for i in songs:
                media = QUrl.fromLocalFile(i)
                content = QMediaContent(media)
                self.playlist.addMedia(content)
            self.player.setPlaylist(self.playlist)
            self.song()

    def func_play(self):  # Play
        if self.user_action == -1:
            self.slider_dur.show()
            self.song()
            self.player.play()
            self.play.setIcon(QIcon("icons\\pause.png"))
            self.play.setIconSize(QSize(35, 35))
            self.user_action = 1
            return

        elif self.user_action == 1:
            self.player.pause()
            self.play.setIcon(QIcon("icons\\play-button.png"))
            self.play.setIconSize(QSize(35, 35))
            self.user_action = -1
            return

    def inc_volume(self):  # Increase volume
        vol = self.player.volume()
        vol = min(vol + 5, 100)  # If vol > 100: vol = 100
        self.player.setVolume(vol)

    def dec_volume(self):  # Decrease volume
        vol = self.player.volume()
        vol = max(vol - 5, 0)  # If vol < 0: vol = 0
        self.player.setVolume(vol)

    def next_func(self):  # Next song
        try:
            self.player.playlist().next()
        except AttributeError:
            pass

    def prev_func(self):  # Previous song
        try:
            if self.time_now.text() != "0:00":
                self.player.setPosition(0)
            else:
                self.player.playlist().previous()
        except AttributeError:
            pass

    def repeat_func(self):  # Repeat function
        if self.repeat_flag:
            self.repeat_flag = False
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
            self.repeat.setIcon(QIcon("icons\\non-replay.png"))
            self.repeat.setIconSize(QSize(35, 35))
        else:
            self.repeat_flag = True
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
            self.repeat.setIcon(QIcon("icons\\replay.png"))
            self.repeat.setIconSize(QSize(35, 35))

    def change_time(self, position, send_type=False):  # Change song time_now
        if not send_type:
            self.slider_dur.setValue(position)
        self.duration.setText(
            f"{int(self.player.duration() / 60000)}:{str(int((self.player.duration() / 1000) % 60)).rjust(2, '0')}")
        self.time_now.setText(
            f"{int(position / 60000)}:{str(int((position / 1000) % 60)).rjust(2, '0')}")
        self.title()
        self.slider_dur.setRange(0, self.player.duration())

    def change_butt(self):  # Change button play
        if self.player.state() == QMediaPlayer.StoppedState:
            self.player.stop()
            self.play.setIcon(QIcon("icons\\play-button.png"))
            self.play.setIconSize(QSize(35, 35))
            self.user_action = -1

    def slider_pos(self, position):  # Seeking position of slider
        pos = self.sender()
        if isinstance(pos, QSlider):
            if self.player.isSeekable():
                self.player.setPosition(position)


if __name__ == "__main__":
    main()
