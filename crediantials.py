from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("USER")
PWD = os.getenv("YOUTUBE_PWD")

file_path = os.path.abspath(__file__)
current_Folder_Path = os.path.dirname(file_path)
root_folder = os.path.dirname(current_Folder_Path)

print(f"Current Folder Path: {current_Folder_Path}")
print(f"Root Folder Path: {root_folder}")
screenshot_path = current_Folder_Path + '/reports/screenshot.png'
page_content_path = current_Folder_Path + '/reports/page_content.html'
video_path = current_Folder_Path + '/reports'

if not PWD:
    raise ValueError("PWD key is missing. Ensure it is set in GitHub Secrets.")

if not USER:
    raise ValueError("USER key is missing. Ensure it is set in GitHub Secrets.")
