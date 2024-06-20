import datetime

from infrastructure.database.db_working import UserWorking
from tgbot.keyboards.inline.main_profile.subscribes.subscribes_kb import profile_subscribes


async def check_subs(bot):
    users = await UserWorking.get_all_users_with_subs()
    for user in users:

        if user.date <= datetime.date.today():
            await UserWorking.set_subscribe_false(user.user_id)
            await bot.send_message(text="У вас кончилась подписка❗❗❗\n💸Вы можете приобрести другой тариф:",
                                   reply_markup=profile_subscribes(), chat_id=user.user_id)
