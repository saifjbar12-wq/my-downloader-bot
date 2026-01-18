ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'quiet': True,
    'no_warnings': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'addmetadata': True,
    'no_color': True,
    'source_address': '0.0.0.0', # يساعد في تخطي بعض قيود الشبكة
}
