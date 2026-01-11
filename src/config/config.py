from dotenv import load_dotenv
import os

load_dotenv()

def get_req_config(key:str):
    dict_config = {
        "MONGO_URL":os.getenv("MONGO_URL"),
        "SECRET_KEY_API":os.getenv("SECRET_KEY_API"),
        "JWT_SECRET_KEY":os.getenv("JWT_SECRET_KEY"),
        "GROK_API_KEY":os.getenv("GROK_API_KEY"),
        "JWT_ALGORITHM":os.getenv("JWT_ALGORITHM")
    
    }

    return dict_config[key]