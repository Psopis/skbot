from gradio_client import Client, handle_file


def img_to_vid_generate(photo):
    client = Client("doevent/AnimateLCM-SVD")
    result = client.predict(
        handle_file(photo),
        0,
        True,
        1,
        5,
        1,
        1,
        576,
        320,
        1,
        api_name="/video"
    )
    print(result[0]['video'])
    return result[0]['video']
