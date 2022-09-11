from telethon import functions, types
from telethon.sync import TelegramClient
from telethon import TelegramClient, sync
from telethon import TelegramClient, events, sync
from telethon.sync import connection
import numpy as np
import csv
import pandas as pd
import openpyxl
import random
import string
from telethon.tl.types import PeerChannel
from telethon.tl.functions.channels import JoinChannelRequest

# api_id = 15858753 # 
# api_hash = "0945911118c83526d25e0522e46df219" # 

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    #print("Random string of length", length, "is:", rand_string)
    return rand_string

random_string = generate_random_string(5)

filepath = """/home/platon/"""+random_string+""".xlsx"""
wb = openpyxl.Workbook()

wb.save(filepath)

server = 'www.mihan--server.yoga'
port = 443
secret = 'dd00000000000000000000000000000000'

api_id = 9822367
api_hash = 'ef86edf2f2b6a418614061d4997a17bb'
#connection = connection.ConnectionTcpMTProxyRandomizedIntermediate # this mode supports most proxies
client = TelegramClient('pars_vulk', api_id, api_hash)#, connection=connection, proxy=(server, port, secret))
client.connect()
client.start()
url = input("Введите ссылку на канал: ")
id_first = input("введите id канала:")

i = 0
#url = "https://t.me/rtv_igor"
#id_first =1642640051
first_channel = url[url.find("e/") + 2:]
id_first = int(id_first)
channels_fake = []
channels_fake.append(id_first)
channels = []
channels.append(first_channel)
channels.insert(0, ' ')
x_x = np.zeros((1, 1), dtype= int, order='F')
matrix = []
numOperation = 0

client(JoinChannelRequest(url))
@client.on(events.NewMessage(outgoing=True, incoming = True))#outgoing=False))#chats=channels[1:])) # список каналов, откуда будем брать посты
async def normal_handler(event):
    global x_x
    global matrix
    global numOperation
    global df
    global matrix_small
    if isinstance(event.chat, types.Channel):
        try:
            chan_ex = event.message.peer_id.channel_id
            id_new = event.message.fwd_from.from_id.channel_id
            chat1 = await client.get_entity(PeerChannel(chan_ex))
            name_ex = chat1.username
            last_name = str(name_ex)
            chat2 = await client.get_entity(PeerChannel(id_new))
            chat_name = chat2.username
            name = str(chat_name) 
            new_name = "https://t.me/" + str(chat_name)
            await client(JoinChannelRequest(new_name))
            name_fake =  id_new
            count_chat = len(channels_fake) - 1
            if channels_fake.count(name_fake) == 0: 
                    channels.append(name)
                    channels_fake.append(name_fake)
                    numOperation += 1
                    count_chat = len(channels) - 1
                    if numOperation > 1:
                        x_x = matrix[1:, 1:]
                    pos = channels_fake.index(chan_ex)
                    zeros1 = np.zeros((count_chat - 1, 1))
                    zeros1[pos][0] = 1
                    zeros2 = np.zeros((1, count_chat))
                    zeros2[0][pos] = 1
                    m1 = np.concatenate((x_x, zeros1), axis = 1)
                    m2 = np.concatenate((m1, zeros2), axis = 0)
                    x_x = m2
                    mas1 = np.concatenate((np.expand_dims(np.array(channels[1:], dtype = str), axis = 0), m2), axis=0)
                    matrix = np.concatenate((np.expand_dims(np.array(channels, dtype = str), axis = 1), mas1), axis=1)
                    matrix_small = matrix[1:, :][:, 1:]
                    df = pd.DataFrame(matrix)
                    df.to_excel(excel_writer = filepath)
                    print(matrix)
                    print('first')
            else:
                    pos = channels_fake.index(chan_ex)
                    position = channels_fake.index(id_new)
                    matrix_small[pos][position] = str(float(matrix_small[pos][position]) + 1)
                    matrix_small[position][pos] = str(float(matrix_small[position][pos]) + 1)
                    print(matrix_small)
                    print('repeat')
        except:
                    print('пост или пересланное сообщение')
                    #print(event)
                    #nickname = event.chat.username
                    #nickname=str(nickname)
                    #sms = event.chat.message
        			#await client.forward_messages("https://t.me/taskVulk", sms)
        			#await client.forward_messages("https://t.me/rtv_igor", nickname)
            
            
        # print(channels)
    
client.run_until_disconnected()
channels = []