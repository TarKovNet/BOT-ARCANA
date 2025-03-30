import logging
try:
    import openai
except ImportError:
    openai = None
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ChatMemberHandler, CallbackContext
from database import add_user

# ========== 1. НАЛАШТУВАННЯ ЛОГГІНГУ ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    add_user(user.id, user.first_name, user.last_name, user.username)
    
    await update.message.reply_text(WELCOME_TEXT)
    return await show_main_menu(update, context)

async def new_user(update: Update, context: CallbackContext) -> None:
    """Обробник для нових користувачів"""
    for member in update.chat_member.new_chat_members:
        welcome_text = (
            f"👋 Вітаю, {member.first_name}!\n\n"
            "Я допоможу тобі у світі езотерики. Натисни /start, щоб розпочати!"
        )
        await update.message.reply_text(welcome_text)

# ========== 2. ТОКЕНИ ==========
# Завантажуємо змінні з .env
load_dotenv()

# Зчитуємо токени
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GPT_TOKEN = os.getenv("GPT_TOKEN")
app = ApplicationBuilder().token(BOT_TOKEN).build()
openai.api_key = GPT_TOKEN  # 🔹 Встановлюємо API-ключ для OpenAI

# Перевіряємо, чи токен існує
if not BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN не знайдено. Додай його у файл .env!")

if not GPT_TOKEN:
    raise ValueError("❌ GPT_TOKEN не знайдено. Додай його у файл .env!")

# ========== 3. СТАНИ ДЛЯ CONVERSATIONHANDLER ==========


app.add_handler(ChatMemberHandler(new_user, ChatMemberHandler.CHAT_MEMBER))

(
    MAIN_MENU,
    NUMEROLOGY_MENU,
    ASTROLOGY_MENU,
    ESOTERICS_MENU,
    MAGIC_MENU,
    TOOLS_MENU,
    ENTER_DATA_STATE
) = range(7)

# ========== 4. ФУНКЦІЯ ДЛЯ НУМЕРОЛОГІЇ (КРЕАТИВНИЙ СТИЛЬ) ==========
async def handle_numerology_data(user_input: str) -> str:
    """
    Формує креативний нумерологічний аналіз (українською), 
    з емодзі та позитивним настроєм, без технічних деталей.
    """
    system_message = (
        "Ти — креативний нумеролог, який пояснює суть дат народження чи імен "
        "у простій і надихаючій формі. Не згадуй технічних аспектів, "
        "не пиши складних обчислень, просто підсумовуй та надихай."
    )
    user_prompt = (
        f"Проаналізуй нумерологічні дані: {user_input}.\n"
        "Створи короткий, натхненний опис із емодзі та позитивними побажаннями."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Сталася помилка під час звернення до сервісу. Деталі: {e}"

# ========== 5. ІНШІ ФУНКЦІЇ "ЗАГЛУШКИ" (ЗА БАЖАННЯМ ОНОВЛЮЙТЕ ТАК САМО) ==========
# ========== 5. ФУНКЦІЇ ДЛЯ ОБРОБКИ ДАНИХ ==========
async def handle_astrology_data(user_input: str) -> str:
    """
    Креативний астрологічний аналіз на основі введених даних.
    """
    system_message = (
        "Ти — досвідчений астролог, який пояснює вплив зірок на людину "
        "у простій, натхненній формі. Уникай складних технічних термінів, "
        "подавай інформацію так, щоб вона була цікавою для будь-кого."
    )
    user_prompt = f"Проаналізуй астрологічні дані: {user_input}.\nСтвори натхненний опис із емодзі."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Сталася помилка під час звернення до сервісу. Деталі: {e}"


async def handle_esoterics_data(user_input: str) -> str:
    """
    Генерує езотеричний аналіз на основі введених даних.
    """
    system_message = (
        "Ти — езотеричний гід, який пояснює містичні аспекти життя "
        "у доступній та надихаючій формі. Уникай складної термінології, "
        "подавай інформацію яскраво та з позитивним настроєм."
    )
    user_prompt = f"Проаналізуй езотеричні дані: {user_input}.\nСтвори натхненний опис із емодзі."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Сталася помилка під час звернення до сервісу. Деталі: {e}"


async def handle_magic_data(user_input: str) -> str:
    """
    Генерує містичний опис магічних практик.
    """
    system_message = (
        "Ти — експерт у магії, який просто і захопливо розповідає про ритуали, "
        "енергії та талісмани. Створи магічний опис, що надихне читача."
    )
    user_prompt = f"Опиши магічні практики, пов'язані з: {user_input}.\nДодай трохи таємничості й емодзі."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Сталася помилка під час звернення до сервісу. Деталі: {e}"


async def handle_tools_data(user_input: str) -> str:
    """
    Генерує пояснення для додаткових езотеричних інструментів.
    """
    system_message = (
        "Ти — досвідчений майстер езотеричних інструментів, "
        "який доступно пояснює їх значення і використання."
    )
    user_prompt = f"Опиши езотеричний інструмент: {user_input}.\nСтвори короткий, цікавий опис із емодзі."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Сталася помилка під час звернення до сервісу. Деталі: {e}"


# ========== 6. ПРИВІТАЛЬНИЙ ТЕКСТ І МЕНЮ ==========

WELCOME_TEXT = (
    "Вітаю у містичному просторі! ✨\n\n"
    "Тут ви можете досліджувати числа, зірки, езотерику та різні інструменти, "
    "щоб відкрити нові грані свого життя.\n\n"
    "Просто надішліть будь-яке повідомлення або оберіть пункт меню нижче, "
    "щоб розпочати!"
)

async def show_main_menu(update_or_context, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Показує головне меню з п'ятьма розділами.
    """
    keyboard = [
        [InlineKeyboardButton("1. Нумерологія 🔢", callback_data="menu_numerology")],
        [InlineKeyboardButton("2. Астрологія 🌌", callback_data="menu_astrology")],
        [InlineKeyboardButton("3. Езотерика 🔮", callback_data="menu_esoterics")],
        [InlineKeyboardButton("4. Магія 🪄", callback_data="menu_magic")],
        [InlineKeyboardButton("5. Інструменти 🛠", callback_data="menu_tools")],
        [InlineKeyboardButton("Завершити /cancel", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text_main_menu = (
        "Оберіть розділ, що вас цікавить:\n\n"
        "1. 🔢 Нумерологія – Числа розкажуть про характер, сумісність і майбутнє. ✨ \n"
        "2. 🌌 Астрологія – Знаки Зодіаку, гороскопи та натальна карта. 🔭\n"
        "3. 🔮 Езотерика – Інтуїція, енергетика та таємні знаки долі. 🌀 \n"
        "4. 🪄 Магія – Ритуали, Таро, амулети та магічні практики. 🔥\n"
        "5. 🛠 Інструменти – Карма, час сили, виконання бажань. ⚖️\n"
        "Якщо захочете вийти, натисніть «Завершити /cancel»."
    )

    if isinstance(update_or_context, Update) and update_or_context.callback_query:
        query = update_or_context.callback_query
        await query.answer()
        await query.edit_message_text(text_main_menu, reply_markup=reply_markup)
    elif isinstance(update_or_context, Update) and update_or_context.message:
        await update_or_context.message.reply_text(text_main_menu, reply_markup=reply_markup)
    else:
        chat_id = update_or_context.effective_chat.id
        await context.bot.send_message(chat_id, text_main_menu, reply_markup=reply_markup)

    return MAIN_MENU

# ========== 7. ОБРОБНИК /START І ПОВЕДІНКА ПРИ ПЕРШОМУ ВІЗИТІ ==========

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Якщо користувач введе /start, покажемо привітання і меню.
    """
    await update.message.reply_text(WELCOME_TEXT)
    return await show_main_menu(update, context)

async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Якщо користувач щойно відкрив бот і пише будь-яке повідомлення (не команду).
    При першому повідомленні – показуємо WELCOME_TEXT,
    далі одразу відправляємо його в головне меню.
    """
    if not context.user_data.get("has_seen_welcome", False):
        context.user_data["has_seen_welcome"] = True
        await update.message.reply_text(WELCOME_TEXT)

    return await show_main_menu(update, context)

# ========== 8. ПІДМЕНЮ (КОРОТКО, В ТОМУ ЧИСЛІ ДЛЯ НУМЕРОЛОГІЇ) ==========

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обробляє натискання кнопок у головному меню."""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_numerology":
        return await show_numerology_menu(update, context)
    elif data == "menu_astrology":
        return await show_astrology_menu(update, context)
    elif data == "menu_esoterics":
        return await show_esoterics_menu(update, context)
    elif data == "menu_magic":
        return await show_magic_menu(update, context)
    elif data == "menu_tools":
        return await show_tools_menu(update, context)
    elif data == "cancel":
        return await cancel(update, context)

    return MAIN_MENU

# --- Підменю: Нумерологія ---
async def show_numerology_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.edit_message_text("🔢 Нумерологія: оберіть конкретний аспект:")
    keyboard = [
    [InlineKeyboardButton("📜 Аналіз особистості – Що кажуть числа про вас? 🔮", callback_data="num_personal")],
    [InlineKeyboardButton("🔢 Матриця Піфагора – Ваші унікальні числові характеристики. 🔢", callback_data="num_pythagoras")],
    [InlineKeyboardButton("📅 Прогноз року – Що чекати у цьому році? 🗓️", callback_data="num_forecast")],
    [InlineKeyboardButton("💞 Сумісність – Наскільки ви підходите один одному? ❤️", callback_data="num_compatibility")],
    [InlineKeyboardButton("🔙 «Назад»", callback_data="back_main_menu")]
]

    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
    return NUMEROLOGY_MENU

async def numerology_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "num_personal":
        await query.edit_message_text("Введіть дату народження або ім’я (наприклад, 15.07.1995 або Олександр):")
        context.user_data["numerology_mode"] = "personal"
        return ENTER_DATA_STATE

    elif data == "num_pythagoras":
        await query.edit_message_text("Введіть дату народження для розрахунку Матриці Піфагора:")
        context.user_data["numerology_mode"] = "pythagoras"
        return ENTER_DATA_STATE

    elif data == "num_forecast":
        await query.edit_message_text("Вкажіть дату народження для особистого прогнозу:")
        context.user_data["numerology_mode"] = "forecast"
        return ENTER_DATA_STATE

    elif data == "num_compatibility":
        await query.edit_message_text("Введіть дві дати через кому (01.01.2000, 02.02.2002):")
        context.user_data["numerology_mode"] = "compatibility"
        return ENTER_DATA_STATE

    elif data == "back_main_menu":
        return await show_main_menu(update, context)

    return NUMEROLOGY_MENU

# --- Підменю: Астрологія ---
async def show_astrology_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.edit_message_text("🔮 Астрологія: оберіть конкретний аспект:")
    keyboard = [
        [InlineKeyboardButton("🌟 Натальна карта – Вплив планет на ваше життя. 🔭", callback_data="astro_natal")],
        [InlineKeyboardButton("📆 Гороскоп на день – Що підготували зорі сьогодні? ✨", callback_data="astro_daily")],
        [InlineKeyboardButton("♌ Знаки Зодіаку – Дізнайтеся більше про свій знак. ♈", callback_data="astro_zodiac")],
        [InlineKeyboardButton("💞 Сумісність – Чи ви ідеальна пара за зірками? 💫", callback_data="astro_compatibility")],
        [InlineKeyboardButton("🔙 «Назад»", callback_data="back_main_menu")]
    ]

    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
    return ASTROLOGY_MENU

async def astrology_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "astro_natal":
        await query.edit_message_text("Введіть дату, час і місце народження для аналізу натальної карти (15.07.1995, 14:30, Київ):")
        context.user_data["astrology_mode"] = "natal"
        return ENTER_DATA_STATE

    elif data == "astro_daily":
        await query.edit_message_text("Введіть ваш знак Зодіаку для щоденного гороскопу (Овен, Рак і т. д.):")
        context.user_data["astrology_mode"] = "daily"
        return ENTER_DATA_STATE

    elif data == "astro_zodiac":
        await query.edit_message_text("Введіть вашу дату народження, щоб дізнатися характеристику знаку:")
        context.user_data["astrology_mode"] = "zodiac"
        return ENTER_DATA_STATE

    elif data == "astro_compatibility":
        await query.edit_message_text("Введіть два знаки (Овен, Рак) для аналізу сумісності:")
        context.user_data["astrology_mode"] = "compatibility"
        return ENTER_DATA_STATE

    elif data == "back_main_menu":
        return await show_main_menu(update, context)

    return ASTROLOGY_MENU


# --- Підменю: Езотерика ---
async def show_esoterics_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.edit_message_text("🔑 Езотерика: оберіть напрямок:")
    keyboard = [
        [InlineKeyboardButton("🌀 Енергетика людини – Гармонія та внутрішня сила. ⚡", callback_data="eso_energy")],
        [InlineKeyboardButton("👁️ Третє око – Розвиток інтуїції та передбачень. 🔮", callback_data="eso_thirdeye")],
        [InlineKeyboardButton("🔮 Пророцтва та знаки – Тлумачення снів і підказок долі. 🌙", callback_data="eso_prophecy")],
        [InlineKeyboardButton("🔙 «Назад»", callback_data="back_main_menu")]
    ]

    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
    return ESOTERICS_MENU

async def esoterics_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "eso_energy":
        await query.edit_message_text("Опишіть свій поточний стан (Відчуваю втому, Немає енергії):")
        context.user_data["esoterics_mode"] = "energy"
        return ENTER_DATA_STATE

    elif data == "eso_thirdeye":
        await query.edit_message_text(" Введіть свій досвід або питання (Чи можна відкрити третє око?):")
        context.user_data["esoterics_mode"] = "thirdeye"
        return ENTER_DATA_STATE

    elif data == "eso_prophecy":
        await query.edit_message_text("Опишіть знак або сон (Приснився чорний кіт, що це означає?):")
        context.user_data["esoterics_mode"] = "prophecy"
        return ENTER_DATA_STATE

    elif data == "back_main_menu":
        return await show_main_menu(update, context)

    return ESOTERICS_MENU


# --- Підменю: Магія ---
async def show_magic_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.edit_message_text("✨ Магія: оберіть категорію:")
    keyboard = [
        [InlineKeyboardButton("🕯️ Ритуали – Магічні обряди для різних ситуацій. 🔥", callback_data="magic_rituals")],
        [InlineKeyboardButton("🔮 Магічні предмети – Амулети, талісмани та їхні сили. 🏺", callback_data="magic_items")],
        [InlineKeyboardButton("🃏 Карти Таро – Отримайте відповідь на своє питання. 🎴", callback_data="magic_tarot")],
        [InlineKeyboardButton("🔙 «Назад»", callback_data="back_main_menu")]
    ]

    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
    return MAGIC_MENU

async def magic_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "magic_rituals":
        await query.edit_message_text("Введіть мету ритуалу (Залучення грошей, Захист від негативу):")
        context.user_data["magic_mode"] = "rituals"
        return ENTER_DATA_STATE

    elif data == "magic_items":
        await query.edit_message_text("Введіть назву магічного предмета (Амулет, Свічка, Талісман):")
        context.user_data["magic_mode"] = "items"
        return ENTER_DATA_STATE

    elif data == "magic_tarot":
        await query.edit_message_text("Введіть питання, на яке хочете отримати відповідь (Що мене чекає в коханні?):")
        context.user_data["magic_mode"] = "tarot"
        return ENTER_DATA_STATE

    elif data == "back_main_menu":
        return await show_main_menu(update, context)

    return MAGIC_MENU


# --- Підменю: Інструменти ---
async def show_tools_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.edit_message_text("🛠️ Інструменти: оберіть потрібний інструмент:")
    keyboard = [
        [InlineKeyboardButton("🕰️ Час сили – Найкращі моменти для дій. ⏳", callback_data="tools_power_time")],
        [InlineKeyboardButton("📜 Маніфестація бажань – Як втілити мрію у реальність? 💫", callback_data="tools_manifestation")],
        [InlineKeyboardButton("⚖️ Кармічний баланс – Аналіз карми та її покращення. 🌿", callback_data="tools_karma")],
        [InlineKeyboardButton("🔙 «Назад»", callback_data="back_main_menu")]
    ]

    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
    return TOOLS_MENU

async def tools_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "tools_power_time":
        await query.edit_message_text("Введіть дату народження для визначення вашого часу сили:")
        context.user_data["tools_mode"] = "power_time"
        return ENTER_DATA_STATE

    elif data == "tools_manifestation":
        await query.edit_message_text("Опишіть бажання (Хочу знайти кохання, Прагну фінансового успіху):")
        context.user_data["tools_mode"] = "manifestation"
        return ENTER_DATA_STATE

    elif data == "tools_karma":
        await query.edit_message_text("Опишіть ситуацію або проблему (Чому мені не щастить у стосунках?):")
        context.user_data["tools_mode"] = "karma"
        return ENTER_DATA_STATE

    elif data == "back_main_menu":
        return await show_main_menu(update, context)

    return TOOLS_MENU

# ========== 9. ОБРОБКА ВВЕДЕНИХ ДАНИХ (ENTER_DATA_STATE) ==========

async def handle_entered_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text.strip()

    # --- Нумерологія ---
    if "numerology_mode" in context.user_data:
        mode = context.user_data.pop("numerology_mode")
        result = await handle_numerology_data(user_input)
        # Відправляємо користувачу результат:
        await update.message.reply_text(result)
        return await show_main_menu(update, context)

    # --- Астрологія ---
    if "astrology_mode" in context.user_data:
        mode = context.user_data.pop("astrology_mode")
        result = await handle_astrology_data(user_input)
        await update.message.reply_text(result)
        return await show_main_menu(update, context)

    # --- Езотерика ---
    if "esoterics_mode" in context.user_data:
        mode = context.user_data.pop("esoterics_mode")
        result = await handle_esoterics_data(user_input)
        await update.message.reply_text(result)
        return await show_main_menu(update, context)

    # --- Магія ---
    if "magic_mode" in context.user_data:
        mode = context.user_data.pop("magic_mode")
        result = await handle_magic_data(user_input)
        await update.message.reply_text(result)
        return await show_main_menu(update, context)

    # --- Інструменти ---
    if "tools_mode" in context.user_data:
        mode = context.user_data.pop("tools_mode")
        result = await handle_tools_data(user_input)
        await update.message.reply_text(result)
        return await show_main_menu(update, context)

    # Якщо нічого не знайдено:
    await update.message.reply_text("Невідомий запит. Повертаю вас у головне меню.")
    return await show_main_menu(update, context)

# ========== 10. КОМАНДА /CANCEL ==========
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершити взаємодію з ботом."""
    if update.callback_query:
        await update.callback_query.edit_message_text("Дякуємо, що завітали! Нехай щастить 🌟")
    else:
        await update.message.reply_text("Дякуємо, що завітали! Нехай щастить 🌟")
    return ConversationHandler.END

# ========== 11. ГОЛОВНА ФУНКЦІЯ Запуску Бота ==========
def main() -> None:
    # Створюємо Application (аналог Updater у версіях 20+)
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[
            # Коли користувач надсилає будь-який текст (не команду) — handle_any_message
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message),
            # Якщо користувач вводить /start
            CommandHandler("start", start_command)
        ],
        states={

        MAIN_MENU: [
            CallbackQueryHandler(main_menu_callback),
        ],
        NUMEROLOGY_MENU: [
            CallbackQueryHandler(numerology_menu_callback),
        ],
        ASTROLOGY_MENU: [  
            CallbackQueryHandler(astrology_menu_callback),
        ],
        ESOTERICS_MENU: [  
            CallbackQueryHandler(esoterics_menu_callback),
        ],
        MAGIC_MENU: [ 
            CallbackQueryHandler(magic_menu_callback),
        ],
        TOOLS_MENU: [  
            CallbackQueryHandler(tools_menu_callback),
        ],
        ENTER_DATA_STATE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_entered_data),
        ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CallbackQueryHandler(cancel, pattern="^cancel$")
        ],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
