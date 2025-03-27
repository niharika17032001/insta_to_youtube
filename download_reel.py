import yt_dlp


def download_instagram_reel(url, output_path="downloads/%(title)s.%(ext)s"):
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# Example usage:
download_instagram_reel("https://www.instagram.com/reel/CCtAS_CJjZV/")
