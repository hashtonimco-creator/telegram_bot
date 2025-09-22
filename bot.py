import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import database
import os

# --- CONFIGURATION ---
# !!! IMPORTANT: Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8283337457:AAEVcwVrbvUtwoZZh1fgvIYjXcDR4tyF_FI')

# !!! IMPORTANT: Replace 'YOUR_SUPER_ADMIN_USER_ID' with your own Telegram user ID
SUPER_ADMIN_ID = 579146791  # Replace with your Telegram User ID

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# --- WELCOME MESSAGE ---
WELCOME_MESSAGE = """\
👋 به بات هشتونیم خوش آمدید

برای استفاده بهتر، لطفاً این قوانین رو با دقت مطالعه کنید:

1️⃣ این بات فقط مخصوص ناشران فعال در شبکه‌های اجتماعی هست. ناشرانی که وب‌سایت یا رسانه‌ی محتوایی دارند، امکان استفاده از این بات را ندارند.

2️⃣ دسترسی به بات فقط با شماره موبایلی که در پنل ثبت کرده‌اید امکان‌پذیر است. (حتماً باید اکانت تلگرام شما هم با همین شماره فعال باشد.)

3️⃣ لینک‌های ارائه‌شده در این بات فقط برای استفاده در شبکه‌های اجتماعی طراحی شده‌اند و برای سایر بسترها کاربردی نخواهند داشت.
"""

# --- KEYBOARDS / MENUS ---
def create_main_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton('📱 اشتراک گذاری شماره تماس', request_contact=True)
    btn2 = KeyboardButton('🔑 ورود با کد دسترسی')
    markup.add(btn1, btn2)
    return markup

def create_publisher_panel():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton('🔗 دریافت لینک افیلیت')
    btn2 = KeyboardButton('🖼️ دریافت محتوای تبلیغاتی')
    btn3 = KeyboardButton('👤 پروفایل من')
    btn4 = KeyboardButton('📊 آمار عملکرد من')
    btn5 = KeyboardButton('✏️ تغییر یوزرنیم اینستاگرام')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

# Alias for backward compatibility
def create_publisher_menu():
    return create_publisher_panel()

def create_admin_panel():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton('👥 مدیریت ناشران')
    btn2 = KeyboardButton('🏪 مدیریت فروشگاه‌ها')
    btn3 = KeyboardButton('📦 مدیریت محصولات')
    btn4 = KeyboardButton('🖼️ مدیریت محتوا')
    btn5 = KeyboardButton('👨‍💼 مدیریت ادمین‌ها')
    btn6 = KeyboardButton('🏠 منوی اصلی')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

def create_admin_publishers_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton('👥 مشاهده لیست ناشران')
    btn2 = KeyboardButton('➕ افزودن ناشر جدید')
    btn3 = KeyboardButton('🔧 ویرایش ناشر')
    btn4 = KeyboardButton('🔙 برگشت به پنل ادمین')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def create_admin_stores_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton('🏪 مشاهده فروشگاه‌ها')
    btn2 = KeyboardButton('➕ افزودن فروشگاه')
    btn3 = KeyboardButton('🔙 برگشت به پنل ادمین')
    markup.add(btn1, btn2, btn3)
    return markup

def create_admin_products_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton('📦 مشاهده محصولات')
    btn2 = KeyboardButton('➕ افزودن محصول')
    btn3 = KeyboardButton('🔙 برگشت به پنل ادمین')
    markup.add(btn1, btn2, btn3)
    return markup

def create_admin_admins_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton('📜 لیست ادمین‌ها')
    btn2 = KeyboardButton('➕ افزودن ادمین')
    btn3 = KeyboardButton('➖ حذف ادمین')
    btn4 = KeyboardButton('🔙 برگشت به پنل ادمین')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# --- BOT HANDLERS ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id

    # Check if user is Super Admin
    if user_id == SUPER_ADMIN_ID:
        bot.send_message(user_id, '👑 سلام سوپر ادمین! به پنل مدیریت خوش آمدید.', reply_markup=create_admin_panel())
        return

    # Check if user is an Admin
    if database.is_admin(user_id):
        bot.send_message(user_id, '🛡️ سلام ادمین! به پنل مدیریت خوش آمدید.', reply_markup=create_admin_panel())
        return

    # Check if user is a registered Publisher
    publisher = database.get_publisher(user_id)
    if publisher:
        bot.send_message(user_id, f'سلام مجدد! به پنل ناشران هشتونیم خوش آمدید.', reply_markup=create_publisher_panel())
        return

    # New user: show welcome message and options
    bot.send_message(user_id, WELCOME_MESSAGE, reply_markup=create_main_menu())

# --- MAIN MENU HANDLERS ---
@bot.message_handler(func=lambda message: message.text == '🏠 منوی اصلی')
def back_to_main_menu(message):
    user_id = message.from_user.id
    
    # Check user type and redirect accordingly
    if user_id == SUPER_ADMIN_ID or database.is_admin(user_id):
        bot.send_message(user_id, '🏠 منوی اصلی ادمین', reply_markup=create_admin_panel())
    elif database.get_publisher(user_id):
        bot.send_message(user_id, '🏠 منوی اصلی ناشر', reply_markup=create_publisher_panel())
    else:
        bot.send_message(user_id, '🏠 منوی اصلی', reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == '🔑 ورود با کد دسترسی')
def request_access_code(message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id, '🔑 لطفاً کد دسترسی عددی خود را وارد کنید:', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_access_code)

def process_access_code(message):
    user_id = message.from_user.id
    access_code = message.text.strip()
    
    # Check if access code exists
    publisher_data = database.get_publisher_by_access_code(access_code)
    if not publisher_data:
        bot.send_message(user_id, '❌ کد دسترسی نامعتبر است. لطفاً مجدداً تلاش کنید.', reply_markup=create_main_menu())
        return
    
    # Check if already activated
    if publisher_data[1]:  # user_id field
        bot.send_message(user_id, '⚠️ این کد دسترسی قبلاً استفاده شده است.', reply_markup=create_main_menu())
        return
    
    # Request contact for activation
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = KeyboardButton('📱 تأیید شماره تماس', request_contact=True)
    markup.add(btn)
    
    # publisher_data structure: id, user_id, phone_number, telegram_username, page_username, publisher_code, access_code, is_active, registration_date, created_by_admin
    bot.send_message(user_id, f'✅ کد دسترسی معتبر است!\n\n📄 اطلاعات پیج شما:\n🔸 نام پیج: @{publisher_data[4]}\n🔸 کد ناشر: {publisher_data[5]}\n\nبرای فعال‌سازی حساب، لطفاً شماره تماس خود را تأیید کنید:', reply_markup=markup)
    
    # Store access code temporarily
    bot.register_next_step_handler_by_chat_id(user_id, lambda msg: handle_contact_with_access_code(msg, access_code))

def handle_contact_with_access_code(message, access_code):
    user_id = message.from_user.id
    
    if message.content_type != 'contact':
        bot.send_message(user_id, '❌ لطفاً شماره تماس خود را ارسال کنید.')
        return
    
    if message.contact.user_id != user_id:
        bot.send_message(user_id, '❌ لطفاً فقط شماره تماس خودتان را به اشتراک بگذارید.')
        return
    
    phone_number = message.contact.phone_number
    username = message.from_user.username
    
    # Activate publisher account
    if database.activate_publisher_account(access_code, user_id, phone_number, username):
        bot.send_message(user_id, '🎉 حساب شما با موفقیت فعال شد! به پنل ناشران هشتونیم خوش آمدید.', reply_markup=create_publisher_panel())
    else:
        bot.send_message(user_id, '❌ خطا در فعال‌سازی حساب. لطفاً با پشتیبانی تماس بگیرید.', reply_markup=create_main_menu())

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.from_user.id
    phone_number = message.contact.phone_number
    username = message.from_user.username

    # Check if the sent contact belongs to the user
    if message.contact.user_id != user_id:
        bot.send_message(user_id, '❌ لطفاً فقط شماره تماس خودتان را به اشتراک بگذارید.')
        return

    # Add publisher to the database (old method for direct registration)
    database.add_publisher(user_id, phone_number, username)

    bot.send_message(user_id, '✅ ثبت‌نام شما با موفقیت انجام شد! به پنل ناشران خوش آمدید.', reply_markup=create_publisher_panel())
    bot.send_message(user_id, 'از این پس می‌توانید از دکمه‌های زیر برای کار با ربات استفاده کنید.')


# --- PUBLISHER PANEL HANDLERS ---

@bot.message_handler(func=lambda message: database.get_publisher(message.from_user.id) is not None)
def handle_publisher_options(message):
    user_id = message.from_user.id
    text = message.text

    if text == '🔗 دریافت لینک افیلیت':
        show_stores_for_link(user_id)


    elif text == '🖼️ دریافت محتوای تبلیغاتی':
        show_stores_for_content(user_id)


    elif text == '📊 آمار عملکرد من':
        publisher = database.get_publisher(user_id)
        if not publisher:
            bot.send_message(user_id, 'خطا: اطلاعات ناشر یافت نشد.')
            return

        publisher_id = publisher[0]
        stats = get_publisher_stats(publisher_id) # Dummy stats function

        response = f"""📊 آمار عملکرد شما (کلی):

🔗 تعداد کلیک‌ها: {stats['clicks']}
📱 تعداد لیدها (ثبت شماره): {stats['leads']}
✅ تعداد سفارشات نهایی: {stats['orders']}

📈 نرخ تبدیل (کلیک به سفارش): {stats['conversion_rate']:.2f}%

توجه: این آمار به صورت دوره‌ای به‌روزرسانی می‌شود."""
        bot.send_message(user_id, response)

    elif text == '👤 پروفایل من':
        publisher_data = database.get_publisher(user_id)
        if not publisher_data:
            bot.send_message(user_id, 'خطایی رخ داده است. لطفاً با /start مجدداً تلاش کنید.')
            return
        
        # New structure: id, user_id, phone_number, telegram_username, page_username, publisher_code, access_code, is_active, registration_date, created_by_admin
        _, _, phone, tg_user, page_user, publisher_code, access_code, is_active, reg_date, created_by_admin = publisher_data
        
        response = '👤 مشخصات پروفایل شما:\n\n'
        response += f'📞 شماره تماس: {phone}\n'
        response += f'📱 یوزرنیم تلگرام: @{tg_user or "-"}\n'
        response += f'📸 یوزرنیم پیج اینستاگرام: @{page_user or "هنوز ثبت نشده"}\n'
        response += f'🔸 کد ناشر: {publisher_code or "نامشخص"}\n'
        response += f'📅 تاریخ عضویت: {reg_date or "نامشخص"}'

        bot.send_message(user_id, response, reply_markup=create_publisher_menu())
    
    elif text == '✏️ تغییر یوزرنیم اینستاگرام':
        markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        markup.add(KeyboardButton('🔙 برگشت به منوی اصلی'))
        
        msg = bot.send_message(user_id, '✏️ یوزرنیم جدید پیج اینستاگرام خود را بدون @ وارد کنید (مثال: my_page):', reply_markup=markup)
        bot.register_next_step_handler(msg, process_page_username)

def process_page_username(message):
    user_id = message.from_user.id
    page_username = message.text

    # Handle back button
    if page_username == '🔙 برگشت به منوی اصلی':
        bot.send_message(user_id, '🏠 منوی اصلی', reply_markup=create_publisher_menu())
        return

    if page_username.startswith('@'):
        page_username = page_username[1:] # Remove the @
    
    database.update_page_username(user_id, page_username)
    bot.send_message(user_id, f'✅ یوزرنیم پیج اینستاگرام شما به @{page_username} تغییر یافت.', reply_markup=create_publisher_menu())


def show_stores_for_link(user_id):
    markup = telebot.types.InlineKeyboardMarkup()
    
    # Get stores from database
    stores = database.get_all_stores()
    if not stores:
        bot.send_message(user_id, 'هیچ فروشگاه فعالی یافت نشد.')
        return
    
    for store in stores:
        store_id, name, base_url, is_active, created_date = store
        if is_active:
            markup.add(telebot.types.InlineKeyboardButton(text=name, callback_data=f'link_{store_id}'))
    
    # Add back button
    markup.add(telebot.types.InlineKeyboardButton(text='🔙 برگشت به منوی اصلی', callback_data='back_to_main'))
    
    bot.send_message(user_id, 'لطفاً فروشگاهی که می‌خواهید برای آن لینک بسازید را انتخاب کنید:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('link_'))
def handle_link_generation(call):
    user_id = call.from_user.id
    store_id = call.data.replace('link_', '')

    publisher = database.get_publisher(user_id)
    if not publisher:
        bot.answer_callback_query(call.id, 'خطا: اطلاعات ناشر یافت نشد.')
        return

    # Get publisher ID for affiliate link (should be just the number)
    publisher_id = publisher[0]  # Use publisher ID directly

    # Get store info from database
    stores = database.get_all_stores()
    selected_store = None
    for store in stores:
        if str(store[0]) == store_id:
            selected_store = store
            break
    
    if not selected_store:
        bot.answer_callback_query(call.id, 'فروشگاه یافت نشد.')
        return

    store_name = selected_store[1]
    base_url = selected_store[2]
    affiliate_link = f'https://{base_url}/{publisher_id}'

    response_text = f'✅ لینک افیلیت شما برای فروشگاه {store_name} ساخته شد:\n\n{affiliate_link}\n\nاین لینک را در استوری یا پست خود قرار دهید تا فروش شما ثبت شود.'

    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=response_text)
    bot.answer_callback_query(call.id, 'لینک شما با موفقیت ساخته شد!')

# Handle back to main menu button
@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main')
def handle_back_to_main(call):
    user_id = call.from_user.id
    
    # Check if user is publisher or admin
    if database.get_publisher(user_id):
        bot.edit_message_text('🏠 منوی اصلی', chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, '🏠 منوی اصلی پابلیشر', reply_markup=create_publisher_menu())
    elif database.is_admin(user_id) or user_id == SUPER_ADMIN_ID:
        bot.edit_message_text('🏠 پنل ادمین', chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, '🏠 پنل ادمین', reply_markup=create_admin_panel())
    else:
        bot.edit_message_text('🏠 منوی اصلی', chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, '🏠 منوی اصلی', reply_markup=create_main_menu())
    
    bot.answer_callback_query(call.id, 'بازگشت به منوی اصلی')

# Handle back to admin panel button
@bot.callback_query_handler(func=lambda call: call.data == 'back_to_admin')
def handle_back_to_admin(call):
    user_id = call.from_user.id
    
    if database.is_admin(user_id) or user_id == SUPER_ADMIN_ID:
        bot.edit_message_text('🏠 پنل ادمین', chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, '🏠 پنل ادمین', reply_markup=create_admin_panel())
    else:
        bot.edit_message_text('❌ دسترسی غیرمجاز', chat_id=user_id, message_id=call.message.message_id)
    
    bot.answer_callback_query(call.id, 'بازگشت به پنل ادمین')


def show_stores_for_content(user_id):
    markup = telebot.types.InlineKeyboardMarkup()
    
    # Get stores from database
    stores = database.get_all_stores()
    if not stores:
        bot.send_message(user_id, 'هیچ فروشگاه فعالی یافت نشد.')
        return
    
    for store in stores:
        store_id, name, base_url, is_active, created_date = store
        if is_active:
            markup.add(telebot.types.InlineKeyboardButton(text=name, callback_data=f'content_{store_id}'))
    
    # Add back button
    markup.add(telebot.types.InlineKeyboardButton(text='🔙 برگشت به منوی اصلی', callback_data='back_to_main'))
    
    bot.send_message(user_id, 'لطفاً فروشگاهی که می‌خواهید محتوای آن را دریافت کنید را انتخاب کنید:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('content_'))
def handle_content_request(call):
    user_id = call.from_user.id
    store_id = call.data.replace('content_', '')

    # Get store info from database
    stores = database.get_all_stores()
    selected_store = None
    for store in stores:
        if str(store[0]) == store_id:
            selected_store = store
            break
    
    if not selected_store:
        bot.answer_callback_query(call.id, 'فروشگاه یافت نشد.')
        return

    store_name = selected_store[1]
    # Use store name for content folder (simplified)
    content_path = os.path.join('content', f'store_{store_id}')

    if not os.path.isdir(content_path) or not os.listdir(content_path):
        bot.edit_message_text(f'متأسفانه در حال حاضر محتوایی برای فروشگاه {store_name} موجود نیست.', chat_id=user_id, message_id=call.message.message_id)
        bot.answer_callback_query(call.id, 'محتوایی یافت نشد.')
        return

    bot.edit_message_text('در حال ارسال محتوای تبلیغاتی... لطفاً منتظر بمانید.', chat_id=user_id, message_id=call.message.message_id)
    bot.answer_callback_query(call.id, 'در حال ارسال...')

    media_files = []
    for filename in os.listdir(content_path):
        file_path = os.path.join(content_path, filename)
        try:
            # Skip non-media files and check file size
            if os.path.getsize(file_path) == 0:
                continue
                
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                media_files.append(telebot.types.InputMediaPhoto(open(file_path, 'rb')))
            elif filename.lower().endswith(('.mp4', '.mov', '.avi')):
                media_files.append(telebot.types.InputMediaVideo(open(file_path, 'rb')))
        except Exception as e:
            print(f"Error opening file {file_path}: {e}")

    if media_files:
        # Send files in groups of 10 (Telegram limit)
        for i in range(0, len(media_files), 10):
            batch = media_files[i:i+10]
            if i == 0:
                batch[0].caption = f"📦 محتوای تبلیغاتی {store_name}\n\n🔗 لینک افیلیت شما را از منوی اصلی دریافت کنید\n📱 این محتوا را در استوری یا پست خود استفاده کنید"
            
            try:
                bot.send_media_group(user_id, batch)
            except Exception as e:
                print(f"Error sending media group: {e}")
                # If media group fails, send files individually
                for media in batch:
                    try:
                        if hasattr(media, 'media'):
                            if 'photo' in str(type(media)):
                                bot.send_photo(user_id, media.media, caption=media.caption if hasattr(media, 'caption') else None)
                            elif 'video' in str(type(media)):
                                bot.send_video(user_id, media.media, caption=media.caption if hasattr(media, 'caption') else None)
                    except Exception as e2:
                        print(f"Error sending individual file: {e2}")
        
        # Send usage instructions
        instructions = (
            "📋 راهنمای استفاده:\n\n"
            "1️⃣ محتوای بالا را در گالری خود ذخیره کنید\n"
            "2️⃣ از منوی اصلی 'دریافت لینک افیلیت' را انتخاب کنید\n"
            "3️⃣ لینک اختصاصی خود را کپی کنید\n"
            "4️⃣ محتوا را همراه با لینک در استوری یا پست خود منتشر کنید\n\n"
            "💡 نکته: حتماً لینک اختصاصی خود را استفاده کنید تا فروش‌ها به حساب شما ثبت شود."
        )
        bot.send_message(user_id, instructions)
        
    else:
        bot.send_message(user_id, '📭 متأسفانه محتوایی برای این فروشگاه موجود نیست.\n\n💬 لطفاً با ادمین تماس بگیرید تا محتوای جدید اضافه شود.')


def get_publisher_stats(publisher_id):
    """Generates dummy performance stats for a given publisher ID."""
    # In a real application, this would fetch data from an analytics service or database.
    # The stats can be keyed by publisher_id to seem more realistic.
    clicks = 1234 + (publisher_id * 15)
    leads = 87 + (publisher_id * 3)
    orders = 56 + publisher_id
    conversion_rate = (orders / clicks) * 100 if clicks > 0 else 0
    
    return {
        'clicks': clicks,
        'leads': leads,
        'orders': orders,
        'conversion_rate': conversion_rate
    }


# --- ADMIN PANEL HANDLERS ---

@bot.message_handler(func=lambda message: message.text == '🔙 برگشت به پنل ادمین')
def back_to_admin_panel(message):
    user_id = message.from_user.id
    if database.is_admin(user_id) or user_id == SUPER_ADMIN_ID:
        bot.send_message(user_id, '🔙 برگشت به پنل ادمین', reply_markup=create_admin_panel())

# --- PUBLISHER MANAGEMENT ---
@bot.message_handler(func=lambda message: message.text == '👥 مدیریت ناشران')
def admin_publishers_menu(message):
    user_id = message.from_user.id
    if database.is_admin(user_id) or user_id == SUPER_ADMIN_ID:
        bot.send_message(user_id, '👥 مدیریت ناشران', reply_markup=create_admin_publishers_menu())

@bot.message_handler(func=lambda message: message.text == '➕ افزودن ناشر جدید')
def add_new_publisher(message):
    user_id = message.from_user.id
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        return
    
    msg = bot.send_message(user_id, '📝 لطفاً یوزرنیم پیج اینستاگرام را وارد کنید (بدون @):', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_new_publisher_page)

def process_new_publisher_page(message):
    user_id = message.from_user.id
    page_username = message.text.strip().replace('@', '')
    
    msg = bot.send_message(user_id, f'📝 کد ناشر برای پیج @{page_username} را وارد کنید (فرمت: P0X مثل P01, P02) یا خالی بگذارید تا خودکار تولید شود:')
    bot.register_next_step_handler(msg, lambda m: process_new_publisher_code(m, page_username))

def process_new_publisher_code(message, page_username):
    user_id = message.from_user.id
    publisher_code = message.text.strip()
    
    # If empty, let database auto-generate P0X format
    if not publisher_code:
        publisher_code = None
    
    # Generate random 6-digit access code
    import random
    access_code = str(random.randint(100000, 999999))
    
    result = database.create_publisher_by_admin(page_username, publisher_code, access_code, user_id)
    if result:
        # Get the actual publisher code that was created
        created_publisher = database.get_publisher_by_id(result)
        actual_publisher_code = created_publisher[5] if created_publisher else publisher_code
        
        response = f'''✅ ناشر جدید با موفقیت ایجاد شد!

📄 اطلاعات ناشر:
🔸 پیج: @{page_username}
🔸 کد ناشر: {actual_publisher_code}
🔸 کد دسترسی: {access_code}

📋 این کد دسترسی را به صاحب پیج ارسال کنید تا بتواند وارد ربات شود.'''
        
        bot.send_message(user_id, response, reply_markup=create_admin_publishers_menu())
    else:
        bot.send_message(user_id, '❌ خطا در ایجاد ناشر. ممکن است کد ناشر یا کد دسترسی تکراری باشد.', reply_markup=create_admin_publishers_menu())

# --- STORE MANAGEMENT ---
@bot.message_handler(func=lambda message: message.text == '🏪 مدیریت فروشگاه‌ها')
def admin_stores_menu(message):
    user_id = message.from_user.id
    if database.is_admin(user_id) or user_id == SUPER_ADMIN_ID:
        bot.send_message(user_id, '🏪 مدیریت فروشگاه‌ها', reply_markup=create_admin_stores_menu())

@bot.message_handler(func=lambda message: message.text == '🏪 مشاهده فروشگاه‌ها')
def view_stores(message):
    user_id = message.from_user.id
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        return
    
    stores = database.get_all_stores()
    if not stores:
        bot.send_message(user_id, 'هنوز هیچ فروشگاهی ثبت نشده است.')
        return
    
    response = '🏪 لیست فروشگاه‌ها:\n\n'
    for store in stores:
        store_id, name, base_url, is_active, created_date = store
        status = "🟢 فعال" if is_active else "🔴 غیرفعال"
        response += f'🔸 {name}\n   🌐 {base_url}\n   📊 وضعیت: {status}\n\n'
    
    bot.send_message(user_id, response)

@bot.message_handler(func=lambda message: message.text == '➕ افزودن فروشگاه')
def add_store_handler(message):
    user_id = message.from_user.id
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        return
    
    msg = bot.send_message(user_id, '🏪 نام فروشگاه جدید را وارد کنید:', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_store_name)

def process_store_name(message):
    user_id = message.from_user.id
    store_name = message.text.strip()
    
    msg = bot.send_message(user_id, f'🌐 URL پایه برای فروشگاه "{store_name}" را وارد کنید:\n\nمثال: lfshop.ir/newstore')
    bot.register_next_step_handler(msg, lambda m: process_store_url(m, store_name))

def process_store_url(message, store_name):
    user_id = message.from_user.id
    base_url = message.text.strip()
    
    store_id = database.add_store(store_name, base_url)
    if store_id:
        bot.send_message(user_id, f'✅ فروشگاه "{store_name}" با موفقیت اضافه شد!\n\n🆔 شناسه فروشگاه: {store_id}\n🌐 URL: {base_url}', 
                        reply_markup=create_admin_stores_menu())
    else:
        bot.send_message(user_id, '❌ خطا در افزودن فروشگاه. لطفاً مجدداً تلاش کنید.', 
                        reply_markup=create_admin_stores_menu())

# --- PRODUCT MANAGEMENT ---
@bot.message_handler(func=lambda message: message.text == '📦 مدیریت محصولات')
def admin_products_menu(message):
    user_id = message.from_user.id
    if database.is_admin(user_id) or user_id == SUPER_ADMIN_ID:
        bot.send_message(user_id, '📦 مدیریت محصولات', reply_markup=create_admin_products_menu())

@bot.message_handler(func=lambda message: message.text == '📦 مشاهده محصولات')
def view_products(message):
    user_id = message.from_user.id
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        return
    
    stores = database.get_all_stores()
    response = '📦 لیست محصولات:\n\n'
    
    for store in stores:
        store_id, store_name = store[0], store[1]
        products = database.get_products_by_store(store_id)
        
        response += f'🏪 {store_name}:\n'
        if products:
            for product in products:
                prod_id, _, name, desc, price, discount, is_active, _ = product
                final_price = price - discount
                status = "🟢" if is_active else "🔴"
                response += f'  {status} {name}\n'
                response += f'     💰 قیمت: {price:,} تومان\n'
                if discount > 0:
                    response += f'     🎁 تخفیف: {discount:,} تومان\n'
                    response += f'     💸 قیمت نهایی: {final_price:,} تومان\n'
                response += '\n'
        else:
            response += '  هیچ محصولی یافت نشد\n\n'
    
    bot.send_message(user_id, response)

@bot.message_handler(func=lambda message: message.text == '➕ افزودن محصول')
def add_product_handler(message):
    user_id = message.from_user.id
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        return
    
    stores = database.get_all_stores()
    if not stores:
        bot.send_message(user_id, '❌ ابتدا باید حداقل یک فروشگاه اضافه کنید.')
        return
    
    markup = telebot.types.InlineKeyboardMarkup()
    for store in stores:
        store_id, name, base_url, is_active, created_date = store
        if is_active:
            markup.add(telebot.types.InlineKeyboardButton(text=f'🏪 {name}', callback_data=f'addprod_{store_id}'))
    
    bot.send_message(user_id, '🏪 محصول جدید را به کدام فروشگاه اضافه می‌کنید؟', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('addprod_'))
def handle_add_product(call):
    user_id = call.from_user.id
    store_id = call.data.replace('addprod_', '')
    
    # Get store name
    stores = database.get_all_stores()
    store_name = "نامشخص"
    for store in stores:
        if str(store[0]) == store_id:
            store_name = store[1]
            break
    
    bot.edit_message_text(f'📦 نام محصول جدید برای فروشگاه "{store_name}" را وارد کنید:', 
                         chat_id=user_id, message_id=call.message.message_id)
    bot.answer_callback_query(call.id, 'منتظر نام محصول...')
    
    bot.register_next_step_handler_by_chat_id(user_id, lambda msg: process_product_name(msg, store_id, store_name))

def process_product_name(message, store_id, store_name):
    user_id = message.from_user.id
    product_name = message.text.strip()
    
    msg = bot.send_message(user_id, f'📝 توضیحات محصول "{product_name}" را وارد کنید:')
    bot.register_next_step_handler(msg, lambda m: process_product_description(m, store_id, store_name, product_name))

def process_product_description(message, store_id, store_name, product_name):
    user_id = message.from_user.id
    description = message.text.strip()
    
    msg = bot.send_message(user_id, f'💰 قیمت محصول "{product_name}" را به تومان وارد کنید:\n\nمثال: 370000')
    bot.register_next_step_handler(msg, lambda m: process_product_price(m, store_id, store_name, product_name, description))

def process_product_price(message, store_id, store_name, product_name, description):
    user_id = message.from_user.id
    
    try:
        price = int(message.text.strip())
        msg = bot.send_message(user_id, f'🎁 مبلغ تخفیف برای محصول "{product_name}" را به تومان وارد کنید:\n\nمثال: 100000\n\n(برای عدم تخفیف عدد 0 را وارد کنید)')
        bot.register_next_step_handler(msg, lambda m: process_product_discount(m, store_id, store_name, product_name, description, price))
    except ValueError:
        msg = bot.send_message(user_id, '❌ لطفاً قیمت را به صورت عددی وارد کنید:')
        bot.register_next_step_handler(msg, lambda m: process_product_price(m, store_id, store_name, product_name, description))

def process_product_discount(message, store_id, store_name, product_name, description, price):
    user_id = message.from_user.id
    
    try:
        discount = int(message.text.strip())
        
        product_id = database.add_product(store_id, product_name, description, price, discount)
        if product_id:
            final_price = price - discount
            response = f'''✅ محصول "{product_name}" با موفقیت اضافه شد!

🏪 فروشگاه: {store_name}
📦 محصول: {product_name}
📝 توضیحات: {description}
💰 قیمت اصلی: {price:,} تومان
🎁 تخفیف: {discount:,} تومان
💸 قیمت نهایی: {final_price:,} تومان
🆔 شناسه محصول: {product_id}'''
            
            bot.send_message(user_id, response, reply_markup=create_admin_products_menu())
        else:
            bot.send_message(user_id, '❌ خطا در افزودن محصول. لطفاً مجدداً تلاش کنید.', 
                           reply_markup=create_admin_products_menu())
    except ValueError:
        msg = bot.send_message(user_id, '❌ لطفاً مبلغ تخفیف را به صورت عددی وارد کنید:')
        bot.register_next_step_handler(msg, lambda m: process_product_discount(m, store_id, store_name, product_name, description, price))

# --- CONTENT MANAGEMENT ---
@bot.message_handler(func=lambda message: message.text == '🖼️ مدیریت محتوا')
def admin_content_menu(message):
    user_id = message.from_user.id
    if database.is_admin(user_id) or user_id == SUPER_ADMIN_ID:
        markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn1 = KeyboardButton('📤 آپلود محتوا')
        btn2 = KeyboardButton('📋 مشاهده محتوا')
        btn3 = KeyboardButton('🗑️ حذف محتوا')
        btn4 = KeyboardButton('🔙 برگشت به پنل ادمین')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(user_id, '🖼️ مدیریت محتوا', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '📤 آپلود محتوا')
def upload_content_menu(message):
    user_id = message.from_user.id
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        return
    
    # Show stores to select for content upload
    stores = database.get_all_stores()
    if not stores:
        bot.send_message(user_id, 'هیچ فروشگاهی یافت نشد.')
        return
    
    markup = telebot.types.InlineKeyboardMarkup()
    for store in stores:
        store_id, name, base_url, is_active, created_date = store
        if is_active:
            markup.add(telebot.types.InlineKeyboardButton(text=f'📤 {name}', callback_data=f'upload_{store_id}'))
    
    # Add back button
    markup.add(telebot.types.InlineKeyboardButton(text='🔙 برگشت به پنل ادمین', callback_data='back_to_admin'))
    
    bot.send_message(user_id, '📤 برای کدام فروشگاه محتوا آپلود می‌کنید؟', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('upload_'))
def handle_content_upload(call):
    user_id = call.from_user.id
    store_id = call.data.replace('upload_', '')
    
    # Get store name
    stores = database.get_all_stores()
    store_name = "نامشخص"
    for store in stores:
        if str(store[0]) == store_id:
            store_name = store[1]
            break
    
    bot.edit_message_text(f'📤 آپلود محتوا برای {store_name}\n\nلطفاً فایل‌های تصویری یا ویدیویی خود را ارسال کنید.\n\n⚠️ برای پایان آپلود، پیام "پایان" را ارسال کنید.', 
                         chat_id=user_id, message_id=call.message.message_id)
    bot.answer_callback_query(call.id, 'آماده دریافت فایل‌ها')
    
    # Store the store_id for this user's upload session
    if not hasattr(bot, 'upload_sessions'):
        bot.upload_sessions = {}
    bot.upload_sessions[user_id] = store_id

@bot.message_handler(content_types=['photo', 'video', 'document'])
def handle_file_upload(message):
    user_id = message.from_user.id
    
    # Check if user is in upload session
    if not hasattr(bot, 'upload_sessions') or user_id not in bot.upload_sessions:
        return
    
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        return
    
    store_id = bot.upload_sessions[user_id]
    
    # Create content directory if it doesn't exist
    import os
    content_dir = os.path.join('content', f'store_{store_id}')
    os.makedirs(content_dir, exist_ok=True)
    
    try:
        file_info = None
        file_extension = ""
        
        if message.content_type == 'photo':
            file_info = bot.get_file(message.photo[-1].file_id)
            file_extension = ".jpg"
        elif message.content_type == 'video':
            file_info = bot.get_file(message.video.file_id)
            file_extension = ".mp4"
        elif message.content_type == 'document':
            file_info = bot.get_file(message.document.file_id)
            file_name = message.document.file_name
            file_extension = os.path.splitext(file_name)[1] if file_name else ".file"
        
        if file_info:
            downloaded_file = bot.download_file(file_info.file_path)
            
            # Generate unique filename
            import time
            timestamp = str(int(time.time()))
            file_path = os.path.join(content_dir, f"{timestamp}{file_extension}")
            
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            bot.reply_to(message, f'✅ فایل با موفقیت آپلود شد!\n📁 مسیر: {file_path}')
        
    except Exception as e:
        bot.reply_to(message, f'❌ خطا در آپلود فایل: {str(e)}')

@bot.message_handler(func=lambda message: message.text == 'پایان' and hasattr(bot, 'upload_sessions') and message.from_user.id in bot.upload_sessions)
def end_upload_session(message):
    user_id = message.from_user.id
    
    if hasattr(bot, 'upload_sessions') and user_id in bot.upload_sessions:
        del bot.upload_sessions[user_id]
    
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton('📤 آپلود محتوا')
    btn2 = KeyboardButton('📋 مشاهده محتوا')
    btn3 = KeyboardButton('🗑️ حذف محتوا')
    btn4 = KeyboardButton('🔙 برگشت به پنل ادمین')
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(user_id, '✅ جلسه آپلود به پایان رسید.', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '📋 مشاهده محتوا')
def view_content_menu(message):
    user_id = message.from_user.id
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        return
    
    import os
    stores = database.get_all_stores()
    
    if not stores:
        bot.send_message(user_id, 'هیچ فروشگاهی یافت نشد.')
        return
    
    markup = telebot.types.InlineKeyboardMarkup()
    for store in stores:
        store_id, store_name = store[0], store[1]
        content_dir = os.path.join('content', f'store_{store_id}')
        
        if os.path.exists(content_dir) and os.listdir(content_dir):
            file_count = len(os.listdir(content_dir))
            markup.add(telebot.types.InlineKeyboardButton(
                text=f'📋 {store_name} ({file_count} فایل)', 
                callback_data=f'viewcontent_{store_id}'
            ))
    
    # Add back button
    markup.add(telebot.types.InlineKeyboardButton(text='🔙 برگشت به پنل ادمین', callback_data='back_to_admin'))
    
    if markup.keyboard:
        bot.send_message(user_id, '📋 محتوای کدام فروشگاه را می‌خواهید مشاهده کنید؟', reply_markup=markup)
    else:
        bot.send_message(user_id, '📭 محتوایی برای نمایش یافت نشد.')

@bot.callback_query_handler(func=lambda call: call.data.startswith('viewcontent_'))
def handle_view_content(call):
    user_id = call.from_user.id
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        bot.answer_callback_query(call.id, 'دسترسی غیرمجاز')
        return
    
    store_id = call.data.replace('viewcontent_', '')
    
    # Get store name
    stores = database.get_all_stores()
    store_name = "نامشخص"
    for store in stores:
        if str(store[0]) == store_id:
            store_name = store[1]
            break
    
    import os
    content_dir = os.path.join('content', f'store_{store_id}')
    
    if not os.path.exists(content_dir) or not os.listdir(content_dir):
        bot.edit_message_text(f'📭 محتوایی برای فروشگاه {store_name} یافت نشد.', 
                             chat_id=user_id, message_id=call.message.message_id)
        return
    
    bot.edit_message_text(f'📋 در حال ارسال محتوای فروشگاه {store_name}...', 
                         chat_id=user_id, message_id=call.message.message_id)
    bot.answer_callback_query(call.id, 'در حال ارسال...')
    
    # Send files like for publishers
    media_files = []
    for filename in os.listdir(content_dir):
        file_path = os.path.join(content_dir, filename)
        try:
            # Skip non-media files and check file size
            if os.path.getsize(file_path) == 0:
                continue
                
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                media_files.append(telebot.types.InputMediaPhoto(open(file_path, 'rb')))
            elif filename.lower().endswith(('.mp4', '.mov', '.avi')):
                media_files.append(telebot.types.InputMediaVideo(open(file_path, 'rb')))
        except Exception as e:
            print(f"Error opening file {file_path}: {e}")

    if media_files:
        # Send files in groups of 10 (Telegram limit)
        for i in range(0, len(media_files), 10):
            batch = media_files[i:i+10]
            if i == 0:
                batch[0].caption = f"📋 محتوای فروشگاه {store_name} (پیش‌نمایش ادمین)"
            
            try:
                bot.send_media_group(user_id, batch)
            except Exception as e:
                print(f"Error sending media group: {e}")
                # If media group fails, send files individually
                for media in batch:
                    try:
                        if hasattr(media, 'media'):
                            if 'photo' in str(type(media)):
                                bot.send_photo(user_id, media.media, caption=media.caption if hasattr(media, 'caption') else None)
                            elif 'video' in str(type(media)):
                                bot.send_video(user_id, media.media, caption=media.caption if hasattr(media, 'caption') else None)
                    except Exception as e2:
                        print(f"Error sending individual file: {e2}")
        
        # Send summary
        summary = f"✅ نمایش محتوای فروشگاه {store_name} تکمیل شد.\n📁 تعداد فایل‌ها: {len(media_files)}"
        bot.send_message(user_id, summary)
    else:
        bot.send_message(user_id, f'❌ خطا در خواندن فایل‌های فروشگاه {store_name}.')

@bot.message_handler(func=lambda message: message.text == '🗑️ حذف محتوا')
def delete_content_menu(message):
    user_id = message.from_user.id
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        return
    
    import os
    stores = database.get_all_stores()
    markup = telebot.types.InlineKeyboardMarkup()
    
    for store in stores:
        store_id, store_name = store[0], store[1]
        content_dir = os.path.join('content', f'store_{store_id}')
        
        if os.path.exists(content_dir) and os.listdir(content_dir):
            file_count = len(os.listdir(content_dir))
            markup.add(telebot.types.InlineKeyboardButton(
                text=f'🗑️ {store_name} ({file_count} فایل)', 
                callback_data=f'delete_{store_id}'
            ))
    
    # Add back button
    markup.add(telebot.types.InlineKeyboardButton(text='🔙 برگشت به پنل ادمین', callback_data='back_to_admin'))
    
    if markup.keyboard:
        bot.send_message(user_id, '🗑️ محتوای کدام فروشگاه را می‌خواهید حذف کنید؟', reply_markup=markup)
    else:
        bot.send_message(user_id, '📭 محتوایی برای حذف یافت نشد.')

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
def handle_content_delete(call):
    user_id = call.from_user.id
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        bot.answer_callback_query(call.id, 'دسترسی غیرمجاز')
        return
    
    store_id = call.data.replace('delete_', '')
    
    # Get store name
    stores = database.get_all_stores()
    store_name = "نامشخص"
    for store in stores:
        if str(store[0]) == store_id:
            store_name = store[1]
            break
    
    # Confirmation markup
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton('✅ بله، حذف کن', callback_data=f'confirm_delete_{store_id}'),
        telebot.types.InlineKeyboardButton('❌ انصراف', callback_data='cancel_delete')
    )
    
    import os
    content_dir = os.path.join('content', f'store_{store_id}')
    file_count = len(os.listdir(content_dir)) if os.path.exists(content_dir) else 0
    
    bot.edit_message_text(
        f'⚠️ هشدار!\n\nآیا مطمئن هستید که می‌خواهید تمام محتوای فروشگاه "{store_name}" را حذف کنید؟\n\n📁 تعداد فایل‌ها: {file_count}\n\n❗ این عمل غیرقابل بازگشت است!',
        chat_id=user_id,
        message_id=call.message.message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_delete_'))
def confirm_content_delete(call):
    user_id = call.from_user.id
    if not (database.is_admin(user_id) or user_id == SUPER_ADMIN_ID):
        bot.answer_callback_query(call.id, 'دسترسی غیرمجاز')
        return
    
    store_id = call.data.replace('confirm_delete_', '')
    
    import os
    import shutil
    content_dir = os.path.join('content', f'store_{store_id}')
    
    try:
        if os.path.exists(content_dir):
            shutil.rmtree(content_dir)
            bot.edit_message_text(
                '✅ محتوای فروشگاه با موفقیت حذف شد!',
                chat_id=user_id,
                message_id=call.message.message_id
            )
        else:
            bot.edit_message_text(
                '❌ پوشه محتوا یافت نشد.',
                chat_id=user_id,
                message_id=call.message.message_id
            )
    except Exception as e:
        bot.edit_message_text(
            f'❌ خطا در حذف محتوا: {str(e)}',
            chat_id=user_id,
            message_id=call.message.message_id
        )
    
    bot.answer_callback_query(call.id, 'عملیات انجام شد')

@bot.callback_query_handler(func=lambda call: call.data == 'cancel_delete')
def cancel_content_delete(call):
    bot.edit_message_text(
        '❌ عملیات حذف لغو شد.',
        chat_id=call.from_user.id,
        message_id=call.message.message_id
    )
    bot.answer_callback_query(call.id, 'لغو شد')

# --- ADMIN MANAGEMENT ---
@bot.message_handler(func=lambda message: message.text == '👨‍💼 مدیریت ادمین‌ها')
def admin_admins_menu(message):
    user_id = message.from_user.id
    if database.is_admin(user_id) or user_id == SUPER_ADMIN_ID:
        bot.send_message(user_id, '👨‍💼 مدیریت ادمین‌ها', reply_markup=create_admin_admins_menu())

@bot.message_handler(func=lambda message: database.is_admin(message.from_user.id) or message.from_user.id == SUPER_ADMIN_ID)
def handle_admin_options(message):
    user_id = message.from_user.id
    text = message.text

    if text == '👥 مشاهده لیست ناشران':
        publishers = database.get_all_publishers_for_admin()
        if not publishers:
            bot.send_message(user_id, 'هنوز هیچ ناشری ایجاد نشده است.')
            return

        response = '👥 لیست کامل ناشران:\n\n'
        for i, pub in enumerate(publishers, 1):
            pub_id, user_id_pub, page_user, publisher_code, access_code, phone, tg_user, is_active = pub
            
            status = "🟢 فعال" if is_active and user_id_pub else "🔴 در انتظار فعال‌سازی"
            if not is_active:
                status = "⚫ غیرفعال"
            
            response += f'{i}. @{page_user or "نامشخص"}\n'
            response += f'   🆔 کد ناشر: {publisher_code}\n'
            response += f'   🔑 کد دسترسی: {access_code}\n'
            response += f'   📊 وضعیت: {status}\n'
            
            if user_id_pub:
                response += f'   👤 آیدی تلگرام: {user_id_pub}\n'
                response += f'   📞 شماره تماس: {phone or "ثبت نشده"}\n'
                response += f'   📱 یوزرنیم تلگرام: @{tg_user or "-"}\n'
            
            response += '\n'
        
        # Split message if it's too long for Telegram
        if len(response) > 4096:
            for x in range(0, len(response), 4096):
                bot.send_message(user_id, response[x:x+4096])
        else:
            bot.send_message(user_id, response)

    elif text == '📜 لیست ادمین‌ها':
        admins = database.get_all_admins()
        response = '👑 لیست ادمین‌ها:\n\n'
        for i, admin in enumerate(admins, 1):
            admin_id, admin_user = admin
            response += f'{i}. کاربر: {admin_id}'
            if admin_id == SUPER_ADMIN_ID:
                response += ' (سوپر ادمین)\n'
            else:
                response += f' (یوزرنیم: @{admin_user or "-"})\n'
        bot.send_message(user_id, response)

    elif text == '➕ افزودن ادمین':
        if user_id != SUPER_ADMIN_ID:
            bot.send_message(user_id, '❌ این دستور فقط توسط سوپر ادمین قابل اجراست.')
            return
        msg = bot.send_message(user_id, 'لطفاً شناسه کاربری (User ID) عددی ادمین جدید را وارد کنید:', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_add_admin_id)

    elif text == '➖ حذف ادمین':
        if user_id != SUPER_ADMIN_ID:
            bot.send_message(user_id, '❌ این دستور فقط توسط سوپر ادمین قابل اجراست.')
            return
        msg = bot.send_message(user_id, 'لطفاً شناسه کاربری (User ID) ادمینی که می‌خواهید حذف کنید را وارد کنید:', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_remove_admin_id)


def process_add_admin_id(message):
    user_id = message.from_user.id
    try:
        new_admin_id = int(message.text.strip())
        
        # Try to add admin to database
        if database.add_admin(new_admin_id, f"admin_{new_admin_id}"):
            bot.send_message(user_id, f'✅ ادمین جدید با موفقیت اضافه شد:\n🆔 شناسه: {new_admin_id}', reply_markup=create_admin_panel())
            
            # Try to send notification to new admin
            try:
                bot.send_message(new_admin_id, 'شما توسط سوپر ادمین به عنوان ادمین جدید انتخاب شدید. برای شروع /start را بزنید.')
            except Exception as e:
                print(f"Could not send notification to new admin {new_admin_id}: {e}")
                bot.send_message(user_id, f'⚠️ ادمین اضافه شد اما نتوانستیم پیام اطلاع‌رسانی ارسال کنیم. احتمالاً کاربر ربات را start نکرده است.')
        else:
            bot.send_message(user_id, '❌ خطا در افزودن ادمین. ممکن است این شناسه قبلاً ثبت شده باشد.', reply_markup=create_admin_panel())
    except ValueError:
        bot.send_message(user_id, '❌ لطفاً یک شناسه عددی معتبر وارد کنید.', reply_markup=create_admin_panel())

def process_remove_admin_id(message):
    try:
        admin_to_remove_id = int(message.text)
        if admin_to_remove_id == SUPER_ADMIN_ID:
            bot.send_message(message.from_user.id, '❌ شما نمی‌توانید سوپر ادمین را حذف کنید.', reply_markup=create_admin_panel())
            return

        if database.remove_admin(admin_to_remove_id):
            bot.send_message(message.from_user.id, f'✅ کاربر {admin_to_remove_id} با موفقیت از لیست ادمین‌ها حذف شد.', reply_markup=create_admin_panel())
            bot.send_message(admin_to_remove_id, 'دسترسی ادمین از شما گرفته شد.')
        else:
            bot.send_message(message.from_user.id, f'⚠️ کاربری با شناسه {admin_to_remove_id} در لیست ادمین‌ها یافت نشد.', reply_markup=create_admin_panel())

    except ValueError:
        bot.send_message(message.from_user.id, '❌ ورودی نامعتبر است. لطفاً فقط شناسه کاربری عددی را وارد کنید.', reply_markup=create_admin_panel())


# --- MAIN EXECUTION ---
if __name__ == '__main__':
    print("Bot is starting...")
    database.init_db()
    
    # Add the super admin to the admins table automatically on start
    if not database.is_admin(SUPER_ADMIN_ID):
        database.add_admin(SUPER_ADMIN_ID, 'superadmin')
    
    # Run bot with error handling and auto-restart
    while True:
        try:
            print("Starting bot polling...")
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"Bot polling error: {e}")
            print("Restarting bot in 10 seconds...")
            import time
            time.sleep(10)
            continue
