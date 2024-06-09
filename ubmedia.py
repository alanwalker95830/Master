from pyrogram import *
from pyrogram.types import *
from apscheduler.schedulers.background import BackgroundScheduler
import os
from os import getenv


#---------------------------------+ heroku
api_id_pyrogram = int(getenv("API_ID"))
api_hash_pyrogram = getenv("API_HASH")
string_pyrogram = getenv("SESSION_STRING")
g_time = int(getenv("GROUP_DELETE_TIME"))
c_time = int(getenv("CHANNEL_DELETE_TIME"))
group =int(getenv("NEW_GROUP"))
channel =int(getenv("NEW_CHANNEL"))

#------------------------------------end
idss = []


app = Client(name="auto-delete",session_string =string_pyrogram, api_id=api_id_pyrogram, api_hash=api_hash_pyrogram, sleep_threshold=60)

    
    
def clean_data():
    print("checking media")
    idss = []
    for message in app.search_messages(chat_id=group, filter=enums.MessagesFilter.PHOTO_VIDEO, limit=3):
        msg_id = message.id
        idss.append(msg_id)
        app.copy_message(chat_id=channel, from_chat_id=group, message_id=msg_id)
        app.delete_messages(chat_id=group, message_ids=msg_id)
    else:
        if len(idss) == 0:
            print("no photos to delete")
            return
        else:
            c = len(idss)
            print(f"cleared almost {c} messages")
            idss.clear() 

    
def channel_delete():
    print("trying to delete channel messages")
    for message in app.search_messages(chat_id=channel, filter=enums.MessagesFilter.PHOTO_VIDEO):
        msg_id = message.id
        idss.append(msg_id)
        app.delete_messages(chat_id=channel, message_ids=msg_id)
    else:
        if len(idss) == 0:
            print("no photos to delete")
            return
        else:
            c = len(idss)
            print(f"almost {c} files deleted")
            idss.clear() 

    
    
scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.add_job(clean_data, 'interval' , seconds=g_time)


scheduler.start()   

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.add_job(channel_delete, 'interval' , minutes=c_time)


scheduler.start()  





app.run()
