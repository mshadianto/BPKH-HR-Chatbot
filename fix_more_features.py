# Add this to replace handle_more_features in bot.py

async def handle_more_features(query):
    """More features with CLICKABLE buttons"""
    keyboard = [
        [
            InlineKeyboardButton("Expense Tracker", callback_data='expense_tracker'),
            InlineKeyboardButton("Team Collab", callback_data='team_collab')
        ],
        [
            InlineKeyboardButton("Learning Hub", callback_data='learning_hub'),
            InlineKeyboardButton("Wellness", callback_data='wellness')
        ],
        [
            InlineKeyboardButton("Document Vault", callback_data='doc_vault'),
            InlineKeyboardButton("Career Path", callback_data='career_path')
        ],
        [
            InlineKeyboardButton("Feedback", callback_data='feedback_system'),
            InlineKeyboardButton("Goals", callback_data='goal_tracker')
        ],
        [InlineKeyboardButton("Back", callback_data='main_menu')]
    ]
    
    text = (
        f"<b>MORE FEATURES</b>\n"
        f"{create_separator(30)}\n\n"
        f"<b>Advanced Tools</b>\n"
        f"Select a feature to explore:\n\n"
        f"<i>All features operational!</i>"
    )
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

# Add handlers for each feature
async def handle_expense_tracker(query):
    text = (
        "<b>EXPENSE TRACKER</b>\n"
        "------------------------------\n\n"
        "<b>Current Month:</b>\n"
        "  Transport: Rp 200,000\n"
        "  Meals: Rp 150,000\n"
        "  Supplies: Rp 50,000\n\n"
        "<b>Total:</b> Rp 400,000\n"
        "Status: Approved\n\n"
        "<i>Submit new expense claims here</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_team_collab(query):
    text = (
        "<b>TEAM COLLABORATION</b>\n"
        "------------------------------\n\n"
        "<b>Your Teams:</b>\n"
        "  - HR Department (12 members)\n"
        "  - Project Alpha (8 members)\n\n"
        "<b>Recent Activity:</b>\n"
        "  + 3 new tasks assigned\n"
        "  + 2 documents shared\n"
        "  + Team meeting scheduled\n\n"
        "<i>Stay connected with your team</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_learning_hub(query):
    text = (
        "<b>LEARNING HUB</b>\n"
        "------------------------------\n\n"
        "<b>Active Courses:</b>\n"
        "  1. Leadership Skills (65% done)\n"
        "  2. Excel Advanced (completed)\n"
        "  3. Python Basics (starting soon)\n\n"
        "<b>Your Progress:</b>\n"
        "  Learning Hours: 48h\n"
        "  Certificates: 3\n"
        "  Rank: Top 15%\n\n"
        "<i>Keep learning, keep growing!</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_wellness(query):
    text = (
        "<b>WELLNESS CENTER</b>\n"
        "------------------------------\n\n"
        "<b>Today's Activity:</b>\n"
        "  Steps: 7,250 / 10,000\n"
        "  Water: 6 / 8 glasses\n"
        "  Sleep: 7.5 hours\n\n"
        "<b>Programs Available:</b>\n"
        "  + Gym Membership\n"
        "  + Mental Health Support\n"
        "  + Yoga Classes\n\n"
        "<i>Your health is our priority</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_doc_vault(query):
    text = (
        "<b>DOCUMENT VAULT</b>\n"
        "------------------------------\n\n"
        "<b>Your Documents:</b>\n"
        "  Personal Docs (5 files)\n"
        "  Work Projects (12 files)\n"
        "  Certificates (3 files)\n\n"
        "<b>Storage:</b>\n"
        "  Used: 245 MB / 1 GB\n"
        "  [==========----------] 24%\n\n"
        "<b>Features:</b>\n"
        "  + Encrypted Storage\n"
        "  + Version Control\n"
        "  + E-signature Ready\n\n"
        "<i>Secure document management</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_career_path(query):
    text = (
        "<b>CAREER PATH</b>\n"
        "------------------------------\n\n"
        "<b>Current Position:</b>\n"
        "  Staff HR\n\n"
        "<b>Career Timeline:</b>\n"
        "  [Done] Junior Staff\n"
        "  [Current] Staff\n"
        "  [Next] Senior Staff\n"
        "  [Goal] Team Lead\n\n"
        "<b>Readiness Score:</b>\n"
        "  [=============-------] 75%\n\n"
        "<b>Next Steps:</b>\n"
        "  1. Complete leadership training\n"
        "  2. Lead 2 major projects\n"
        "  3. Mentor junior staff\n\n"
        "<i>Your growth matters</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_feedback_system(query):
    text = (
        "<b>FEEDBACK SYSTEM</b>\n"
        "------------------------------\n\n"
        "<b>Recent Feedback:</b>\n\n"
        "From Manager:\n"
        "  'Excellent problem-solving'\n"
        "  Rating: 4.5/5\n\n"
        "From Peers:\n"
        "  'Great team player'\n"
        "  Rating: 4.7/5\n\n"
        "<b>Overall Rating:</b> 4.6/5\n"
        "[==================--] 92%\n\n"
        "<i>Give and receive feedback</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def handle_goal_tracker(query):
    text = (
        "<b>GOAL TRACKER</b>\n"
        "------------------------------\n\n"
        "<b>Q4 2025 Goals:</b>\n\n"
        "1. Complete Project Alpha\n"
        "   [====================] 100%\n\n"
        "2. Team Performance\n"
        "   [===============-----] 75%\n\n"
        "3. Skill Development\n"
        "   [============--------] 60%\n\n"
        "4. Innovation Initiative\n"
        "   [--------------------] 0%\n\n"
        "<b>Overall:</b> 58% ON TRACK\n\n"
        "<i>Track your progress</i>"
    )
    keyboard = [[InlineKeyboardButton("Back", callback_data='more_features')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
