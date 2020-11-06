import os
import asyncio
import secrets
import logging
import configparser
from textwrap import wrap
from pyrogram import Client, idle, filters
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont, ImageChops

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger(__name__)

is_env = bool(os.environ.get("ENV", None))
if is_env:
    tg_app_id = int(os.environ.get("TG_APP_ID"))
    tg_api_key = os.environ.get("TG_API_HASH")
    bot_api_key = os.environ.get("TG_BOT_TOKEN")

    some_sticker_bot = Client(
        api_id=tg_app_id,
        api_hash=tg_api_key,
        session_name=":memory:",
        bot_token=bot_api_key,
        workers=200
    )
else:
    app_config = configparser.ConfigParser()
    app_config.read("config.ini")
    bot_api_key = app_config.get("bot-configuration", "api_key")

    some_sticker_bot = Client(
        session_name="some_sticker_bot",
        bot_token=bot_api_key,
        workers=200
    )


async def get_y_and_heights(text_wrapped, dimensions, margin, font):
    _, descent = font.getmetrics()
    line_heights = [font.getmask(text_line).getbbox()[3] + descent + margin for text_line in text_wrapped]
    line_heights[-1] -= margin
    height_text = sum(line_heights)
    y = (dimensions[1] - height_text) // 2
    return y, line_heights


async def crop_to_circle(im):
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, im.split()[-1])
    im.putalpha(mask)


@some_sticker_bot.on_message(filters.command("start"))
async def start_handler(c: Client, m: Message):
    await m.reply_text(
        "Hi, I just create telegram sticker from the text messages you send me. \nMy creator @eyaadh did a YouTube "
        "[video](https://youtu.be/dVrA9hit4ks) on how he created me. The link for my source is on the video "
        "description, you can fork the project and make a better version of me.",
        disable_web_page_preview=True
    )


@some_sticker_bot.on_message(filters.command("help"))
async def help_handler(c: Client, m: Message):
    await m.reply_text(
        "Hi, I do not have much to say on help - I just create telegram stickers from the text messages you send me. "
        "\nMy creator @eyaadh did a YouTube "
        "[video](https://youtu.be/dVrA9hit4ks) on how he created me. The link for my source is on the video "
        "description, you can fork the project and make a better version of me.",
        disable_web_page_preview=True
    )


@some_sticker_bot.on_message(filters.text & (~filters.command("start") | ~filters.command("help")))
async def create_sticker_handler(c: Client, m: Message):
    s = await m.reply_text("...")

    font = ImageFont.truetype("Segan-Light.ttf", 30)
    font_who = ImageFont.truetype("TitilliumWeb-Bold.ttf", 24)

    img = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    text_lines = wrap(m.text if len(m.text) < 200 else f"{m.text[:200]}...", 25)

    y, line_heights = await get_y_and_heights(
        text_lines,
        (512, 512),
        10,
        font
    )

    draw.rectangle(((0, 00), (img.size[0] - 10, img.size[1] - 10)), fill=(250, 250, 250, 40))

    try:
        user_profile_pic = await c.get_profile_photos(m.from_user.id)
        photo = await c.download_media(user_profile_pic[0].file_id, file_ref=user_profile_pic[0].file_ref)
    except Exception as e:
        photo = "default.jpg"
        logging.error(e)

    im = Image.open(photo).convert("RGBA")
    im.thumbnail((60, 60))
    await crop_to_circle(im)
    img.paste(im, (30, y))

    f_user = m.from_user.first_name + " " + m.from_user.last_name if m.from_user.last_name else m.from_user.first_name

    draw.text((100, y), f"{f_user}:", (0, 0, 0), font=font_who)

    for i, line in enumerate(text_lines):
        x = 100
        y += line_heights[i]
        draw.text((x, y), line, (0, 0, 0), font=font)

    sticker_file = f"{secrets.token_hex(2)}.webp"

    img.save(sticker_file)

    await m.reply_sticker(
        sticker=sticker_file
    )

    try:
        if os.path.isfile(sticker_file):
            os.remove(sticker_file)

        if os.path.isfile(photo) and (photo != "default.jpg"):
            os.remove(photo)
    except Exception as e:
        logging.error(e)

    await s.delete()


async def main():
    await some_sticker_bot.start()
    await idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
