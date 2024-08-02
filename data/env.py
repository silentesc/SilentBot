import dotenv
import os


class Env:
    def __init__(self) -> None:
        dotenv.load_dotenv()
    

    def get_token(self) -> str:
        return os.getenv("TOKEN")


    def get_test_guild_id(self) -> str:
        return os.getenv("TEST_GUILD_ID")
