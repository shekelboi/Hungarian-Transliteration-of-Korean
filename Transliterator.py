import codecs, sys, os, math


class Syllable:
    def __init__(self, c1, c2, c3):
        self.leading_consonant = c1
        self.vowel = c2
        self.batchim = c3


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

    def transliterate_vowel(self, vowel):
        # Normal vowels
        if vowel == "ㅏ":
            return "á"
        elif vowel == "ㅑ":
            return "j"
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

    def form_batchim_from_characters(self, characters):
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

    def transliterate_word(self, word: [Syllable]):
        if len(word) == 0:
            return ""

        result = ""

        for syllable in word:
            result += self.transliterate_vowel(syllable.vowel)

        return result

    def is_character_korean(self, character):
        code_point = ord(character)
        SIndex = code_point - self.SBase
        if 0 <= SIndex < self.SCount:
            return True
        else:
            return False

    def transliterate_text(self, text):
        result = ""
        words = text.split()
        for word in words:
            korean_word = []
            for character in word:
                if self.is_character_korean(character):
                    characters = self.syllables_to_characters(character)
                    leading_consonant = characters[0]
                    vowel = characters[1]
                    batchim = None
                    if len(characters) == 4:
                        batchim = self.form_batchim_from_characters(characters[2:4])
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
print(translator.transliterate_text(
    "김정은(1984년 1월 8일[1] ~ )은 조선민주주의인민공화국의 최고지도자이다. 2000년대 후반부터 김정일의 후계자로 내세우는 등 차츰 영향력이 커지고 이름이 알려지기 시작했으며, 2010년부터 당 중앙군사위 부위원장 등으로 정치에 참여했다. 2011년 김정일의 사망 이후 3대 세습으로 조선민주주의인민공화국의 원수가 되었다."))