import requests
from instagrapi import Client
from loader import bot
import aiofiles
import os
import aiohttp
from aiogram import types
from io import BytesIO
# Create a client instance
async def upload_instagram(file_id,content_type,photo,caption):
    if content_type== 'photo':
        photo = photo
        file_id = file_id
        photo_file = await bot.download_file_by_id(file_id) 
        with open(f"{file_id}.jpg", 'wb') as photo_file_local:
            photo_file_local.write(photo_file.read())
    cl = Client()

    caption = caption
    caption += "#SelimbeyServis #AvtoServisSelimbey #SelimbeyAvtoSavdo #SelimbeyCarDetailing #SelimbeyAvtoTexnika #SelimbeyAvtoTozalash #SelimbeyLuxuryCars #SelimbeyAvtoMijozlik #SelimbeyAvtoBiznes #SelimbeyAvtoTarz\n"
    username = "bytefycompany"
    password = "youcan'thackthispassword"
    cl.login(username, password)

    media = cl.photo_upload(path=f"{file_id}.jpg",caption=caption)
    os.system(f'rm -rf {file_id}.jpg')
    # Upload the downloaded image
#     media = cl.video_upload(path="/home/amirjon/Documents/123.mp4", caption="#hashtag #using #python")


# photo to link function section

async def photo_link(photo: types.photo_size.PhotoSize) -> str:
    with await photo.download(BytesIO()) as file:
        form = aiohttp.FormData()
        form.add_field(
            name='file',
            value=file,
        )
        async with bot.session.post('https://telegra.ph/upload', data=form) as response:
            img_src = await response.json()

    link = 'http://telegra.ph/' + img_src[0]["src"]
    return link