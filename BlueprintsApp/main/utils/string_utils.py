from utils.utils import Utils
from utils import logger_utils


class StringUtils(Utils):

    __LOGGER = logger_utils.get_logger(__name__)

    LANGUAGES = [
        ["ID_ENGLISH", "English"],
        ["ID_RUSSIAN", "Русский"]
    ]

    # TODO load saved language from config file
    DEFAULT_LANGUAGE = LANGUAGES[0][0]

    # LANGUAGE [ID - WORD] DICTIONARY
    ENGLISH_DICT = {
        "ID_ENGLISH": "English",
        "ID_RUSSIAN": "Русский",
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
        "ID_SELECT": "Select",
        "ID_THEME": "Theme",
        "ID_LANGUAGE": "Language",
        "ID_BACK": "Back",
        "ID_APPLY": "Apply",
        "ID_CAR_SIMULATOR": "Car Simulator",
        "ID_DARK_KNIGHT": "Dark Knight",
        "ID_DAY_LIGHT": "Day Light",
        "ID_PRINCESS": "Princess",
        "ID_FILE": "File",
        "ID_RUN": "Run",
        "ID_BUILD": "Build",
        "ID_SETTINGS": "Settings",
        "ID_SAVE": "Save",
        "ID_CONTROL_PANEL": "Control Panel",
        "ID_EDIT": "Edit"
    }

    RUSSIAN_DICT = {
        "ID_NEW_PROJECT": "Новый проект",
        "ID_LOAD_PROJECT": "Загрузить проект",
        "ID_CONFIGURATION": "Конфигурация",
        "ID_EXIT": "Выход",
        "ID_SAVED_PROJECTS": "Сохраненные проекты",
        "ID_SELECT": "Выбрать",
        "ID_DELETE": "Удалить",
        "ID_WELCOME": "Добро пожаловать",
        "ID_TITLE": "Название",
        "ID_GAME_API": "Game API",
        "ID_CANCEL": "Отмена",
        "ID_CREATE": "Создать",
        "ID_SELECT": "Выбрать",
        "ID_THEME": "Тема",
        "ID_LANGUAGE": "Язык",
        "ID_BACK": "Назад",
        "ID_APPLY": "Применить",
        "ID_CAR_SIMULATOR": "Симулятор автомобиля",
        "ID_DARK_KNIGHT": "Темный рыцарь",
        "ID_DAY_LIGHT": "Дневной свет",
        "ID_PRINCESS": "Принцесса"
    }

    @classmethod
    def get_string(cls, word_id):
        if StringUtils.DEFAULT_LANGUAGE == StringUtils.LANGUAGES[0][0]:
            return StringUtils.ENGLISH_DICT.get(word_id)
        elif StringUtils.DEFAULT_LANGUAGE == StringUtils.LANGUAGES[1][0]:
            return StringUtils.RUSSIAN_DICT.get(word_id)

    @classmethod
    def set_language(cls, lang_id):
        for i in range(0, len(StringUtils.LANGUAGES), 1):
            if lang_id == StringUtils.LANGUAGES[i][0]:
                StringUtils.DEFAULT_LANGUAGE = lang_id
        if lang_id != StringUtils.DEFAULT_LANGUAGE:
            StringUtils.__LOGGER.error("Failed to set unknown language: " + lang_id)
