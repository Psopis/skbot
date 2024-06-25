import yookassa
from yookassa import Payment
import uuid

yookassa.Configuration.account_id = '405453'
yookassa.Configuration.secret_key = 'live_gBhm1wf96V8E-Cl0q2KNZqvFTQ7z6isIoUj9tiYTUbo'


# yookassa.Configuration.account_id = '365116'
# yookassa.Configuration.secret_key = 'test_Xs8XG91weUa9QRvnBaeyaJs7LV6ZOWOl7FNTwAkrBoU'
# yookassa.Configuration.configure_auth_token('390540012:LIVE:52542')


def create_payment(cost):
    idempotence_key = str(uuid.uuid4())
    res = Payment.create(
        {
            "amount": {
                "value": cost,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/Avraam_aibot"
            },
            "capture": True,
            "description": "Оплата подписки на бота",

            "receipt": {
                "customer": {
                    "full_name": "Ivanov Ivan Ivanovich",
                    "email": "email@email.ru",
                    "phone": "79211234567",
                    "inn": "6321341814"
                },
                "items": [
                    {
                        "description": "Бот",
                        "quantity": "1.00",
                        "amount": {
                            "value": cost,
                            "currency": "RUB"
                        },
                        "vat_code": "2",
                        "payment_mode": "full_payment",
                        "payment_subject": "commodity",
                        "country_of_origin_code": "CN",
                        "product_code": "44 4D 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00",
                        "customs_declaration_number": "10714040/140917/0090376",
                        "excise": "20.00",
                        "supplier": {
                            "name": "string",
                            "phone": "string",
                            "inn": "string"
                        }
                    },
                ]
            }
        }
    )

    # get confirmation url

    return res


def check_payment(payment_id):
    payment = Payment.find_one(payment_id)

    if payment.status == 'succeeded':
        return True
    else:
        return False
