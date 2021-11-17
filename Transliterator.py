import codecs, sys, os, math


class Syllable:
    def __init__(self, c1, c2, c3):
        self.leading_consonant = c1
        self.vowel = c2
        self.batchim = c3


class Complex:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    @staticmethod
    def is_complex(consonant):
        return consonant in ["ㄳ", "ㄵ", "ㄶ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅄ"]

    @staticmethod
    def merge_characters(characters):
        if characters == "ㄱㅅ":
            return "ㄳ"
        elif characters == "ㄴㅈ":
            return "ㄵ"
        elif characters == "ㄴㅎ":
            return "ㄶ"
        elif characters == "ㄹㄱ":
            return "ㄺ"
        elif characters == "ㄹㅁ":
            return "ㄻ"
        elif characters == "ㄹㅂ":
            return "ㄼ"
        elif characters == "ㄹㅅ":
            return "ㄽ"
        elif characters == "ㄹㅌ:":
            return "ㄾ"
        elif characters == "ㄹㅍ":
            return "ㄿ"
        elif characters == "ㄹㅎ":
            return "ㅀ"
        elif characters == "ㅂㅅ":
            return "ㅄ"
        else:
            raise ValueError

    @staticmethod
    def separate_characters(character):
        if character == "ㄳ":
            return Complex("ㄱ", "ㅅ")
        elif character == "ㄵ":
            return Complex("ㄴ", "ㅈ")
        elif character == "ㄶ":
            return Complex("ㄴ", "ㅎ")
        elif character == "ㄺ":
            return Complex("ㄹ", "ㄱ")
        elif character == "ㄻ":
            return Complex("ㄹ", "ㅁ")
        elif character == "ㄼ":
            return Complex("ㄹ", "ㅂ")
        elif character == "ㄽ":
            return Complex("ㄹ", "ㅅ")
        elif character == "ㄾ":
            return Complex("ㄹ", "ㅌ")
        elif character == "ㄿ":
            return Complex("ㄹ", "ㅍ")
        elif character == "ㅀ":
            return Complex("ㄹ", "ㅎ")
        elif character == "ㅄ":
            return Complex("ㅂ", "ㅅ")
        else:
            raise ValueError


# Everything is purposefully redundant in this class
# To help the developer understand the rules properly
# Once the rules have been aggregated the program will be compressed
class Hangul:
    def __init__(self):
        pass

    JLT = "ㄱ,ㄲ,ㄴ,ㄷ,ㄸ,ㄹ,ㅁ,ㅂ,ㅃ,ㅅ,ㅆ,ㅇ,ㅈ,ㅉ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ".split(",")
    JTT = ",ㄱ,ㄲ,ㄱㅅ,ㄴ,ㄴㅈ,ㄴㅎ,ㄷ,ㄹ,ㄹㄱ,ㄹㅁ,ㄹㅂ,ㄹㅅ,ㄹㅌ,ㄹㅍ,ㄹㅎ,ㅁ,ㅂ,ㅂㅅ,ㅅ,ㅆ,ㅇ,ㅈ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ".split(",")
    JVT = "ㅏ,ㅐ,ㅑ,ㅒ,ㅓ,ㅔ,ㅕ,ㅖ,ㅗ,ㅘ,ㅙ,ㅚ,ㅛ,ㅜ,ㅝ,ㅞ,ㅟ,ㅠ,ㅡ,ㅢ,ㅣ".split(",")
    # Start of Hangul syllables in Unicode
    SBase = 0xAC00
    # Number of active Hangul syllables in Unicode
    SCount = 11172
    TCount = 28
    # 11172 / 588 = 19 which is equal to the number of leading consonant jamos
    NCount = 588

    """
    Hangul syllables consists of 2 to 3 characters (because of diphthongs sometimes 4).
    There are all together 11.732 Hangul syllables registered in unicode but all of
    these characters can be broken down to 2 or 3 characters.
    Original version of this function:
    https://stackoverflow.com/a/12765973/7257264
    The three parts of the syllables is as follows:
    - Leading consonant jamo
    - Vowel jamo
    - Trailing consonant jamo
    The calculations inside the function can be explained by taking a look at the Hangul syllables in Unicode:
    https://en.wikipedia.org/wiki/Hangul_Syllables
    The table is very logical, it goes through all the leading consonant jamos,
    the vowel jamos and the trailing consonant jamos in alphabetical order.
    The program may also be rewritten in a way to create a map to all possible hangul syllables
    and use that.
    """

    def syllables_to_characters(self, text):
        letters = ''
        for s in text:
            code_point = ord(s)
            SIndex = code_point - self.SBase
            # If the syllable is in the Hangul range of Unicode
            if 0 <= SIndex < self.SCount:
                LIndex = SIndex // self.NCount
                VIndex = (SIndex % self.NCount) // self.TCount
                TIndex = int(SIndex % self.TCount)
                letters = letters + (self.JLT[LIndex] + self.JVT[VIndex] + self.JTT[TIndex]).lower()
            else:
                letters += s
        return letters

    @staticmethod
    def default_consonant(consonant):
        # Simple consonants
        if consonant == "ㄱ":
            return "g"
        elif consonant == "ㄴ":
            return "n"
        elif consonant == "ㄷ":
            return "d"
        elif consonant == "ㄹ":
            return "r"
        elif consonant == "ㅁ":
            return "m"
        elif consonant == "ㅂ":
            return "b"
        elif consonant == "ㅅ":
            return "sz"
        elif consonant == "ㅇ":
            return "ng"
        elif consonant == "ㅈ":
            return "dzs"
        elif consonant == "ㅊ":
            return "cs"
        elif consonant == "ㅋ":
            return "k"
        elif consonant == "ㅌ":
            return "t"
        elif consonant == "ㅍ":
            return "p"
        elif consonant == "ㅎ":
            return "h"
        # Tense consonants
        elif consonant == "ㄲ":
            return "gg"
        elif consonant == "ㄸ":
            return "dd"
        elif consonant == "ㅃ":
            return "bb"
        elif consonant == "ㅆ":
            return "ssz"
        elif consonant == "ㅉ":
            return "ddzs"
        # Complex consonants
        elif consonant == "ㄳ":
            return "g"
        elif consonant == "ㄵ":
            return "ndzs"
        elif consonant == "ㄶ":
            return "nh"
        elif consonant == "ㄺ":
            return "g"
        elif consonant == "ㄻ":
            return "m"
        elif consonant == "ㄼ":
            return "b"
        elif consonant == "ㄽ":
            return "s"
        elif consonant == "ㄾ":
            return "t"
        elif consonant == "ㄿ":
            return "p"
        elif consonant == "ㅀ":
            return "h"
        elif consonant == "ㅄ":
            return "p"
        else:
            raise ValueError

    # Part 4 Section 8 Korean Prules rule is unclear
    @staticmethod
    def syllable_final_consonants(current_batchim, next_syllable: Syllable):
        if current_batchim == "ㄱ":
            if next_syllable.leading_consonant == "ㅎ":
                return ""
            elif next_syllable.leading_consonant in ["ㄴ", "ㅁ"]:
                return "ng"
            else:
                return "g"
        elif current_batchim == "ㄷ":
            if next_syllable.leading_consonant == "ㅎ":
                return ""
            elif next_syllable.leading_consonant == "ㅇ" and next_syllable.vowel == "ㅣ":
                return "dzs"
            else:
                return "d"
        elif current_batchim == "ㅂ":
            if next_syllable.leading_consonant == "ㅎ":
                return ""
            elif next_syllable.leading_consonant in ["ㄴ", "ㅁ"]:
                return "m"
            else:
                return "b"
        elif current_batchim == "ㅅ":
            if next_syllable.leading_consonant in ["ㅅ", "ㅈ", "ㅊ", "ㅌ"]:
                return ""
            elif next_syllable.leading_consonant in ["ㄴ", "ㅁ"]:
                return "n"
            else:
                return "s"
        # TODO: continue from ㅇ according to alphabetical order
        # Other cases such as:
        # ㄴ, ㄹ, ㅁ
        return Hangul.default_consonant(current_batchim)

    @staticmethod
    def syllable_initial_consonants(previous_batchim, current_initial):
        # Simple consonants
        if current_initial == "ㄱ":
            if previous_batchim == "ㄺ":
                return "r"
            elif previous_batchim == "ㅎ":
                return "k"
        elif current_initial == "ㄴ":
            if previous_batchim == "ㅎ":
                return "n"
            elif previous_batchim == "ㄶ":
                return "n"
            elif previous_batchim == "ㅀ":
                return "r"
            elif previous_batchim == "ㄹ":
                return "r"
        elif current_initial == "ㄷ":
            if previous_batchim in ["ㅎ", "ㄶ", "ㅀ"]:
                return "t"
        elif current_initial == "ㄹ":
            if previous_batchim in ["ㅁ", "ㅇ", "ㄱ", "ㅂ"]:
                return "n"
            elif previous_batchim == "ㄴ":
                return "r"
        elif current_initial == "ㅅ":
            if previous_batchim in ["ㅎ", "ㄶ", "ㅀ"]:
                return "ssz"
        elif current_initial == "ㅇ":
            # If the previous character was complex we take the default pronunciation of the second letter from that.
            if Complex.is_complex(previous_batchim):
                return Hangul.default_consonant(Complex.separate_characters(previous_batchim).second)
            else:
                return ""
        elif current_initial == "ㅈ":
            if previous_batchim in ["ㅎ", "ㄶ", "ㅀ"]:
                return "cs"
        elif current_initial == "ㅎ":
            if previous_batchim in ["ㄱ", "ㄺ"]:
                return "k"
            elif previous_batchim in ["ㄷ", "ㅌ", "ㅅ"]:
                return "t"
            elif previous_batchim in ["ㅂ", "ㄼ"]:
                return "p"
            elif previous_batchim in ["ㅈ", "ㄵ"]:
                return "dzs"
            elif previous_batchim == "ㅊ":
                return "cs"
        # Tense consonants
        elif current_initial == "ㄲ":
            return "k"
        elif current_initial == "ㅆ":
            return "d"

        # Other cases such as:
        # ㅁ, ㅂ, ㅊ, ㅋ, ㅌ, ㅍ
        # ㄸ, ㅃ, ㅉ
        return Hangul.default_consonant(current_initial)

    @staticmethod
    def word_final_consonants(consonant):
        if consonant == "ㄱ":
            return "k"
        elif consonant == "ㄴ":
            return "n"
        elif consonant == "ㄷ":
            return "t"
        elif consonant == "ㄹ":
            return "r"
        elif consonant == "ㅁ":
            return "m"
        elif consonant == "ㅂ":
            return "p"
        elif consonant == "ㅅ":
            return "g"
        elif consonant == "ㅇ":
            return "ng"
        elif consonant == "ㅈ":
            return "g"
        elif consonant == "ㅊ":
            return "d"
        elif consonant == "ㅋ":
            return "g"
        elif consonant == "ㅌ":
            return "d"
        elif consonant == "ㅍ":
            return "b"
        elif consonant == "ㅎ":
            return ""
        # Tense consonants
        elif consonant == "ㄲ":
            return "kk"
        elif consonant == "ㄸ":
            return ""
        elif consonant == "ㅃ":
            return ""
        elif consonant == "ㅆ":
            return "t"
        elif consonant == "ㅉ":
            return ""
        # Complex consonants
        elif consonant == "ㄳ":
            return "k"
        elif consonant == "ㄵ":
            return "n"
        elif consonant == "ㄶ":
            return "n"
        elif consonant == "ㄺ":
            return "k"
        elif consonant == "ㄻ":
            return "m"
        elif consonant == "ㄼ":
            return "r"
        elif consonant == "ㄽ":
            return "r"
        elif consonant == "ㄾ":
            return "r"
        elif consonant == "ㄿ":
            return "p"
        elif consonant == "ㅀ":
            return "r"
        elif consonant == "ㅄ":
            return "p"
        raise ValueError

    @staticmethod
    def word_initial_consonants(consonant):
        if consonant == "ㄱ":
            return "k"
        elif consonant == "ㄴ":
            return "n"
        elif consonant == "ㄷ":
            return "t"
        elif consonant == "ㄹ":
            return "r"
        elif consonant == "ㅁ":
            return "m"
        elif consonant == "ㅂ":
            return "p"
        elif consonant == "ㅅ":
            return "sz"
        elif consonant == "ㅇ":
            return ""
        elif consonant == "ㅈ":
            return "dzs"
        elif consonant == "ㅊ":
            return "cs"
        elif consonant == "ㅋ":
            return "k"
        elif consonant == "ㅌ":
            return "t"
        elif consonant == "ㅍ":
            return "p"
        elif consonant == "ㅎ":
            return "h"
        # Tense consonants
        elif consonant == "ㄲ":
            return "kk"
        elif consonant == "ㄸ":
            return "tt"
        elif consonant == "ㅃ":
            return "pp"
        elif consonant == "ㅆ":
            return "ss"
        elif consonant == "ㅉ":
            return "ddzs"
        raise ValueError

    @staticmethod
    def transliterate_vowel(vowel):
        # Normal vowels
        if vowel == "ㅏ":
            return "á"
        elif vowel == "ㅑ":
            return "já"
        elif vowel == "ㅓ":
            return "a"
        elif vowel == "ㅕ":
            return "ja"
        elif vowel == "ㅗ":
            return "o"
        elif vowel == "ㅛ":
            return "jo"
        elif vowel == "ㅜ":
            return "u"
        elif vowel == "ㅠ":
            return "ju"
        elif vowel == "ㅡ":
            return "ü"
        elif vowel == "ㅣ":
            return "i"
        # Complex vowels
        elif vowel == "ㅐ":
            return "e"
        elif vowel == "ㅒ":
            return "je"
        elif vowel == "ㅔ":
            return "é"
        elif vowel == "ㅖ":
            return "jé"
        # Complex vowels with more than one characters (the syllables_to_characters method doesn't break them)
        elif vowel == "ㅘ":
            return "vá"
        elif vowel == "ㅙ":
            return "ve"
        elif vowel == "ㅚ":
            return "vé"
        elif vowel == "ㅝ":
            return "va"
        elif vowel == "ㅞ":
            return "ve"
        elif vowel == "ㅟ":
            return "vi"
        elif vowel == "ㅢ":
            return "üi"
        raise ValueError

    @staticmethod
    def transliterate_word(word: [Syllable]):
        result = ""

        for i, syllable in enumerate(word):
            previous_syllable = None
            next_syllable = None
            if i != 0:
                previous_syllable = word[i - 1]
            if i != len(word) - 1:
                next_syllable = word[i + 1]

            if syllable.leading_consonant is not None:
                if previous_syllable is None:
                    result += Hangul.word_initial_consonants(syllable.leading_consonant)
                else:
                    result += Hangul.syllable_initial_consonants(previous_syllable.batchim, syllable.leading_consonant)
            if syllable.vowel is not None:
                result += Hangul.transliterate_vowel(syllable.vowel)
            if syllable.batchim is not None:
                if next_syllable is None:
                    result += Hangul.word_final_consonants(syllable.batchim)
                else:
                    # Only for testing, must be changed later
                    result += Hangul.syllable_final_consonants(syllable.batchim, next_syllable)

        return result

    # Only returns true for complex characters.
    def is_character_korean(self, character):
        code_point = ord(character)
        SIndex = code_point - self.SBase
        if 0 <= SIndex < self.SCount:
            return True
        else:
            return False

    def transliterate_text(self, text):
        result = ""
        # Splitting may need to be improved to properly include linebreaks
        words = text.split() # text.split(' ') is worth consideration but might need some improvement
        for word in words:
            korean_word = []
            for character in word:
                if self.is_character_korean(character):
                    characters = self.syllables_to_characters(character)
                    leading_consonant = characters[0]
                    vowel = characters[1]
                    batchim = None
                    if len(characters) == 4:
                        batchim = self.merge_characters(characters[2:4])
                    elif len(characters) > 2:
                        batchim = characters[2]
                    korean_word.append(Syllable(leading_consonant, vowel, batchim))
                else:
                    result += self.transliterate_word(korean_word)
                    # print(korean_word, end="")
                    korean_word = []
                    result += character
            result += self.transliterate_word(korean_word)
            result += " "

        return result


translator = Hangul()
# print(translator.syllables_to_characters("ㄳ,ㄵ,ㄶ,ㄺ,ㄻ,ㄼ,ㄽ,ㄾ,ㄿ,ㅀ,ㅄ...밟"))
# print()
# print(translator.syllables_to_characters("대한민국 this is a test"))
# print(translator.transliterate_text(
#     "김정은(1984년 1월 8일[1] ~ )은 조선민주주의인민공화국의 최고지도자이다. 2000년대 후반부터 김정일의 후계자로 내세우는 등 차츰 영향력이 커지고 이름이 알려지기 시작했으며, 2010년부터 당 중앙군사위 부위원장 등으로 정치에 참여했다. 2011년 김정일의 사망 이후 3대 세습으로 조선민주주의인민공화국의 원수가 되었다."))
# print(translator.transliterate_text("책 속 에 서 나 드 라 마 속 에 서 사 랑 을 느 껴"))
# print(translator.transliterate_text("책 속에서나 드라마 속에서 사랑을 느껴"))
# print(translator.syllables_to_characters("씨"))
print(translator.transliterate_text("따뜻한"))
print(translator.transliterate_text("굳이"))
print(translator.transliterate_text("전했습니다"))
