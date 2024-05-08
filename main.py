#!/usr/bin/env python


import psycopg2
import logging
from telegram import __version__ as TG_VER
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
import os
from dotenv import load_dotenv
import pdb
import openai
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key



load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    database=os.getenv("PG_TABLE"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
)

cur = conn.cursor()

EDITOR_CHAT_ID = os.getenv("PG_USER")
TOKEN = os.getenv("TG_TOKEN")


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

async def add(update: Update, _context):
    pdb.set_trace()
    word = update.message.text.split(" ")[-1]
    res = chat_with_gpt(PROMPT.format(word)).strip()
    
    print(f'chat gpt res: {res}')
    cur.execute(f"INSERT INTO synonyms (word, synonyms) VALUES ('{word}','{res}');")
    conn.commit()

    return res 

async def list(update: Update, _context):
    cur = conn.cursor()
    cur.execute("SELECT word  FROM synonyms;")
    rows = cur.fetchall()

    await update.message.reply_text(f'{rows}')


async def show(update: Update, _context, word) : 
    cur = conn.cursor()
    cur.execute(f"SELECT synonyms FROM synonyms WHERE word = '{word}'")
    rows = cur.fetchall()
    await update.message.reply_text(f'{rows}')


async def delete(word ): 
    cur = conn.cursor()
    cur.execute(f"DELETE FROM synonyms WHERE word  = '{word}';")
    conn.commit()



PROMPT =  'верни слова синонимы к слову {} через запятую ,верни только эти слова '


def main() -> None:
    logging.debug("Debugging information")
    
    
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", list))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("show", show))

    application.run_polling()


if __name__ == "__main__":
    main()
