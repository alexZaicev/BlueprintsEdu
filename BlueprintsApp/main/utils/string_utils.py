from utils.utils import Utils
from utils import logger_utils
from utils.languages.english import EnglishLanguage
from utils.languages.russian import RussianLanguage
from utils.languages.german import GermanLanguage
from utils.languages.french import FrenchLanguage
from utils.languages.spanish import SpanishLanguage
from utils.languages.norwegian import NorwegianLanguage


class StringUtils(Utils):

    __LOGGER = logger_utils.get_logger(__name__)

    LANGUAGES = [
        ["ID_ENGLISH", "English"],
        ["ID_RUSSIAN", "Русский"],
        ["ID_SPANISH", "Español"],
        ["ID_FRENCH", "Français"],
        ["ID_GERMAN", "Deutsche"],
        ["ID_NORWEGIAN", "Norsk"]
    ]

    DEFAULT_LANGUAGE = LANGUAGES[0][0]

    @classmethod
    def get_string(cls, word_id):
        if StringUtils.DEFAULT_LANGUAGE == StringUtils.LANGUAGES[0][0]:
            return EnglishLanguage.WORD_TRANSLATIONS.get(word_id)
        elif StringUtils.DEFAULT_LANGUAGE == StringUtils.LANGUAGES[1][0]:
            return RussianLanguage.WORD_TRANSLATIONS.get(word_id)
        elif StringUtils.DEFAULT_LANGUAGE == StringUtils.LANGUAGES[2][0]:
            return SpanishLanguage.WORD_TRANSLATIONS.get(word_id)
        elif StringUtils.DEFAULT_LANGUAGE == StringUtils.LANGUAGES[3][0]:
            return FrenchLanguage.WORD_TRANSLATIONS.get(word_id)
        elif StringUtils.DEFAULT_LANGUAGE == StringUtils.LANGUAGES[4][0]:
            return GermanLanguage.WORD_TRANSLATIONS.get(word_id)
        elif StringUtils.DEFAULT_LANGUAGE == StringUtils.LANGUAGES[5][0]:
            return NorwegianLanguage.WORD_TRANSLATIONS.get(word_id)

    @classmethod
    def set_language(cls, lang_id):
        for i in range(0, len(StringUtils.LANGUAGES), 1):
            if lang_id == StringUtils.LANGUAGES[i][0]:
                StringUtils.DEFAULT_LANGUAGE = lang_id
        if lang_id != StringUtils.DEFAULT_LANGUAGE:
            StringUtils.__LOGGER.error("Failed to set unknown language: " + lang_id)
