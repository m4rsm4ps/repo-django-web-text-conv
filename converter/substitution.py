from functools import wraps


def substitute(func):
    """Performs substitution of ambiguous characters based on rules provided by methods of certain class which defines
    those rules though methods. This functions is used as a decorator for those methods."""
    @wraps(func)
    def inner(*args):
        args = list(args)
        while args[1] in args[2]:
            option = func(*args)
            args[2] = args[2].replace(args[1], args[0].AMBIGUOUS_CHAR_TAB[func.__name__][args[1]][option], 1)
        return args[2]
    return inner


class LatynkaMapsa:
    """Defines the rules for character substitution.
    An instance of this class is passed as an argument for 'Romaniser(..rules=LatynkaMapsa()..)' object."""

    # This table is used for substitution of all unambiguous characters;
    # it's being passed as argument for str.translate() method, which is applied to the whole text to be converted.
    UNAMBIGUOUS_CHAR_TAB = 'АБГҐДЕЗИІКЛМНОПРСТУФЦабгґдезиіклмнопрстуфхцщ'.maketrans({
        'А': 'A', 'Б': 'B', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'З': 'Z', 'И': 'Y', 'І': 'I', 'К': 'K', 'Л': 'L',
        'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Ц': 'C', 'а': 'a',
        'б': 'b', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'з': 'z', 'и': 'y', 'і': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'ch', 'ц': 'c', 'щ': 'shj'
    })

    # This dict contains ambiguous chars and combinations of them, grouped in nested dicts by their type of ambiguity.
    # Each key for each nested dict is a sring and is equal to __name__ property of corresponding method defined further
    # below.
    # The '_resolve_ambiguity()' method of 'Romanizer' class loops throug 'amb_char_tab' and performs nested for loops
    # throug each of nested dicts.
    # If a key of a nested dict is found in the string, upon which '_resolve_ambiguity()' was called, a corresponding
    # method of 'LatinkaMapsa' class is called passing it the key of a nested dict as an argument.
    AMBIGUOUS_CHAR_TAB = {
        '_doubles': {'ьо': ('io',),
                     'ЬО': ('IO',),
                     'ьк': ('q',),
                     'ЬК': ('Q',),
                     'вв': ('wv',),  # This group is placed firs because words may contain single characters of the same
                     'чч': ('jj',),  # kind, and having them replaced first will eliminate doubled variants.
                     'жж': ('zhh',),
                     'шш': ('shh',),
                     'шг': ('shgh',),
                     'дж': ('dj',),
                     'ДЖ': ('DJ',),
                     'Дж': ('Dj',),
                     'дч': ('dtj',),
                     'ДЧ': ('DTJ',),
                     'Вв': ('Wv',),
                     'ВВ': ('WV',),
                     'ЧЧ': ('JJ',),
                     'ЖЖ': ('ZHH',),
                     'ШШ': ('SHH',),
                     'ШГ': ('SHGH',)},

        '_sibilants': {'ж': ('zh',),
                       'ч': ('j',),
                       'ш': ('sh',),
                       'Ж': ('Zh', 'ZH'),
                       'Ч': ('J', 'J'),
                       'Ш': ('Sh', 'SH'),
                       'Щ': ('Shj', 'SHJ'),
                       'Х': ('Ch', 'CH')},

        '_v_or_w': {'в': ('v', 'w'),
                    'В': ('V', 'W')},

        '_vowels_small': {'я': ('ia', 'ya'),
                          'ї': ('iy', 'yi'),
                          'є': ('ie', 'ye'),
                          'ю': ('iu', 'yu')},

        '_vowels_capital': {'Я': ('IA', 'Ya', 'YA'),
                            'Є': ('IE', 'Ye', 'YE'),
                            'Ю': ('IU', 'Yu', 'YU'),
                            'Ї': ('IY', 'Yi', 'YI')},

        '_y_or_i': {'й': ('y', 'i', "'y"),  # This one should follow '_vowels_small' and '_vowels_capital'
                    'Й': ('Y', 'I', "'Y")},

        '_softener': {'ь': ('',),
                      'Ь': ('',)}
    }

    # These methods below define the character substitution rules for certain types of ambiguity:

    @substitute
    def _doubles(self, *args):
        """Replaces certain doubled consonants"""
        return 0

    @substitute
    def _sibilants(self, *args):
        option = 1 if args[1].isupper() else 0
        return option

    @substitute
    def _v_or_w(self, char, word):
        nxt = word.index(char) + 1
        if word.endswith(char) or word[nxt] not in 'aeyoiuєяAEYOIUЄЯ':
            option = 1
        else:
            option = 0
        return option

    @substitute
    def _vowels_small(self, char, word):
        position = word.index(char)
        if position != 0 and word[position - 1] not in "'ь":
            option = 0
        else:
            option = 1
        return option

    @substitute
    def _vowels_capital(self, char, word):
        word = ''.join([smb if smb.isalpha() else '' for smb in word])
        position = word.index(char)
        if position != 0 and word[position - 1] not in "'Ь":
            option = 0
        elif (word.index(char) == 0 and len(word) == 1) or not word.isupper():
            option = 1
        else:
            option = 2
        return option

    @substitute
    def _y_or_i(self, char, word):
        prvs, position = word.index(char) - 1, word.index(char)
        if position == 0 or word[prvs] == '\n':
            option = 0
        elif word[prvs] in 'aeiouyAEIOUY':
            option = 1
        else:
            option = 2
        return option

    @substitute
    def _softener(self, *args):
        return 0
