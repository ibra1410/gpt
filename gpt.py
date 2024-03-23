from telegram import Updater
from telegram.ext import MessageHandler, Filters
import requests
import json

# تعريف الوظيفة للتفاعل مع خادم GPT
def gpt(message):
    url = 'https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta'
    headers = {
        'Host': 'us-central1-chat-for-chatgpt.cloudfunctions.net',
        'Connection': 'keep-alive',
        'If-None-Match': 'W/"1c3-Up2QpuBs2+QUjJl/C9nteIBUa00"',
        'Accept': '*/*',
        'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/15.6.1 hw/iPhone8_2',
        'Content-Type': 'application/json',
        'Accept-Language': 'en-GB,en;q=0.9'
    }
    data = {
        'data': {
            'message': message,
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        result = response.json()["result"]["choices"][0]["text"]
        return result
    except Exception as e:
        print("Error:", e)
        return None

# تعريف الدالة التي تستجيب لرسائل المستخدمين
def reply(update, context):
    # الحصول على الرسالة من المستخدم
    user_message = update.message.text
    # الحصول على الرد من خادم GPT
    gpt_response = gpt(user_message)
    # إرسال الرد إلى المستخدم في تليجرام
    if gpt_response:
        update.message.reply_text(gpt_response)
    else:
        update.message.reply_text("Sorry, I couldn't process your request.")

def main():
    # تهيئة بوت تليجرام
    updater = Updater("6658939432:AAFAO3xXHDq_ecjJ_L65-CGlNojAeMsLi-4", use_context=True)
    dp = updater.dispatcher
    # تحديد الدالة التي تستجيب لرسائل المستخدمين
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
    # بدء البوت والاستماع للرسائل الواردة
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
