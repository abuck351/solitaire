import pickle
import os


default_settings = {'draw_three': False}

def save_settings(settings):
    data = settings

    file_path = os.path.join("game_data", "settings.data")
    file = open(file_path, "wb")

    pickle.dump(data, file)
    file.close()


def load_settings():
    try:
        file_path = os.path.join("game_data", "settings.data")
        file = open(file_path, "rb")
    except FileNotFoundError:
        save_settings(default_settings)
        return default_settings
    else:
        settings = pickle.load(file)
        file.close()
        return settings 