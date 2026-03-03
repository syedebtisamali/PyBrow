from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLineEdit, QToolBar, QAction,
    QFileDialog, QPushButton, QLabel
)
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, QFile
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem, QWebEngineProfile, QWebEnginePage
import sys
import json
import os
from urllib.parse import urlparse

class API:
    def __init__(self):
        self.homepage = "https://www.google.com"
        self.bookmarks_file = "bookmarks.json"
        self.downloads_folder = os.path.join(os.getcwd(), "Downloads")
        if not os.path.exists(self.downloads_folder):
            os.makedirs(self.downloads_folder)

    def save_bookmark(self, url):
        bookmarks = self.load_bookmarks()
        if url not in bookmarks:
            bookmarks.append(url)
            with open(self.bookmarks_file, "w") as f:
                json.dump(bookmarks, f)

    def load_bookmarks(self):
        if os.path.exists(self.bookmarks_file):
            with open(self.bookmarks_file, "r") as f:
                return json.load(f)
        return []

    def save_homepage(self, url):
        self.homepage = url

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api = API()
        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)
        self.setCentralWidget(self.tabs)

        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        back_btn = QAction("Back", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        bookmark_btn = QAction("Bookmark", self)
        bookmark_btn.triggered.connect(self.bookmark_page)
        navtb.addAction(bookmark_btn)

        view_bookmarks_btn = QAction("View Bookmarks", self)
        view_bookmarks_btn.triggered.connect(self.view_bookmarks)
        navtb.addAction(view_bookmarks_btn)

        download_btn = QAction("Downloads", self)
        download_btn.triggered.connect(self.show_downloads_folder)
        navtb.addAction(download_btn)

        navtb.addSeparator()

        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.clicked.connect(self.add_blank_tab)
        navtb.addWidget(self.new_tab_btn)

        self.add_new_tab(QUrl(self.api.homepage), "Home")

        self.set_homepage_btn = QAction("Set Homepage", self)
        self.set_homepage_btn.triggered.connect(self.set_homepage)
        navtb.addAction(self.set_homepage_btn)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None or isinstance(qurl, int):
            qurl = QUrl(self.api.homepage)

        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.urlChanged.connect(self.update_url_bar)
        browser.loadFinished.connect(self.update_tab_title)

        self.tabs.addTab(browser, label)

    def add_blank_tab(self):
        self.add_new_tab(QUrl(self.api.homepage), "New Tab")

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def update_tab_title(self):
        # Get the current browser widget
        browser = self.tabs.currentWidget()
        
        if isinstance(browser, QWebEngineView):
            title = browser.page().title()
            
            if not title:  # If there's no title, fallback to domain
                url = browser.url().toString()
                parsed_url = urlparse(url)
                title = parsed_url.netloc  # Use domain name if no title is found
            
            current_index = self.tabs.indexOf(browser)
            self.tabs.setTabText(current_index, title)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl(self.api.homepage))

    def navigate_to_url(self):
        url = self.urlbar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_url_bar(self, q):
        browser = self.tabs.currentWidget()
        if isinstance(browser, QWebEngineView):
            self.urlbar.setText(browser.url().toString())

    def bookmark_page(self):
        url = self.tabs.currentWidget().url().toString()
        self.api.save_bookmark(url)

    def view_bookmarks(self):
        bookmarks = self.api.load_bookmarks()
        self.bookmarks_window = QWidget()
        self.bookmarks_window.setWindowTitle("Bookmarks")
        layout = QVBoxLayout()
        for url in bookmarks:
            btn = QPushButton(url)
            btn.clicked.connect(lambda _, u=url: self.open_bookmark(u))
            layout.addWidget(btn)
        self.bookmarks_window.setLayout(layout)
        self.bookmarks_window.show()

    def open_bookmark(self, url):
        self.add_new_tab(QUrl(url), "Bookmark")
        self.bookmarks_window.close()

    def show_downloads_folder(self):
        QFileDialog.getOpenFileName(self, "Open Downloads Folder", self.api.downloads_folder)

    def set_homepage(self):
        homepage, ok = QFileDialog.getOpenFileName(self, "Select Homepage URL")
        if ok:
            self.api.save_homepage(homepage)
            self.navigate_home()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
