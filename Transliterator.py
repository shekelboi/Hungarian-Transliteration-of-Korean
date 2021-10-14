import codecs, sys, os, math


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

    '''
    Hangul syllables consists of 2 to 3 characters.
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
    '''

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


translator = Hangul()
print(translator.syllables_to_characters("힣"))
print(translator.syllables_to_characters("대한민국 this is a test"))
