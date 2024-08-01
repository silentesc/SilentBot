from bots.bot import Bot
from data.env import Env


if __name__ == "__main__":
    env = Env()
    bot = Bot(env)
    bot.run()
