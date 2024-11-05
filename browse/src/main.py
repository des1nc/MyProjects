import sys
import sqlite3
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, 
    QWidget, QLabel, QMessageBox, QTabWidget, QHBoxLayout, QCheckBox, 
    QComboBox, QColorDialog, QDialog
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from adblockparser import AdblockRules


def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return False 
    finally:
        conn.close()
    
    return True  

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, password))
    user = cursor.fetchone()
    
    conn.close()
    return user  


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        
        create_database()

        
        self.setWindowTitle('TZ browser')
        self.setGeometry(100, 100, 1200, 800)

        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        
        self.add_text_tab() 

        
        self.user_label = QLabel("Пользователь: Не вошел в систему")
        self.tabs.addTab(self.user_label, "Пользователь")

    
        self.toolbar = self.addToolBar('Toolbar')
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск или URL")
        self.search_button = QPushButton("Поиск")
        self.search_button.clicked.connect(self.perform_search)
        self.search_input.returnPressed.connect(self.perform_search)  
        self.toolbar.addWidget(self.search_input)

        self.login_button = QPushButton('Войти / Зарегистрироваться')
        self.login_button.clicked.connect(self.open_login_dialog)
        self.toolbar.addWidget(self.login_button)

        self.settings_button = QPushButton('Настройки')
        self.settings_button.clicked.connect(self.open_settings)
        self.toolbar.addWidget(self.settings_button)

        
        self.new_tab_button = QPushButton('+')
        self.new_tab_button.setFixedSize(30, 30)
        self.new_tab_button.clicked.connect(self.add_new_tab)
        self.toolbar.addWidget(self.new_tab_button)
        
        
        self.tabs.tabBar().setMovable(True)
        self.tabs.tabBar().setTabsClosable(True)
        self.tabs.tabBar().tabCloseRequested.connect(self.close_current_tab)
        
        
        self.adblock_enabled = False
        with open('easylist.txt', 'r', encoding='utf-8') as f:
            rules = f.readlines()
        self.adblock_rules = AdblockRules(rules)

        
        self.apply_style()

    def add_text_tab(self):
        text_widget = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel("Akhmatov Browser")
        title_label.setAlignment(Qt.AlignCenter) 
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #3f51b5;") 
        layout.addWidget(title_label)
        text_widget.setLayout(layout)
        self.tabs.addTab(text_widget, "Главная")

    def add_browser_tab(self, url):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        self.tabs.addTab(browser, "Новая вкладка")

    def add_new_tab(self):
        self.add_browser_tab("http://www.google.com")  

    def close_current_tab(self, index):
        if index > 0: 
            self.tabs.removeTab(index)

    def perform_search(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            url = self.search_input.text()
            
            if not url.startswith('http'):
                url = 'http://' + url
            if self.adblock_enabled:
                self.block_ads(url)
            current_tab.setUrl(QUrl(url))

    def open_settings(self):
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.exec_()

    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5; /* Цвет фона */
            }
            QLineEdit {
                border: 2px solid #3f51b5; /* Цвет границы */
                border-radius: 10px; /* Закруглённые края */
                padding: 5px; /* Отступы внутри */
            }
            QPushButton {
                background-color: #3f51b5; /* Цвет кнопки */
                color: white; /* Цвет текста */
                border-radius: 10px; /* Закруглённые края */
                padding: 10px; /* Отступы внутри */
            }
            QLabel {
                font-size: 16px; /* Размер шрифта */
                color: #333; /* Цвет текста */
            }
        """)

    def open_login_dialog(self):
       
        login_tab = QWidget()
        layout = QVBoxLayout()

        username_input = QLineEdit()
        username_input.setPlaceholderText("Имя пользователя")
        layout.addWidget(username_input)

        password_input = QLineEdit()
        password_input.setPlaceholderText("Пароль")
        password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_input)

        login_button = QPushButton('Войти')
        layout.addWidget(login_button)

        register_button = QPushButton('Зарегистрироваться')
        layout.addWidget(register_button)

        login_button.clicked.connect(lambda: self.login(username_input.text(), password_input.text()))
        register_button.clicked.connect(lambda: self.register(username_input.text(), password_input.text()))

        login_tab.setLayout(layout)
        self.tabs.addTab(login_tab, "Вход / Регистрация")

    def login(self, username, password):
        user = authenticate_user(username, password)
        
        if user:
            self.user_label.setText(f"Пользователь: {username}")
            QMessageBox.information(self, 'Успех', 'Вы вошли в систему!')
            self.tabs.removeTab(self.tabs.indexOf(self.tabs.currentWidget())) 
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверное имя пользователя или пароль')

    def register(self, username, password):
        if register_user(username, password):
            QMessageBox.information(self, 'Успех', 'Регистрация прошла успешно!')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пользователь с таким именем уже существует')

    def block_ads(self, url):
        if any(self.adblock_rules.should_block(url)):
            QMessageBox.information(self, 'AdBlock', 'Заблокирована реклама на странице')

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)

        self.setWindowTitle("Настройки")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

       
        self.vpn_checkbox = QCheckBox("Включить VPN")
        layout.addWidget(self.vpn_checkbox)

       
        proxy_label = QLabel("Прокси сервер (URL):")
        self.proxy_input = QLineEdit()
        layout.addWidget(proxy_label)
        layout.addWidget(self.proxy_input)

       
        self.adblock_checkbox = QCheckBox("Включить AdBlocker")
        layout.addWidget(self.adblock_checkbox)

       
        self.theme_label = QLabel("Выберите тему:")
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Светлая", "Тёмная", "Материал"])
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combobox)

       
        self.color_button = QPushButton("Выбрать цвет фона")
        self.color_button.clicked.connect(self.choose_color)
        layout.addWidget(self.color_button)

       
        apply_button = QPushButton("Применить")
        apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(apply_button)

        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.parent().setStyleSheet(f"QMainWindow {{ background-color: {color.name()}; }}")

    def apply_settings(self):
        vpn_enabled = self.vpn_checkbox.isChecked()
        proxy_server = self.proxy_input.text()
        adblock_enabled = self.adblock_checkbox.isChecked()
        selected_theme = self.theme_combobox.currentText()

       
        if vpn_enabled:
            QMessageBox.information(self, 'VPN', 'VPN включен (требуется настройка стороннего VPN-клиента)')
        if proxy_server:
            QMessageBox.information(self, 'Proxy', f'Прокси установлен: {proxy_server}')

 
        self.parent().adblock_enabled = adblock_enabled

 
        if selected_theme == "Тёмная":
            self.parent().setStyleSheet("QMainWindow { background-color: #333; color: white; }")
        elif selected_theme == "Светлая":
            self.parent().setStyleSheet("QMainWindow { background-color: white; color: black; }")
        elif selected_theme == "Материал":
            self.parent().apply_style()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
