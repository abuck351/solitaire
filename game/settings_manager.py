import pickle


default_settings = {'draw_three': True}

def save_settings(settings):
    data = settings
    file = open("settings.data", "wb")
    pickle.dump(data, file)
    file.close()


def load_settings():
    try:
        file = open("settings.data", "rb")
    except FileNotFoundError:
        save_settings(default_settings)
        return default_settings
    else:
        settings = pickle.load(file)
        file.close()
        return settings 