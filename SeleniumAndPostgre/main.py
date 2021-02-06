import psycopg2
from psycopg2 import Error
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

url = "https://www.youtube.com/live_chat?is_popout=1&v=5qap5aO4i9A"
browser = webdriver.Chrome(ChromeDriverManager().install())
time.sleep(15)
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
messages = soup.find_all("yt-live-chat-text-message-renderer")

user = list()
for message in messages:
    content = message.find("div", {"id": "content"})
    message_content = content.find("span", {"id": "message"}).text
    yazar = content.find("span", {"id": "author-name"}).text
    if yazar == "ChilledCow":
        continue
    user.append([yazar, message_content])

print(user)
browser.close()
try:
    connection = psycopg2.connect(user="postgres",
                                  password="---",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="User")
    print("Database'e başarıyla bağlanıldı")
    cursor = connection.cursor()
    for kullanıcı in user:
        insert_query = """ INSERT INTO kullanici (kullaniciadi, kisisel) VALUES (%s, %s)"""
        item_tuple = (kullanıcı[0], kullanıcı[1])
        cursor.execute(insert_query, item_tuple)
        connection.commit()
        print("Başarı ile eklendi.")


except (Exception, Error) as error:
    print("Bağlanırken Hata İle Karşılaşıldı...", error)

