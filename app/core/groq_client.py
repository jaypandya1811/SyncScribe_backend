import os
from groq import Groq
from dotenv import load_dotenv
from typing import cast

load_dotenv()

url = cast(str, os.getenv("GROQ_API_KEY"))

groq_client = Groq(api_key=os.environ.get(url))