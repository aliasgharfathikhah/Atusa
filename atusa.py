import pyttsx3
import threading
import time
import sys
import sqlite3
import requests
from dotenv import load_dotenv
import os
import speedtest
import cv2

def type(str):
    for i in range(len(str)):
        time.sleep(.08)
        print(str[i], end='')
        sys.stdout.flush()
    print()

def To_Speak(string):
    engine = pyttsx3.init()
    engine.setProperty('rate', 115)
    engine.setProperty('volume', 100.0) 
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(string)
    engine.runAndWait()

def Start_Speak(string):
    t1 = threading.Thread(target=type, args=(string,))
    t2 = threading.Thread(target=To_Speak, args=(string,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

def create_or_connect_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_info (
            name TEXT
        );
    """)

db_name = "my_memory.db"
conn = create_or_connect_db(db_name)
create_table_if_not_exists(conn)

def insert_or_get_user_name(conn, user_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM user_info WHERE name = ?", (user_name,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO user_info (name) VALUES (?)", (user_name,))
        conn.commit()
        Start_Speak(f"Oh very good, hi {user_name}")
        return user_name
    else:
        return result[0]

def get_user_name(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM user_info")
    result = cursor.fetchone()
    if result is None:
        Start_Speak("Hello, I am Atusa and this is my first meeting with you. can you tell me your name »")
        user_name = input()
        name = insert_or_get_user_name(conn, user_name)
    else:
        Start_Speak(f"Hello {result[0]}, how can I help you?")

def GPT(content):

    url = "https://api.openai.com/v1/chat/completions"

    message = {
        'role': 'system',
        'content': content
    }

    load_dotenv()
    secret_key = os.getenv('SECRET-KEY-IN-OPENAI')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + secret_key
    }

    data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [message]
    }

    response = requests.post(url, headers=headers, json=data)

    response_json = response.json()

    message_content = response_json['choices'][0]['message']['content']
    message_content = message_content.replace('OpenAI', 'ZIG ZAG Company').replace('GPT-3', 'AFZ-1').replace('Assistant', 'Atusa')
    Start_Speak(message_content)

get_user_name(conn)

def SpeedtestInternet():
    Start_Speak('A few moments')

    speed = speedtest.Speedtest()
    download__speed = speed.download()
    strd = f'{round(download__speed/1_000_000, 2)} Mbps'
    
    speed = speedtest.Speedtest()
    upload__speed = speed.upload()
    stru = f'{round(upload__speed/1_000_000, 2)} Mbps'


    Start_Speak('download speed >')
    Start_Speak(strd)
    Start_Speak('Upload speed >')
    Start_Speak(stru)

def Taking_Selfie():
    Start_Speak('Get ready')
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    ret, frame = cap.read()
    cv2.imshow('preview', frame)
    Start_Speak('It looks great')
    cv2.imwrite('selfie.jpg', frame)
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()

def System_Operation(string):
    string.lower()
    if 'internet speed' in string:
        SpeedtestInternet()
        return False
    elif 'take photo' in string or 'take selfi' in string:
        Taking_Selfie()
        return False

while True:
    text_input = input()
    
    if System_Operation(text_input):        
        GPT(text_input)




# print("""
#         AAAAAAA     TTTTTTT     U     U     SSSSSSS     AAAAAAA
#         A     A        T        U     U     SS          A     A
#         AAAAAAA        T        U     U      SS         AAAAAAA
#         A     A        T         U   U         SSS      A     A
#         A     A        T           U         SSSSSS     A     A  
# """)

