from aiogram.utils.keyboard import InlineKeyboardBuilder


def invite_friend(referral_link, language: ['rus', 'eng'] = None):
    keyboard = InlineKeyboardBuilder()
    if language:
        text = 'Пригласить друга 👥' if language == 'rus' else 'Invite a friend 👥'
    else:
        text = r'Пригласить друга \ Invite👥'
    keyboard.button(text=text, url=f'https://t.me/share/url?url={referral_link}')
    return keyboard.as_markup()