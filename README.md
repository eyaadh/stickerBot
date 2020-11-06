# StickerBot:
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/30fb5f54df1f4e96b11f795d286a0cf3)](https://www.codacy.com/gh/eyaadh/stickerBot/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eyaadh/stickerBot&amp;utm_campaign=Badge_Grade)

You send it a text, it will return you the content as a telegram sticker. A working example for the bot can be found [here.](https://telegram.dog/somestickerbot)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Cloning and Run:
1. `git clone https://github.com/eyaadh/stickerBot.git`, to clone the repository.
2. `cd stickerBot`, to enter the directory.
3. `pip3 install -r requirements.txt`, to install rest of the dependencies/requirements.
4. Create a new `config.ini` using the sample available at `config.ini.sample`.
5. Run with `python3.8 main.py`, stop with <kbd>CTRL</kbd>+<kbd>C</kbd>.
> It is recommended to use [virtual environments](https://docs.python-guide.org/dev/virtualenvs/) while running the app, this is a good practice you can use at any of your python projects as virtualenv creates an isolated Python environment which is specific to your project.
