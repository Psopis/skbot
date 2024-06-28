from PIL import Image
from gradio_client import Client, handle_file


def img_to_vid_generate(photo_path):
    image = Image.open(photo_path)

    width, height = image.size
    w, h = 0, 0
    if height >= 1000 or width >= 1000:
        hei = int(height / 100 * 80)
        wid = int(width / 100 * 80)
    while True:
        if wid % 64 == 0:
            w = wid
            break
        wid -= 1
    while True:
        if hei % 64 == 0:
            h = hei
            break
        hei -= 1
    client = Client("doevent/AnimateLCM-SVD")
    result = client.predict(
        handle_file(photo_path),
        0,
        True,
        1,
        5,
        1,
        1,
        w,
        h,
        1,
        api_name="/video"
    )
    print(result[0]['video'])
    return result[0]['video']