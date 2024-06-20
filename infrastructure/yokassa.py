import yookassa
from yookassa import Payment
import uuid

yookassa.Configuration.account_id = '365116'
yookassa.Configuration.secret_key = 'test_Xs8XG91weUa9QRvnBaeyaJs7LV6ZOWOl7FNTwAkrBoU'


def create_payment(cost):
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": f"{cost}",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/Avraam_aibot"
        },
        "description": "Оплата бота",
        "capture": True
    }, idempotence_key)

    # get confirmation url

    return payment


def check_payment(payment_id):

    payment = Payment.find_one(payment_id)

    if payment.status == 'succeeded':
        return True
    else:
        return False
