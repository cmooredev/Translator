import discord
from discord.ext import commands
from lingua import Language

basic_languages = {
    'french':'FR',
    'english':'EN-US',
    'spanish':'ES',
    'bulgarian': 'BG',
    'czech': 'CZ',
    'danish': 'DA',
    'german': 'DE',
    'greek': 'EL',
    'estonian': 'ET',
    'finnish': 'FT',
    'hungarian': 'HU',
    'italian': 'IT',
    'japanese': 'JA',
    'lithuanian': 'LT',
    'latvian': 'LV',
    'dutch': 'NL',
    'polish': 'PL',
    'portuguese': 'PT-PT',
    'romanian': 'RO',
    'russian': 'RU',
    'slovak': 'SK',
    'slovenian': 'SL',
    'turkish': 'TR',
    'swedish': 'SV',
    'chinese': 'ZH',
    'indonesian': 'IN',
}

full_languages = basic_languages + {
    'test' : 'lang'

    }


lingua_languages = [Language.ARABIC, Language.ENGLISH, Language.FRENCH, Language.GERMAN,
                    Language.CHINESE, Language.DUTCH, Language.HINDI, Language.SPANISH,
                    Language.ITALIAN, Language.JAPANESE, Language.POLISH, Language.RUSSIAN,
                    Language.TURKISH, Language.INDONESIAN, Language.BELARUSIAN, Language.CZECH,
                    Language.ESTONIAN, Language.GERMAN, Language.HEBREW, Language.KOREAN,
                    Language.LATVIAN, Language.MONGOLIAN, Language.PORTUGUESE, Language.SLOVAK,
                    Language.SWAHILI, Language.TAGALOG, Language.THAI, Language.VIETNAMESE,
                    Language.UKRAINIAN]


class Languages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Languages loaded')


async def setup(client):
    await client.add_cog(Languages(client))
