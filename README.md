# PyBrow

PyBrow is a lightweight, tabbed web browser built using Python and the PyQt5 framework. It leverages the QtWebEngine to provide a functional browsing experience with integrated bookmark management and download tracking.

## Features

* **Tabbed Browsing**: Open multiple websites simultaneously with an easy-to-use tab interface.
* **Bookmark Management**: Save your favorite URLs to a local JSON file and access them through a dedicated bookmarks window.
* **Navigation Tools**: Standard browser controls including Back, Forward, Reload, and Home buttons.
* **Custom Homepage**: Set a custom local file or URL as your default startup page.
* **Download Management**: Automatically creates and links to a local Downloads folder for organized file saving.

## Getting Started

### Prerequisites

* Python 3.x
* PyQt5
* PyQtWebEngine

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/pybrow.git](https://github.com/yourusername/pybrow.git)
    cd pybrow
    ```

2.  **Install dependencies:**
    ```bash
    pip install PyQt5 PyQtWebEngine
    ```

### Usage

Run the application using the following command:
```bash
python PyBrow.py
Navigation and Controls

Address Bar: Enter a URL and press Enter to navigate. The browser automatically prepends "http://" if it is missing.

New Tab: Click the "+" button in the toolbar to open a new tab.

Close Tab: Click the "x" on any tab to close it.

Bookmarks:

Click Bookmark to save the current page.

Click View Bookmarks to see your saved list and launch them in new tabs.

File Structure
PyBrow.py: The main application logic and UI definition.

bookmarks.json: Automatically generated file where your bookmarks are stored.

Downloads/: A local directory created by the app to store downloaded files.

License
MIT
