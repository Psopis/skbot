import asyncio
import uuid

from AsyncKandinsky import FusionBrainApi, ApiApi, ApiWeb

from tgbot.config import load_config

config = load_config(".env")
login = config.tg_bot.login_k
password = config.tg_bot.password_k

# Любой способ на выбор
model = FusionBrainApi(ApiWeb(login, password))


async def generate(prompt):
    result = await model.text2video(prompt)
    # Стиль придётся самому вписывать
    url_video = uuid.uuid1()
    if result["error"]:
        print("Error:")
        print(result["data"])
    else:
        with open(f"{url_video}.mp4", "wb") as f:
            f.write(result["data"].getvalue())
        return f"{url_video}.mp4"
