import pyttsx3
import threading
import time
import sys
import sqlite3


def type(str):
    for i in range(len(str)):
        time.sleep(.090)
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

get_user_name(conn)





# print("""
#         AAAAAAA     TTTTTTT     U     U     SSSSSSS     AAAAAAA
#         A     A        T        U     U     SS          A     A
#         AAAAAAA        T        U     U      SS         AAAAAAA
#         A     A        T         U   U         SSS      A     A
#         A     A        T           U         SSSSSS     A     A  
# """)

