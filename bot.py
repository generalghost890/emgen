import re
import requests as re
from telethon import TelegramClient, events
from telethon.tl.custom import InlineKeyboardButton, InlineKeyboardMarkup
import wget
import os

buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('صنع جيميل', b'generate'),
            InlineKeyboardButton('اعادة تحميل', b'refresh'),
            InlineKeyboardButton('اغلاق', b'close')
        ]
    ]
)

msg_buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('اظهار الرسائل', b'view_msg'),
            InlineKeyboardButton('اغلاق', b'close')
        ]
    ]
)

client = TelegramClient('Temp-Mail Bot', api_id, api_hash).start(bot_token=bot_token)

email = ''


@client.on(events.NewMessage)
async def start_msg(event):
    message = event.message
    await message.reply("مرحبا " + message.sender.first_name + ", \n @mysterymailbot is a free service that allows to generates and receive emails at a temporary address that self-destructed after a certain time elapses.")
    await message.reply("اصنع ايميل جديد الان !", buttons=buttons)


@client.on(events.CallbackQuery)
async def mailbox(event):
    query = event.query
    response = query.data.decode()
    if response == 'generate':
        global email
        email = re.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
        await query.edit('__ايميلك المؤقت: __`' + str(email) + '`', buttons=buttons)
        print(email)
    elif response == 'refresh':
        print(email)
        try:
            if email == '':
                await query.edit('اصنع ايميل جديد', reply_markup=buttons)
            else:
                getmsg_endp = "https://www.1secmail.com/api/v1/?action=getMessages&login=" + email[:email.find("@")] + "&domain=" + email[
                                                                                                                             email.find(
                                                                                                                                 "@") + 1:]
                print(getmsg_endp)
                ref_response = re.get(getmsg_endp).json()
                global idnum
                idnum = str(ref_response[0]['id'])
                from_msg = ref_response[0]['from']
                subject = ref_response[0]['subject']
                refreshrply = 'You a message from ' + from_msg + '\n\nSubject : ' + subject
                await query.edit(refreshrply, reply_markup=msg_buttons)
        except:
            await query.answer('لم يتم الحصول على اي رسائل في صندوق بريدك' + email)
    elif response == 'view_msg':
        msg = re.get(
            "https://www.1secmail.com/api/v1/?action=readMessage&login=" + email[:email.find("@")] + "&domain=" + email[
                                                                                                                  email.find(
                                                                                                                      "@") + 1:] + "&id=" + idnum).json()
        print(msg)
        from_mail = msg['from']
        date = msg['date']
        subjectt = msg['subject']
        try:
            attachments = msg['attachments'][0]
        except:
            pass
        body = msg['body']
        mailbox_view = 'ID No : ' + idnum + '\nFrom : ' + from_mail + '\nDate : ' + date + '\nSubject : ' + subjectt + '\nmessage : \n' + body
        await query.edit(mailbox_view, reply_markup=buttons)
        mailbox_view = 'ID No : ' + idnum + '\nFrom : ' + from_mail + '\nDate : ' + date + '\nSubject : ' + subjectt + '\nmessage : \n' + body
        if attachments == "[]":
            await query.edit(mailbox_view, reply_markup=buttons)
            await query.answer("No Messages Were Recieved..", show_alert=True)
        else:
            dlattach = attachments['filename']
            attc = "https://www.1secmail.com/api/v1/?action=download&login=" + email[:email.find("@")] + "&domain=" + email[
                                                                                                                      email.find(
                                                                                                                          "@") + 1:] + "&id=" + idnum + "&file=" + dlattach
            print(attc)
            mailbox_vieww = 'ID No : ' + idnum + '\nFrom : ' + from_mail + '\nDate : ' + date + '\nSubject : ' + subjectt + '\nmessage : \n' + body + '\n\n' + '[Download](' + attc + ') Attachments'
            filedl = wget.download(attc)
            await query.edit(mailbox_vieww, reply_markup=buttons)
            os.remove(dlattach)
    elif response == 'close':
        await query.edit('تم اغلاق الجلسة')


client.run_until_disconnected()
