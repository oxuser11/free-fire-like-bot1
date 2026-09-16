import os
import json
import time
import threading
import requests
import telebot
from telebot import types
from flask import Flask

# 1. 24/7 Server for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "NUMBER TO INFO BOT ACTIVE 24/7"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# 2. Configs & Bot Token
BOT_TOKEN = "8609353017:AAGN3B9DvcFBnUO809FyC3VfaslmeOyr_gI"
ADMIN_ID = 8671410379
ADMIN_USER = "OxRehann"

CH1_ID = "@OxRehanCyber"
CH1_LINK = "https://t.me/OxRehanCyber"
CH2_LINK = "https://t.me/+852hkOgj0UNlZGU9"

API_BASE = "https://api-hub-alpha.vercel.app/api/number-info"
API_KEY = "cybershr1k_b800c6028c1935c39a"

DB_FILE = "num_info_db.json"
user_states = {}

bot = telebot.TeleBot(BOT_TOKEN)

# 3. Database Management
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"users": {}}

def save_db(data):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass

db = load_db()

def get_user(uid, username="User"):
    s = str(uid)
    if s not in db["users"]:
        db["users"][s] = {
            "name": username,
            "credits": 10,
            "invites": 0,
            "verified": False,
            "referrer": None
        }
        save_db(db)
    return db["users"][s]

def check_channel_member(uid):
    try:
        st = bot.get_chat_member(CH1_ID, uid).status
        return st in ['member', 'administrator', 'creator']
    except:
        return True

# 4. Keyboards & Markup
def verify_markup():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("📢 Join Official Channel", url=CH1_LINK),
        types.InlineKeyboardButton("📢 Join Backup Channel", url=CH2_LINK),
        types.InlineKeyboardButton("⚡ 𝐕𝐄𝐑𝐈𝐅𝐘 & 𝐔𝐍𝐋𝐎𝐂𝐊 ⚡", callback_data="chk_verify")
    )
    return kb

BTN_NUM_INFO = "🔍 𝐍𝐮𝐦𝐛𝐞𝐫 𝐓𝐨 𝐈𝐧𝐟𝐨"
BTN_BALANCE  = "💳 𝐁𝐚𝐥𝐚𝐧𝐜𝐞"
BTN_REFER    = "🎁 𝐑𝐞𝐟𝐞𝐫"
BTN_BUY      = "💎 𝐁𝐮𝐲 𝐂𝐫𝐞𝐝𝐢𝐭𝐬"
BTN_CHANNEL  = "📢 𝐂𝐡𝐚𝐧𝐧𝐞𝐥"

def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(types.KeyboardButton(BTN_NUM_INFO))
    kb.add(types.KeyboardButton(BTN_BALANCE), types.KeyboardButton(BTN_REFER))
    kb.add(types.KeyboardButton(BTN_BUY), types.KeyboardButton(BTN_CHANNEL))
    return kb

# 5. Handlers
@bot.message_handler(commands=['start'])
def start_handler(m):
    uid = m.from_user.id
    s = str(uid)
    text = m.text.split()
    user_name = m.from_user.first_name or "REHANNN"

    if s not in db["users"]:
        ref_id = text[1] if len(text) > 1 and text[1].isdigit() and text[1] != s else None
        db["users"][s] = {
            "name": user_name,
            "credits": 5,
            "invites": 0,
            "verified": False,
            "referrer": ref_id
        }
        save_db(db)

    u = db["users"][s]

    if not u.get("verified", False):
        rm = types.ReplyKeyboardRemove()
        bot.send_message(m.chat.id, "🔒 *Verification Required!*", reply_markup=rm)
        verify_text = (
            f"👋 *Hey, {user_name}!*\\n\\n"
            "⚠️ Bot ke features use karne ke liye pehle hamare official channels join karein.\\n\\n"
            "Join karne ke baad niche **⚡ 𝐕𝐄𝐑𝐈𝐅𝐘 & 𝐔𝐍𝐋𝐎𝐂𝐊 ⚡** dabayein!"
        )
        bot.send_message(m.chat.id, verify_text, parse_mode='Markdown', reply_markup=verify_markup())
        return

    welcome_text = (
        f"👑 **WELCOME {user_name.upper()}**\\n\\n"
        f"🆔 **Account:** `{uid}`\\n"
        f"💳 **Balance:** `{u['credits']} Credits`\\n"
        f"👥 **Invites:** `{u['invites']}`\\n\\n"
        "Neeche diye gaye buttons se use karein 👇"
    )
    bot.send_message(m.chat.id, welcome_text, parse_mode='Markdown', reply_markup=main_keyboard())

@bot.callback_query_handler(func=lambda c: c.data == "chk_verify")
def callback_verification(c):
    uid = c.from_user.id
    u = get_user(uid, c.from_user.first_name)

    if check_channel_member(uid):
        u["verified"] = True
        u["credits"] += 5

        ref_id = u.get("referrer")
        if ref_id and ref_id in db["users"]:
            db["users"][ref_id]["credits"] += 3
            db["users"][ref_id]["invites"] += 1
            u["referrer"] = None
            try:
                bot.send_message(
                    int(ref_id),
                    f"🎁 *New Referral Joined!*\\n\\n👤 User: `{c.from_user.first_name}`\\n💎 *+3 Credits* added to your wallet!",
                    parse_mode='Markdown'
                )
            except:
                pass

        save_db(db)
        try:
            bot.delete_message(c.message.chat.id, c.message.message_id)
        except:
            pass

        bot.answer_callback_query(c.id, "✅ Verified successfully!")
        bot.send_message(
            c.message.chat.id,
            "🎉 **Verification Successful!**\\n\\nBot unlock ho gaya hai aur aapko bonus credits mil chuke hain.",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )
    else:
        bot.answer_callback_query(c.id, "❌ Aapne abhi tak channel join nahi kiya!", show_alert=True)

# 6. Button Operations
@bot.message_handler(func=lambda m: "NUMBER TO INFO" in m.text.upper())
def num_info_btn(m):
    u = get_user(m.from_user.id)
    if not u.get("verified", False):
        bot.send_message(m.chat.id, "🔒 Kripya pehle /start karke verify karein!", reply_markup=verify_markup())
        return

    if u["credits"] < 1:
        bot.send_message(
            m.chat.id,
            "⚠️ **Insufficient Credits!**\\n\\nNumber info nikalne ke liye minimum **1 Credit** chahiye.\\nFriends ko refer karke credits collect karein.",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )
        return

    user_states[m.from_user.id] = "await_num"
    bot.send_message(
        m.chat.id,
        "📱 **Enter 10-Digit Mobile Number:**\\n\\nJis number ki details nikalni hain wo yahan enter karein.\\n_(Cost: 1 Credit | Cancel: /cancel)_",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda m: "BALANCE" in m.text.upper())
def balance_btn(m):
    user_states.pop(m.from_user.id, None)
    u = get_user(m.from_user.id, m.from_user.first_name)
    bal_text = (
        f"┌─── ❖ **ACCOUNT DETAILS** ❖ ───\\n"
        f"│ 👤 **User:** `{u['name']}`\\n"
        f"│ 🆔 **Account:** `{m.from_user.id}`\\n"
        f"│ 💳 **Balance:** `{u['credits']} Credits`\\n"
        f"│ 👥 **Invites:** `{u['invites']}`\\n"
        f"└─── ❖ ─────────────── ❖ ───"
    )
    bot.send_message(m.chat.id, bal_text, parse_mode='Markdown', reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: "REFER" in m.text.upper())
def refer_btn(m):
    user_states.pop(m.from_user.id, None)
    uid = m.from_user.id
    bot_user = bot.get_me().username
    ref_text = (
        f"🎁 **Referral Link (+3 Credits):**\\n"
        f"`https://t.me/{bot_user}?start={uid}`\\n\\n"
        "Har valid friend ke verification par aapko **3 Credits** milenge!"
    )
    bot.send_message(m.chat.id, ref_text, parse_mode='Markdown', reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: "BUY CREDITS" in m.text.upper())
def buy_btn(m):
    user_states.pop(m.from_user.id, None)
    buy_text = (
        "💎 **BUY EXTRA CREDITS** 💎\\n\\n"
        "Credits recharge karne ke liye admin se direct contact karein:\\n"
        f"👉 @{ADMIN_USER}"
    )
    bot.send_message(m.chat.id, buy_text, parse_mode='Markdown', reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: "CHANNEL" in m.text.upper())
def channel_btn(m):
    user_states.pop(m.from_user.id, None)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📢 Join Channel", url=CH1_LINK))
    bot.send_message(m.chat.id, "Official channel join karein naye updates ke liye:", reply_markup=kb)

@bot.message_handler(commands=['cancel'])
def cancel_cmd(m):
    user_states.pop(m.from_user.id, None)
    bot.send_message(m.chat.id, "❌ Action canceled.", reply_markup=main_keyboard())

# 7. Number Processing & API Call
@bot.message_handler(func=lambda m: m.from_user.id in user_states)
def process_states(m):
    uid = m.from_user.id
    st = user_states.pop(uid, None)
    u = get_user(uid, m.from_user.first_name)

    if st == "await_num":
        mobile = m.text.strip().replace(" ", "").replace("+91", "")
        if not mobile.isdigit() or len(mobile) != 10:
            bot.reply_to(m, "❌ **Invalid Mobile Number!** Kripya sahi 10-digit number enter karein.", reply_markup=main_keyboard())
            return

        wait_msg = bot.send_message(m.chat.id, "🔍 **Fetching Details from Database...**", parse_mode='Markdown')

        try:
            url = f"{API_BASE}?key={API_KEY}&mobile={mobile}"
            resp = requests.get(url, timeout=20)
            res = resp.json()

            # Check validity of returned data
            if not res or res.get("status") is False or res.get("success") is False:
                bot.edit_message_text("❌ Is number ka data server par nahi mila ya number galat hai.", chat_id=m.chat.id, message_id=wait_msg.message_id)
                return

            # Deduct Credit on Success
            u["credits"] -= 1
            save_db(db)

            # Format Response
            data = res.get("data", res)
            out_lines = [
                "╔══════════════════════════╗",
                "   🔍 **NUMBER INFORMATION**   ",
                "╚══════════════════════════╝\\n",
                f"📱 **Mobile:** `{mobile}`"
            ]

            if isinstance(data, dict):
                for k, v in data.items():
                    if k.lower() not in ["status", "success", "key", "code"] and v:
                        out_lines.append(f"🔹 **{k.replace('_', ' ').title()}:** `{v}`")
            elif isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                if isinstance(first_item, dict):
                    for k, v in first_item.items():
                        if v:
                            out_lines.append(f"🔹 **{k.replace('_', ' ').title()}:** `{v}`")
            else:
                out_lines.append(f"🔹 **Result:** `{str(data)}`")

            out_lines.append(f"\\n💳 **Remaining Credits:** `{u['credits']}`")
            final_text = "\\n".join(out_lines)

            bot.delete_message(m.chat.id, wait_msg.message_id)
            bot.send_message(m.chat.id, final_text, parse_mode='Markdown', reply_markup=main_keyboard())

        except Exception as e:
            bot.edit_message_text("❌ API Server offline ya busy hai. Thodi der baad dubara prayas karein.", chat_id=m.chat.id, message_id=wait_msg.message_id)

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    bot.infinity_polling()
        
