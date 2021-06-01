import random
import string

from requests import get
from PIL import Image
from io import BytesIO
from base64 import b64encode

from bot_app import bot


def random_string(n):
    res = ''.join(random.choices(string.digits + string.ascii_letters, k=n))
    return res


def thumbnail_from_id(user_id):
    photo_list = bot.get_user_profile_photos(user_id).photos
    if len(photo_list) != 0:
        url = bot.get_file_url(photo_list[0][2].file_id)
        img = Image.open(get(url=url, stream=True).raw)
        bio = BytesIO()
        img.thumbnail((64, 64))
        img.save(bio, format='JPEG')
        res = b64encode(bio.getvalue())
        return str(res, encoding='utf-8')
    else:
        return None
