from utils import database_manager


async def check_create_tables():
    db = database_manager.SQLiteManager()
    await db.connect()

    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS button_roles (
            id INTEGER PRIMARY KEY NOT NULL,
            label TEXT NOT NULL,
            style INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            guild_id INTEGER NOT NULL
        )
        """
    )

    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS leveling (
            id INTEGER PRIMARY KEY NOT NULL,
            guild_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            xp INTEGER NOT NULL,
            level INTEGER NOT NULL
        )
        """
    )

    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY NOT NULL,
            guild_id INTEGER NOT NULL,
            leveling_enabled INTEGER NOT NULL,
            xp_per_message INTEGER NOT NULL,
            level_up_message_enabled INTEGER NOT NULL,
            level_up_message TEXT NOT NULL,
            level_up_message_channel_id INTEGER NOT NULL
        )
        """
    )

    await db.commit()
    await db.disconnect()


async def check_create_settings(guild_id: int):
    db = database_manager.SQLiteManager()
    await db.connect()

    rows = await db.execute_one("SELECT * FROM settings WHERE guild_id = ?", guild_id)

    if not rows:
        await db.execute(
            """
            INSERT INTO settings (guild_id, leveling_enabled, xp_per_message, level_up_message_enabled, level_up_message, level_up_message_channel_id)
            VALUES (?, 1, 3, 1, "Congratulations {member_mention}! You have leveled up to level {level}!", -1)
            """,
            guild_id
        )

    await db.commit()
    await db.disconnect()
