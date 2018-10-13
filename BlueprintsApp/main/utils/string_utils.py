from utils.utils import Utils


class StringUtils(Utils):

    LANGUAGES = {
        "ID_ENGLISH": "English",
        "ID_RUSSIAN": "Русский"
    }

    DEFAULT_LANGUAGE = LANGUAGES.get("ID_ENGLISH")

    # LANGUAGE [ID - WORD] DICTIONARY
    ENGLISH_DICT = {
        "ID_NEW_PROJECT": "New Project",
        "ID_LOAD_PROJECT": "Load Project",
        "ID_CONFIGURATION": "Configuration",
        "ID_EXIT": "Exit",
        "ID_SAVED_PROJECTS": "Saved Projects",
        "ID_SELECT": "Select",
        "ID_DELETE": "Delete",
        "ID_WELCOME": "Welcome",
        "ID_TITLE": "Title",
        "ID_GAME_API": "Game API",
        "ID_CANCEL": "Cancel",
        "ID_CREATE": "Create",
        "ID_SELECT": "Select"
    }

    @staticmethod
    def get_string(word_id):
        if StringUtils.DEFAULT_LANGUAGE == StringUtils.LANGUAGES.get("ID_ENGLISH"):
            return StringUtils.ENGLISH_DICT.get(word_id)
