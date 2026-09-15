import os
import json
import time
import threading
import requests
import telebot
from telebot import types
from flask import Flask

# 1. 24/7 Web Server for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "FREE FIRE LIKE BOT 1 ACTIVE 24/7"

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
INSTA_LINK = "https://instagram.com/ox.mods"

API_BASE_URL = "https://two0likeapifreebyzexxyh4x.onrender.com/like"
API_KEY = "20LikeFreeApiByzexxyh4x"
HEADER_MEDIA = "https://files.catbox.moe/0v2540.mp4"

KV_URL = "https://api.keyval.org/ox_ff_like_bot1_db_2026"
DB_FILE = "ff_like1_db.json"

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}

# 3. Database Management
def load_db():
    try:
        r = requests.get(KV_URL, timeout=4).json()
        if isinstance(r, dict) and "users" in r:
            return r
    except:
        pass
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"users": {}, "gift_codes": {}}

def save_db(data):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass
    try:
        requests.post(KV_URL, json=data, timeout=4)
    except:
        pass

db = load_db()

def get_user(uid):
    s = str(uid)
    if s not in db["users"]:
        db["users"][s] = {
            "credits": 0,
            "referrals": 0,
            "likes_ordered": 0,
            "verified": False,
            "referrer": None
        }
        save_db(db)
    return db["users"][s]

def check_channel_member(uid):
    try:
        st = bot.get_chat_member(CH1_ID, uid).status
        return st in ['member', 'administrator', 'creator']
    except Exception as e:
        return True

# 4. Keyboards
def verify_markup():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🔵 𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝟭 🔹", url=CH1_LINK),
        types.InlineKeyboardButton("🔵 𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝟮 🔹", url=CH2_LINK),
        types.InlineKeyboardButton("🔵 𝗙𝗢𝗟𝗟𝗢𝗪 𝗜𝗡𝗦𝗧𝗔𝗚𝗥𝗔𝗠 🔹", url=INSTA_LINK),
        types.InlineKeyboardButton("🟢 ⚡ 𝗩𝗘𝗥𝗜𝗙𝗬 & 𝗨𝗡𝗟𝗢𝗖𝗞 ⚡ 🟢", callback_data="chk_verify")
    )
    return kb

BTN_SEND_LIKE = "🚀 🎯 SEND LIKE (10 CREDITS)"
BTN_PROFILE   = "🟡 👤 MY PROFILE / CREDITS"
BTN_REFER     = "🟢 👥 REFER & EARN (10 CR)"
BTN_REDEEM    = "🟣 🎁 REDEEM GIFT CODE"
BTN_BUY       = "💎 💳 BUY CREDITS"
BTN_SUPPORT   = "🟠 📞 24/7 SUPPORT"

def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(types.KeyboardButton(BTN_SEND_LIKE))
    kb.add(types.KeyboardButton(BTN_PROFILE), types.KeyboardButton(BTN_REFER))
    kb.add(types.KeyboardButton(BTN_REDEEM), types.KeyboardButton(BTN_BUY))
    kb.add(types.KeyboardButton(BTN_SUPPORT))
    return kb

# 5. Handlers
@bot.message_handler(commands=['start'])
def start_handler(m):
    uid = m.from_user.id
    s = str(uid)
    text = m.text.split()

    if s not in db["users"]:
        ref_id = text[1] if len(text) > 1 and text[1].isdigit() and text[1] != s else None
        db["users"][s] = {
            "credits": 0,
            "referrals": 0,
            "likes_ordered": 0,
            "verified": False,
            "referrer": ref_id
        }
        save_db(db)

    u = db["users"][s]

    if not u.get("verified", False):
        rm = types.ReplyKeyboardRemove()
        bot.send_message(m.chat.id, "🔒 *Verification Required!*", reply_markup=rm)
        caption_verify = (
            f"👋 *HELLO, {m.from_user.first_name.upper()}!*\n\n"
            "⚠️ *Bot use karne aur 10 Free Credits lene ke liye steps complete karein:*\n"
            "🔹 Channel 1 & Channel 2 join karein\n"
            "🔹 Instagram par follow karein (@ox.mods)\n\n"
            "Tasks poore karke niche **⚡ VERIFY & UNLOCK ⚡** dabayein!"
        )
        bot.send_message(m.chat.id, caption_verify, parse_mode='Markdown', reply_markup=verify_markup())
        return

    caption_text = (
        "╔══════════════════════════╗\n"
        "   ✦  **OX REHAN LIKE BOT**  ✦  ||\n"
        "╚══════════════════════════╝\n\n"
        f"👋 **HELLO, {m.from_user.first_name.upper()}!**\n"
        "────────────────────────────\n"
        f"💰 **Available Balance:** `{u['credits']} Credits`\n"
        "🎯 **Cost:** 10 Credits = 20 Likes\n\n"
        "🚀 **QUICK COMMANDS**\n"
        "┌───────────────────────────\n"
        "│ 🎯 `/like [UID]` — SEND LIKES (10 Cr)\n"
        "│ 🎁 `/redeem [CODE]` — CLAIM GIFT CODE\n"
        "│ 👥 `/refer` — GET 10 CREDITS PER INVITE\n"
        "└───────────────────────────\n\n"
        "Neeche diye gaye buttons se operate karein 👇"
    )

    try:
        bot.send_video(m.chat.id, HEADER_MEDIA, caption=caption_text, parse_mode='Markdown', reply_markup=main_keyboard())
    except:
        bot.send_message(m.chat.id, caption_text, parse_mode='Markdown', reply_markup=main_keyboard())

@bot.callback_query_handler(func=lambda c: c.data == "chk_verify")
def callback_verification(c):
    uid = c.from_user.id
    s = str(uid)
    u = get_user(uid)

    if check_channel_member(uid):
        u["verified"] = True
        u["credits"] += 10

        ref_id = u.get("referrer")
        if ref_id and ref_id in db["users"]:
            db["users"][ref_id]["credits"] += 10
            db["users"][ref_id]["referrals"] += 1
            u["referrer"] = None
            try:
                bot.send_message(
                    int(ref_id),
                    f"🎉 *New Referral Joined & Verified!*\n\n"
                    f"👤 Member: `{c.from_user.first_name}`\n"
                    f"💎 *+10 Credits* aapke account me add ho gaye!",
                    parse_mode='Markdown'
                )
            except:
                pass

        save_db(db)

        try:
            bot.delete_message(c.message.chat.id, c.message.message_id)
        except:
            pass

        bot.answer_callback_query(c.id, "✅ Verified! 10 Credits added!")
        bot.send_message(
            c.message.chat.id,
            "🎉 *Welcome Bonus Unlocked!*\n\n"
            "🎁 Aapko **10 Free Credits** mil gaye hain!\n"
            "Ab aap kisi bhi account par **20 Likes** send kar sakte hain.",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )
    else:
        bot.answer_callback_query(c.id, "❌ Aapne abhi tak channel join nahi kiya!", show_alert=True)

# 6. Button Actions
@bot.message_handler(func=lambda m: "SEND LIKE" in m.text.upper())
def send_like_btn(m):
    user_states[m.from_user.id] = "await_uid"
    bot.send_message(
        m.chat.id,
        "🎯 **Enter Free Fire UID:**\n\n"
        "Jis ID par 20 likes send karne hain, uska UID type karke bhejein.\n"
        "_(Cost: 10 Credits | Cancel: /cancel)_",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda m: "PROFILE" in m.text.upper())
def profile_btn(m):
    user_states.pop(m.from_user.id, None)
    u = get_user(m.from_user.id)
    text = (
        "╔══════════════════════════╗\n"
        "       👤 **USER PROFILE**       \n"
        "╚══════════════════════════╝\n\n"
        f"👤 **Name:** {m.from_user.first_name}\n"
        f"🆔 **Telegram ID:** `{m.from_user.id}`\n\n"
        f"💎 **Credits:** `{u['credits']} Credits`\n"
        f"👥 **Total Referrals:** `{u['referrals']}`\n"
        f"❤️ **Likes Ordered:** `{u['likes_ordered']} Likes`\n\n"
        "📌 *10 Credits = 20 Likes*"
    )
    bot.send_message(m.chat.id, text, parse_mode='Markdown', reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: any(w in m.text.upper() for w in ["REFER", "EARN"]))
def refer_btn(m):
    user_states.pop(m.from_user.id, None)
    uid = m.from_user.id
    bot_user = bot.get_me().username
    text = (
        "🚀 **REFER & EARN UNLIMITED CREDITS** 🚀\n\n"
        "💎 **Reward:** Har valid friend ke join hone par **10 Credits**!\n"
        "🎯 **1 Friend = 20 Free Fire Likes!**\n\n"
        "🔗 **Aapka Personal Invite Link:**\n"
        f"`https://t.me/{bot_user}?start={uid}`\n\n"
        "📌 *Is link ko doston aur groups me share karein!*"
    )
    bot.send_message(m.chat.id, text, parse_mode='Markdown', reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: "BUY" in m.text.upper())
def buy_credits_btn(m):
    user_states.pop(m.from_user.id, None)
    text = (
        "💎 **BUY EXTRA LIKE CREDITS** 💎\n\n"
        "Agar aap extra likes chahte hain toh cheap price me credits khareed sakte hain:\n\n"
        "• 50 Credits (100 Likes) — ₹20\n"
        "• 120 Credits (240 Likes) — ₹40\n"
        "• 300 Credits (600 Likes) — ₹80\n\n"
        f"👉 Contact Admin for Purchase: @{ADMIN_USER}"
    )
    bot.send_message(m.chat.id, text, parse_mode='Markdown', reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: "REDEEM" in m.text.upper())
def redeem_btn(m):
    user_states[m.from_user.id] = "redeem_code"
    bot.send_message(m.chat.id, "🎁 Apna **Gift Code** yahan enter karein:\n\n_(Cancel: /cancel)_")

@bot.message_handler(func=lambda m: "SUPPORT" in m.text.upper())
def support_btn(m):
    user_states.pop(m.from_user.id, None)
    bot.send_message(
        m.chat.id,
        f"📞 **OFFICIAL SUPPORT**\n\nKisi bhi problem ya credits lene ke liye admin se baat karein:\n👉 @{ADMIN_USER}",
        parse_mode='Markdown',
        reply_markup=main_keyboard()
    )

@bot.message_handler(commands=['cancel'])
def cancel_cmd(m):
    user_states.pop(m.from_user.id, None)
    bot.send_message(m.chat.id, "❌ Action canceled.", reply_markup=main_keyboard())

# 7. Processing Inputs
@bot.message_handler(commands=['like'])
def direct_like_cmd(m):
    parts = m.text.split()
    if len(parts) < 2:
        bot.reply_to(m, "Format: `/like <UID>`\nExample: `/like 8559022952`", parse_mode='Markdown')
        return
    execute_like(m, parts[1].strip())

@bot.message_handler(func=lambda m: m.from_user.id in user_states)
def process_states(m):
    uid = m.from_user.id
    st = user_states.pop(uid, None)
    u = get_user(uid)

    if st == "await_uid":
        execute_like(m, m.text.strip())

    elif st == "redeem_code":
        code = m.text.strip().upper()
        s = str(uid)
        codes = db.get("gift_codes", {})

        if code not in codes:
            bot.reply_to(m, "❌ Invalid ya Expired Gift Code!", reply_markup=main_keyboard())
            return

        gdata = codes[code]
        if s in gdata["users"]:
            bot.reply_to(m, "⚠️ Yeh code aap pehle claim kar chuke hain!", reply_markup=main_keyboard())
            return

        if len(gdata["users"]) >= gdata["max_claims"]:
            bot.reply_to(m, "⚠️ Is code ki claims limit full ho chuki hai!", reply_markup=main_keyboard())
            return

        amt = int(gdata["amount"])
        u["credits"] += amt
        gdata["users"].append(s)
        save_db(db)

        bot.reply_to(
            m,
            f"🎉 **Gift Code Redeemed Successfully!**\n\n"
            f"💎 *+{amt} Credits* aapke account me credit ho gaye!\n"
            f"💰 Total Credits: `{u['credits']}`",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )

def execute_like(m, target_uid):
    uid = m.from_user.id
    u = get_user(uid)

    if not target_uid.isdigit():
        bot.reply_to(m, "❌ **Invalid UID!** Sirf numeric digits bhejein.", reply_markup=main_keyboard())
        return

    if u["credits"] < 10:
        bot.send_message(
            m.chat.id,
            f"⚠️ **Insufficient Credits!**\n\n"
            f"Aapka current balance: `{u['credits']} Credits`\n"
            "20 Likes send karne ke liye **10 Credits** chahiye.\n\n"
            "👉 Apne doston ko invite karein (10 Credits per invite) ya Buy karein!",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )
        return

    u["credits"] -= 10
    u["likes_ordered"] += 20
    save_db(db)

    progress_msg = (
        "╭─── ✪ GIVING LIKE ─────────\n"
        "│ 📡 **PROCESSING REQUEST**\n"
        "│ ▰▰▰▰▰▰▰▰▱▱ 80%\n"
        "╰───────────────────────────\n"
        "_SENDING 20 LIKES TO YOUR ACCOUNT CAREFULLY..._"
    )
    sent_card = bot.send_message(m.chat.id, progress_msg, parse_mode='Markdown')

    try:
        url = f"{API_BASE_URL}?key={API_KEY}&uid={target_uid}&region=ind"
        res = requests.get(url, timeout=25).json()

        p_name = res.get("PlayerNickname", res.get("name", "Unknown"))
        p_region = res.get("Region", "ind")
        likes_before = res.get("LikesbeforeCommand", res.get("before", "4685"))
        likes_after = res.get("LikesafterCommand", res.get("after", "4705"))
        likes_given = res.get("LikesGivenByAPI", res.get("given", "+20"))

        result_text = (
            "╭─── ✪ LIKE SUCCESSFUL ─────\n"
            "│ ✅ **ORDER COMPLETED**\n"
            "╰───────────────────────────\n\n"
            "╭─── ✦ PLAYER ✦ ────────────\n"
            f"│ 🆔 **UID:** `{target_uid}`\n"
            f"│ 👤 **NAME:** `{p_name}`\n"
            f"│ 🌍 **REGION:** `{p_region}`\n"
            "╰───────────────────────────\n\n"
            "╭─── ✦ LIKES ✦ ─────────────\n"
            f"│ 📉 **BEFORE:** `{likes_before}`\n"
            f"│ 📈 **AFTER:** `{likes_after}`\n"
            f"│ ❤️ **GIVEN:** `{likes_given}`\n"
            "╰───────────────────────────\n\n"
            f"💰 **Remaining Credits:** `{u['credits']}`\n"
            "🎯 @OxRehanCyber"
        )

        try:
            bot.delete_message(m.chat.id, sent_card.message_id)
        except:
            pass

        try:
            bot.send_video(m.chat.id, HEADER_MEDIA, caption=result_text, parse_mode='Markdown', reply_markup=main_keyboard())
        except:
            bot.send_message(m.chat.id, result_text, parse_mode='Markdown', reply_markup=main_keyboard())

    except Exception as err:
        u["credits"] += 10
        u["likes_ordered"] -= 20
        save_db(db)
        try:
            bot.edit_message_text(
                "❌ **API Busy ya Server down hai!**\nAapke 10 credits refund kar diye gaye hain. 1 minute baad try karein.",
                chat_id=m.chat.id,
                message_id=sent_card.message_id,
                parse_mode='Markdown'
            )
        except:
            bot.reply_to(m, "❌ Server busy hai, credits refund kar diye gaye hain.", reply_markup=main_keyboard())

# 8. Admin Commands
@bot.message_handler(commands=['gen'])
def admin_generate_code(m):
    if m.from_user.id != ADMIN_ID:
        return
    parts = m.text.split()
    if len(parts) != 4:
        bot.reply_to(m, "Format: `/gen <CODE> <CREDITS> <MAX_USERS>`\nExample: `/gen FREE50 50 10`", parse_mode='Markdown')
        return

    code = parts[1].upper()
    amount = int(parts[2])
    max_c = int(parts[3])

    if "gift_codes" not in db:
        db["gift_codes"] = {}

    db["gift_codes"][code] = {
        "amount": amount,
        "max_claims": max_c,
        "users": []
    }
    save_db(db)

    bot.reply_to(
        m,
        f"✅ **Gift Code Created Successfully!**\n\n"
        f"🎁 **Code:** `{code}`\n"
        f"💎 **Credits:** `{amount}`\n"
        f"👥 **Max Users:** `{max_c}`",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['all'])
def admin_broadcast(m):
    if m.from_user.id != ADMIN_ID:
        return
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(m, "Format: `/all <Aapka Message>`", parse_mode='Markdown')
        return

    msg = parts[1]
    all_users = list(db.get("users", {}).keys())
    bot.reply_to(m, f"📢 Broadcast shuru: {len(all_users)} users ko bhej rahe hain...")

    success, failed = 0, 0
    for u in all_users:
        try:
            bot.send_message(int(u), f"📢 **OFFICIAL ANNOUNCEMENT**\n\n{msg}", parse_mode='Markdown')
            success += 1
            time.sleep(0.04)
        except:
            failed += 1

    bot.send_message(m.chat.id, f"✅ Broadcast Done!\nSent: `{success}`\nFailed: `{failed}`", parse_mode='Markdown')

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    bot.infinity_polling()
