import dotenv
import os


class Env:
    def __init__(self) -> None:
        dotenv.load_dotenv()
    

    def get_token(self) -> str:
        return os.getenv("TOKEN")
