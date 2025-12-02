import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random, sqlite3

TOKEN = "8450153849:AAGeY8SanH-cLtigaZStKU29TyJnD0ioK7U"

conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS u (id INTEGER PRIMARY KEY, bal INTEGER DEFAULT 5000, w INTEGER DEFAULT 0, l INTEGER DEFAULT 0)''')
conn.commit()

def g(u): r=c.execute("SELECT * FROM u WHERE id=?",(u,)).fetchone();return list(r)if r else(c.execute("INSERT INTO u(id,bal)VALUES(?,5000)",(u,));conn.commit();[u,5000,0,0])
def s(u,b=None,w=0,l=0):d=g(u);d[1]=b or d[1];d[2]+=w;d[3]+=l;c.execute("UPDATE u SET bal=?,w=?,l=? WHERE id=?",(d[1],d[2],d[3],u));conn.commit()

kb = ReplyKeyboardMarkup([["عقار","باط"],["مضاعفة","رصيدي"],["إحصائيات","مكافأة"]],resize_keyboard=True)

async def start(u,c):await u.message.reply_text("🎰 كازينو الجوكر مفتوح!\nرصيدك 5000\nاكتب رقم الرهان وبعدها اضغط عقار أو باط",reply_markup=kb)

async def m(u,c):
    id = u.effective_user.id;t=u.message.text;d=g(id)
    if t=="مكافأة"and c.user_data.get("d")!=u.message.date.day:s(id,d[1]+1000);c.user_data["d"]=u.message.date.day;await u.message.reply_text("مكافأة +1000")
    if t=="رصيدي":await u.message.reply_text(f"رصيدك: {d[1]:,}");return
    if t.isdigit():b=int(t);c.user_data["b"]=b;await u.message.reply_text(f"رهانك {b} ✅ اختار")
    if t in["عقار","باط"]and"b"in c.user_data:
        win=random.choice([1,0])
        if win:s(id,d[1]+c.user_data["b"],1,0);await u.message.reply_text(f"ربحت +{c.user_data['b']} 💰")
        else:s(id,d[1]-c.user_data["b"],0,1);await u.message.reply_text(f"خسرت {c.user_data['b']} 😭")
        c.user_data.pop("b",None)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,m))
print("شغال دلوقتي")
app.run_polling()
