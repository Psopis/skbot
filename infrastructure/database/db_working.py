import datetime

import tortoise

from infrastructure.database.models import User


class UserWorking:
    @staticmethod
    async def add_user(user_id, username, referred_by, employee=False):
        try:
            return await User.get(user_id=user_id)
        except tortoise.exceptions.DoesNotExist:
            if referred_by:
                try:
                    referral = await User.get(user_id=referred_by)
                except tortoise.exceptions.DoesNotExist:
                    await User.create(user_id=user_id, username=username, is_employee=employee)
                    return
                await User.create(user_id=user_id, username=username, referred_by=referral, is_employee=employee)

            else:
                await User.create(user_id=user_id, username=username, is_employee=employee)

    @staticmethod
    async def check_user(user_id):
        return await User.get_or_none(user_id=user_id)

    @staticmethod
    async def set_referral_balance(user_id, balance):
        user = await User.get(user_id=user_id)
        user.referral_balance += balance
        user.all_money_reffred += balance
        await user.save()

    @staticmethod
    async def set_subscribe_true(user_id, time):
        user = await User.get(user_id=user_id)
        user.subscribe = True
        user.date = datetime.date.today() + datetime.timedelta(days=time)
        await user.save()

    @staticmethod
    async def set_referred(user_id):
        user = await User.get(user_id=user_id)
        user.referreded = True
        await user.save()

    @staticmethod
    async def set_subscribe_false(user_id):
        user = await User.get(user_id=user_id)
        user.subscribe = False
        await user.save()

    @staticmethod
    async def get_id_from_name(username):

        user = await User.get(username=username)
        return user.user_id

    @staticmethod
    async def get_name_from_id(user_id):

        return await User.get_or_none(user_id=user_id)

    @staticmethod
    async def get_user(user_id):
        user = await User.get(user_id=user_id)
        return user

    @staticmethod
    async def attempt_gpt_minus(user_id):

        user = await User.get(user_id=user_id)
        d = user.free_attempts_gpt

        user.free_attempts_gpt = d - 1
        await user.save()
        return user.free_attempts_gpt

    @staticmethod
    async def plus_one_refferes_user(user_id):
        user = await User.get(user_id=user_id)
        user.users_refered += 1
        await user.save()

    @staticmethod
    async def get_all_users_refereded():
        return await User.filter(referreded=True)

    @staticmethod
    async def get_all_users_with_subs():

        return await User.filter(subscribe=True)


class AdminWorking:
    @staticmethod
    async def get_all_admins():
        return await User.filter(is_employee=True)

    @staticmethod
    async def add_admin(user_id, username, time):
        try:
            return await User.get(user_id=user_id)
        except tortoise.exceptions.DoesNotExist:

            await User.create(user_id=user_id, username=username, is_employee=True, date=time)

    @staticmethod
    async def check_admin(user_id):
        user = await User.get(user_id=user_id)
        return user.role_
