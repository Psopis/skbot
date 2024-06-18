from tortoise import Model, fields


class User(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.TextField()
    username = fields.TextField()
    role_ = fields.TextField()
    date = fields.DateField()
    your_promo = fields.TextField()
    activated_promo = fields.TextField()
    free_attempts_gpt = fields.IntField(default=5)
    subscribe = fields.BooleanField(default=False)
    is_employee = fields.BooleanField(default=False)

    def __str__(self):
        return self.username, self.user_id
