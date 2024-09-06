from selenium_youtube import Youtube

# pip install selenium_firefox
from selenium_firefox import Firefox
firefox = Firefox()

# pip install selenium_chrome
# from selenium_chrome import Chrome
# chrome = Chrome()

youtube = Youtube(
    browser=chrome # or firefox
)

VIDEO_FILE = 'D:\\DEV\\MoneyPrinterTurbo\\storage\\tasks\\Epictetus Discourses 2.5.4–5\\final-1.mp4'

upload_result = youtube.upload(VIDEO_FILE, 'Hahah title', 'description', ['tag1', 'tag2'])