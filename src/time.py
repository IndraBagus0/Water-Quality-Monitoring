from datetime import datetime

def get_current_time():
    """
    Fungsi ini mengembalikan waktu saat ini dalam format HH:MM:SS
    """
    now = datetime.now()
    time_str = now.strftime("%y-%m-%d %H:%M:%S")
    return time_str