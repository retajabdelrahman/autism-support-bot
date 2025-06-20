import telebot
import openai
import threading
import random
from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask

# إنشاء تطبيق ويب صغير لإبقاء Replit نشطًا
app = Flask(__name__)

@app.route('/')
def home():
    return "بوت التوحد يعمل بنجاح 🚀"

# 🔹 أدخل مفاتيحك هنا
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")



# إعداد البوت
bot = telebot.TeleBot(TOKEN)

# تهيئة OpenAI API
openai.api_key = OPENAI_API_KEY

# قائمة نصائح عن التوحد
tips = [
    "💡 التوحد ليس مرضًا، بل اختلاف في طريقة عمل الدماغ. كن داعمًا ومتفهمًا. 🤝",
    "🎯 الأطفال المصابون بالتوحد قد يعانون من حساسية زائدة للأصوات أو الأضواء. حاول توفير بيئة هادئة لهم. 🌿",
    "📚 من المفيد استخدام الصور والقصص المصورة لمساعدة الأطفال المصابين بالتوحد على فهم المواقف الاجتماعية. 🖼️",
    "🗣️ بعض الأطفال المصابين بالتوحد لا يتحدثون، لكن يمكنهم التواصل بطرق أخرى مثل الإشارات أو التطبيقات المخصصة. 📱",
    "❤️ الدعم والتفهم من الأسرة والمجتمع يساعد الأشخاص المصابين بالتوحد على تحقيق إمكانياتهم الكاملة. 🌟"
]

# قائمة قصص نجاح ملهمة
stories = [
    "🌟 **تمبل جراندين** - كانت طفلة مصابة بالتوحد ولم تكن تتحدث حتى عمر 4 سنوات، لكنها أصبحت عالمة مشهورة في سلوك الحيوانات ومتحدثة عالمية عن التوحد! 🧠",
    "💙 **جايك بارنيت** - تم تشخيصه بالتوحد في عمر سنتين، لكنه أصبح فيزيائيًا عبقريًا والتحق بالجامعة في سن 10 سنوات! 📚",
    "🚀 **إليجاه ماكواي** - طفل متوحد أصبح مهندسًا ومخترعًا وساهم في تطوير أنظمة التشحيم للقطارات! 🏗️",
    "🎨 **ستيفن ويلتشير** - فنان موهوب مصاب بالتوحد يمكنه رسم مدن كاملة بتفاصيل دقيقة من الذاكرة فقط! 🏙️",
    "🎵 **ديريك بارافيتشيني** - موسيقي كفيف مصاب بالتوحد، لكنه يستطيع عزف أي أغنية من مرة واحدة فقط بسماعه لها! 🎹"
]

# أمر /start
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = """
🤖 *مرحبًا! أنا AutismSupportBot*  
أنا هنا لمساعدتك في الإجابة على أي أسئلة حول التوحد. 😊  
💡 يمكنك سؤالي عن الأعراض، طرق العلاج، أو أي استفسار آخر.  
🔹 *مثال للأسئلة:*  
- ما هو التوحد؟  
- كيف أتعامل مع طفل مصاب بالتوحد؟  
- هل هناك علاج للتوحد؟  

📝 استخدم الأوامر التالية:  
🔹 `/tip` → احصل على نصيحة عن التوحد  
📖 `/story` → استمع إلى قصة نجاح ملهمة  
📩 *ارسل سؤالك الآن!*  
    """
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

# أمر /tip لإرسال نصيحة عشوائية
@bot.message_handler(commands=['tip'])
def send_tip(message):
    bot.send_message(message.chat.id, random.choice(tips))

# أمر /story لإرسال قصة نجاح ملهمة
@bot.message_handler(commands=['story'])
def send_story(message):
    bot.send_message(message.chat.id, random.choice(stories))

# الرد على أي رسالة نصية باستخدام ChatGPT
@bot.message_handler(content_types=['text'])
def gptMessage(message):
    user_message = message.text  

    try:
        # إرسال الطلب إلى OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أجب بنفس لغة المستخدم وبأسلوب واضح وسهل."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_response = response["choices"][0]["message"]["content"]

        # إرسال الإجابة مع تنسيق جميل وزر "معلومات إضافية"
        markup = telebot.types.InlineKeyboardMarkup()
        more_info_button = telebot.types.InlineKeyboardButton("📚 معلومات إضافية", url="https://www.autismspeaks.org/")
        markup.add(more_info_button)

        bot.send_message(message.chat.id, f"🔹 *إجابة:* {bot_response}", parse_mode="Markdown", reply_markup=markup)

    except Exception as e:
        error_message = f"❌ حدث خطأ: {e}"
        bot.send_message(message.chat.id, error_message)
        print(f"خطأ في الاتصال بـ OpenAI: {e}")

# تشغيل البوت بشكل مستمر في Thread منفصل
def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

# تشغيل تطبيق الويب للحفاظ على Replit نشطًا
app.run(host="0.0.0.0", port=8080)











  