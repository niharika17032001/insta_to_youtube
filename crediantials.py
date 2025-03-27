from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("USER")
PWD = os.getenv("YOUTUBE_PWD")


if not PWD:
    raise ValueError("PWD key is missing. Ensure it is set in GitHub Secrets.")

if not USER:
    raise ValueError("USER key is missing. Ensure it is set in GitHub Secrets.")
