from tortoise import Model, fields


class User(Model):
    user_id = fields.TextField(primary_key=True)
    username = fields.TextField()
    date = fields.DateField(null=True)
    referred_by = fields.ForeignKeyField('models.User', null=True)
    referral_balance = fields.FloatField(default=0)
    free_attempts_gpt = fields.IntField(default=5)
    subscribe = fields.BooleanField(default=False)
    is_employee = fields.BooleanField(default=False)
    referreded = fields.BooleanField(default=False)
    users_refered = fields.IntField(default=0)
    all_money_reffred = fields.IntField(default=0)

    def __str__(self):
        return self.username, self.user_id
