# Journal Downloader - Psychology Issues Scraper

Python application with GUI for downloading issues of the journal *"Ψυχολογία"* from the Panteion University digital archive.

---

## What it does

- Scrapes journal volumes from an online archive
- Extracts available PDF links for each volume
- Downloads selected issues automatically
- Organizes files into folders by volume
- Provides a Tkinter GUI for user interaction
- Uses multithreading for smooth download progress UI

---

## Features

- GUI-based selection of volumes (Tkinter)
- Bulk download or selective download
- Automatic folder organization per volume
- Progress bar during downloads
- Image preview in GUI
- Handles invalid filenames automatically
- Multithreaded downloading (non-blocking UI)

---

## Technologies Used

- Python
- Tkinter (GUI)
- Requests
- BeautifulSoup (HTML parsing)
- urllib
- threading
- PIL (Pillow)

---

## How it works

1. The program starts from the main journal page
2. It scrapes available volumes and their links
3. The user selects:
   - all volumes, or
   - specific volumes via GUI input
4. The scraper navigates pages and extracts PDF links
5. Files are downloaded and saved locally in structured folders

---

## Run the project

```bash
pip install requests beautifulsoup4 pillow
python main.py
