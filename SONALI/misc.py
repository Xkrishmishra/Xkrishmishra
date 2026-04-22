import asyncio
import socket
import time

import heroku3
from pyrogram import filters

import config
from SONALI.core.mongo import mongodb

from .logging import LOGGER

SUDOERS = filters.user()

HAPP = None
_boot_ = time.time()


def is_heroku():
    return "heroku" in socket.getfqdn()

XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(config.HEROKU_API_KEY),
    "https",
    str(config.HEROKU_APP_NAME),
    "HEAD",
    "master",
]

def dbb():
    global db
    db = {}
    LOGGER(__name__).info(f"𝗗𝗔𝗧𝗔𝗕𝗔𝗦𝗘 𝗟𝗢𝗔𝗗 𝗕𝗔𝗕𝗬🍫........")

async def init_database():
    """Initialize MongoDB connection with pooling"""
    global db
    try:
        if config.MONGO_DB_URI:
            db = mongodb
            # Test connection
            await db.command("ping")
            LOGGER(__name__).info("𝗠𝗢𝗡𝗚𝗢𝗗𝗕 𝗖𝗢𝗡𝗡𝗘𝗖𝗧𝗘𝗗✨")
    except Exception as e:
        LOGGER(__name__).error(f"Database initialization failed: {e}")

async def sudo():
    global SUDOERS
    SUDOERS.add(config.OWNER_ID)
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    if config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)
    LOGGER(__name__).info(f"𝗦𝗨𝗗𝗢 𝗨𝗦𝗘𝗥 𝗗𝗢𝗡𝗘✨🎋.")


def heroku():
    global HAPP
    if is_heroku():  # FIXED: Added function call parentheses
        if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = Heroku.app(config.HEROKU_APP_NAME)
                LOGGER(__name__).info(f"🍟𝗛𝗘𝗥𝗢𝗞𝗨 𝗔𝗣𝗣 𝗡𝗔𝗠𝗘 𝗟𝗢𝗔𝗗......💦..")
            except BaseException:
                LOGGER(__name__).warning(
                    f"🏓𝐘𝐨𝐮 𝐇𝐚𝐯𝐞 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝 𝐇𝐞𝐫𝐨𝐤𝐮 𝐀𝐩𝐢 𝐊𝐞𝐲 𝐀𝐧𝐝 𝐇𝐞𝐫𝐨𝐤𝐮 𝐀𝐩𝐩 𝐍𝐚𝐦𝐞"
                )
