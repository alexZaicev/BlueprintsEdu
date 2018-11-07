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
        "ID_EDIT": "Edit",
        "ID_ADD_ATTRIBUTE": "Add Attribute",
        "ID_NAME": "Name",
        "ID_TYPE": "Type",
        "ID_ATTRIBUTE": "Attribute",
        "ID_CHARACTER": "Character",
        "ID_SPRITE": "Sprite",
        "ID_FUNCTION": "Function",
        "ID_ADD_CHARACTER": "Add Character",
        "ID_ADD_FUNCTION": "Add Function",
        "ID_ADD_SPRITE": "Add Sprite",
        "ID_NONE": "None",
        "ID_INTEGER": "Integer",
        "ID_STRING": "String",
        "ID_FLOAT": "Float",
        "ID_DATA_TYPE": "Data Type",
        "ID_VALUE": "Value",
        "ID_UNKNOWN": "Unknown",
        "ID_SAVE_AND_EXIT": "Save and Exit"
    }

    RUSSIAN_DICT = {
        "ID_ENGLISH": "Английский",
        "ID_RUSSIAN": "Русский",
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
        "ID_THEME": "Тема",
        "ID_LANGUAGE": "Язык",
        "ID_BACK": "Назад",
        "ID_APPLY": "Применить",
        "ID_CAR_SIMULATOR": "Симулятор автомобиля",
        "ID_DARK_KNIGHT": "Темный рыцарь",
        "ID_DAY_LIGHT": "Дневной свет",
        "ID_PRINCESS": "Принцесса",
        "ID_FILE": "Файл",
        "ID_RUN": "Запустить",
        "ID_BUILD": "Build",
        "ID_SETTINGS": "Настройки",
        "ID_SAVE": "Сохранить",
        "ID_CONTROL_PANEL": "Панель управления",
        "ID_EDIT": "Изменить"
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
