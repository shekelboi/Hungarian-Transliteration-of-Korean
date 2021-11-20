import os
import sys
from argparse import ArgumentParser


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
        """ Merge complex Korean characters. """
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
        """ Separate complex Korean characters. """
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

    def syllables_to_characters(self, text):
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
        """ Retrieve the default pronunciation a Korean consonant. """
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
            return "gsz"
        elif consonant == "ㄵ":
            return "ndzs"
        elif consonant == "ㄶ":
            return "nh"
        elif consonant == "ㄺ":
            return "rg"
        elif consonant == "ㄻ":
            return "rm"
        elif consonant == "ㄼ":
            return "rb"
        elif consonant == "ㄽ":
            return "rs"
        elif consonant == "ㄾ":
            return "rt"
        elif consonant == "ㄿ":
            return "rp"
        elif consonant == "ㅀ":
            return "rh"
        elif consonant == "ㅄ":
            return "bsz"
        else:
            raise ValueError

    # Part 4 Section 8 Korean Prules rule is unclear
    # The rules regarding the pronunciation of 'ㅅ' are not properly described
    # The rules about the pronunciation of 'ㄹ' are lacking
    @staticmethod
    def syllable_final_consonants(current_batchim, next_syllable: Syllable):
        """ Transliterate a Korean consonant at the end of a syllable. """
        # Simple consonants
        # &
        # Tense consonants (these all could be potentially wrong, the same rules
        # may apply to them as to the simples, it needs to be tested)
        # Maybe the consonants should be doubled for tense consonants.

        # Sound assimilation to ㄴ and ㅁ
        if next_syllable.leading_consonant in ["ㄴ", "ㅁ"]:
            if current_batchim in ["ㄱ", "ㄲ", "ㅋ", "ㄳ", "ㄺ"]:
                return "ng"
            elif current_batchim in ["ㅍ", "ㄼ", "ㄿ", "ㅄ"]:
                return "m"
            elif current_batchim in ["ㅂ", "ㅃ"]:
                return "m" if current_batchim == "ㅂ" else "mm"
            elif current_batchim in ["ㅅ", "ㅆ"]:
                return "n" if current_batchim == "ㅅ" else "nn"
            elif current_batchim == ["ㄷ", "ㄸ", "ㅈ", "ㅉ"]:
                return "n" if current_batchim in ["ㄷ", "ㅈ"] else "nn"
            elif current_batchim in ["ㅊ", "ㅌ", "ㅎ", "ㄵ"]:
                return "n"

        # No sound before ㅎ
        if next_syllable.leading_consonant == "ㅎ":
            if current_batchim in ["ㄱ", "ㄲ", "ㄷ", "ㄸ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅈ", "ㅉ", "ㅊ", "ㅌ", "ㄵ"]:
                return ""

        # Sound assimilation before syllable that begins with ㅣ
        if current_batchim in ["ㄷ", "ㅌ", "ㄾ"]:
            if next_syllable.leading_consonant == "ㅇ" and next_syllable.vowel == "ㅣ":
                return ""

        if current_batchim == "ㄹ" and next_syllable.leading_consonant != "ㅇ":
            return "l"
        elif current_batchim in ["ㅅ", "ㅆ"]:
            if next_syllable.leading_consonant in ["ㅈ", "ㅊ", "ㅌ"]:
                return ""
            elif next_syllable.leading_consonant == "ㅇ":
                if next_syllable.vowel == "ㅣ":
                    return "s" if current_batchim == "ㅅ" else "ss"
                else:
                    return "sz" if current_batchim == "ㅅ" else "ssz"
            elif next_syllable.leading_consonant == "ㄷ":
                return "d"
        elif current_batchim in ["ㅈ", "ㅉ"]:
            return "d"
        elif current_batchim == "ㅊ":
            return "n"
        elif current_batchim == "ㅋ":
            return "g"
        elif current_batchim == "ㅍ":
            return "b"
        elif current_batchim == "ㅎ":
            if next_syllable.leading_consonant in ["ㄱ", "ㄲ", "ㄷ", "ㅈ", "ㅊ", "ㅅ"]:
                return ""
        # Complex consonants
        elif current_batchim == "ㄳ":
            if next_syllable.leading_consonant in ["ㄱ", "ㄲ"]:
                return "g"
        elif current_batchim == "ㄵ":
            if next_syllable.leading_consonant == "ㄷ":
                return "d"
        elif current_batchim == "ㄶ":
            if next_syllable.leading_consonant in ["ㄱ", "ㄲ", "ㄷ", "ㅈ", "ㄴ", "ㅇ"]:
                return "n"
            elif next_syllable.leading_consonant == "ㅅ":
                return "n"
        elif current_batchim == "ㄺ":
            if next_syllable.leading_consonant == "ㄱ":
                return "r"
            else:
                return "n"
        elif current_batchim == "ㄻ":
            return "m"
        elif current_batchim in ["ㄼ", "ㄽ", "ㄾ"]:
            return "r" if next_syllable.leading_consonant == "ㅇ" else "l"
        elif current_batchim == "ㄿ":
            return "b"
        elif current_batchim == "ㅀ":
            if next_syllable.leading_consonant in ["ㄱ", "ㄷ", "ㅈ", "ㅅ", "ㅆ", "ㄴ"]:
                return "r"
        elif current_batchim == "ㅄ":
            if next_syllable.leading_consonant == "ㅇ":
                return "bs"

        # Other cases such as:
        # ㄴ, ㅁ, ㅇ
        return Hangul.default_consonant(current_batchim)

    @staticmethod
    def syllable_initial_consonants(previous_batchim, current_initial, current_vowel):
        """ Transliterate a Korean consonant at the beginning of a syllable. """
        # Simple consonants and tense consonants
        if current_initial in ["ㄱ", "ㄲ"]:
            if previous_batchim == "ㄺ":
                return "l" if current_initial == "ㄱ" else "ll"
            elif previous_batchim == "ㅎ":
                return "k" if current_initial == "ㄱ" else "kk"
        elif current_initial == "ㄴ":
            if previous_batchim in ["ㅀ", "ㄹ"]:
                return "l"
        elif current_initial in ["ㄷ", "ㄸ"]:
            if previous_batchim in ["ㅎ", "ㄶ", "ㅀ"]:
                return "t" if current_initial == "ㄷ" else "tt"
        elif current_initial == "ㄹ":
            if previous_batchim in ["ㅁ", "ㅇ", "ㄱ", "ㅂ"]:
                return "n"
            elif previous_batchim is not None:
                return "l"
        elif current_initial in ["ㅅ", "ㅆ"]:
            if previous_batchim in ["ㅎ", "ㄶ", "ㅀ"]:
                return "ssz"
            if current_vowel == "ㅣ":
                return "ss" if current_initial == "ㅆ" else "s"
        elif current_initial == "ㅇ":
            if current_vowel == "ㅣ":
                if previous_batchim in ["ㅌ", "ㄾ"]:
                    return "cs"
                elif previous_batchim == "ㄷ":
                    return "dzs"
            # If the previous character was complex (but not ㄾ) we take the default pronunciation of the second
            # letter from that.
            if Complex.is_complex(previous_batchim):
                return Hangul.default_consonant(Complex.separate_characters(previous_batchim).second)
            else:
                return ""
        elif current_initial in ["ㅈ", "ㅉ"]:
            if previous_batchim in ["ㅎ", "ㄶ", "ㅀ"]:
                return "cs" if current_initial == "ㅈ" else "css"
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

        # Other cases such as:
        # ㅁ, ㅂ, ㅊ, ㅋ, ㅌ, ㅍ
        # ㅃ
        return Hangul.default_consonant(current_initial)

    @staticmethod
    def word_final_consonants(consonant):
        """ Transliterate a Korean consonant at the end of a word. """
        if consonant == "ㄱ":
            return "k"
        elif consonant == "ㄴ":
            return "n"
        elif consonant == "ㄷ":
            return "t"
        elif consonant == "ㄹ":
            return "l"
        elif consonant == "ㅁ":
            return "m"
        elif consonant == "ㅂ":
            return "p"
        elif consonant == "ㅅ":
            return "d"
        elif consonant == "ㅇ":
            return "ng"
        elif consonant == "ㅈ":
            return "d"
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
            return "d"
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
    def word_initial_consonants_with_vowel(consonant, vowel):
        """ For special cases where the vowel affects the pronunciation (e.g. ㅅ) """
        if consonant == "ㅅ":
            if vowel == "ㅣ":
                return "s"
        return Hangul.word_initial_consonants(consonant)

    @staticmethod
    def word_initial_consonants(consonant):
        """ Transliterate a Korean consonant at the beginning of a word. """
        if consonant == "ㄱ":
            return "k"
        elif consonant == "ㄴ":
            return "n"
        elif consonant == "ㄷ":
            return "t"
        elif consonant == "ㄹ":
            return "l"
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
        """ Transliterate a Korean vowel. Default pronunciation is used. """
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
            return "é"  # Alternatively e
        elif vowel == "ㅒ":
            return "jé"  # Alternatively je
        elif vowel == "ㅔ":
            return "é"
        elif vowel == "ㅖ":
            return "jé"
        # Complex vowels with more than one characters (the syllables_to_characters method doesn't break them)
        elif vowel == "ㅘ":
            return "vá"
        elif vowel == "ㅙ":
            return "vé"
        elif vowel == "ㅚ":
            return "vé"
        elif vowel == "ㅝ":
            return "va"
        elif vowel == "ㅞ":
            return "vé"
        elif vowel == "ㅟ":
            return "vi"
        elif vowel == "ㅢ":
            return "üi"
        raise ValueError

    @staticmethod
    def transliterate_word(word: [Syllable]):
        """ Transliterate a Korean word. """
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
                    result += Hangul.word_initial_consonants_with_vowel(syllable.leading_consonant, syllable.vowel)
                else:
                    result += Hangul.syllable_initial_consonants(previous_syllable.batchim, syllable.leading_consonant,
                                                                 syllable.vowel)
            if syllable.vowel is not None:
                result += Hangul.transliterate_vowel(syllable.vowel)
            if syllable.batchim is not None:
                if next_syllable is None:
                    result += Hangul.word_final_consonants(syllable.batchim)
                else:
                    result += Hangul.syllable_final_consonants(syllable.batchim, next_syllable)

        return result

    def is_character_korean(self, character):
        """
        Only returns true for Korean syllables.
        See: https://en.wikipedia.org/wiki/Hangul_Syllables
        """
        code_point = ord(character)
        SIndex = code_point - self.SBase
        if 0 <= SIndex < self.SCount:
            return True
        else:
            return False

    def transliterate_text(self, text):
        """ Transliterate a block of text. """
        result = ""
        # Splitting may need to be improved to properly include linebreaks
        words = text.split(' ')  # is worth consideration but might need some improvement
        for word in words:
            korean_word = []
            for character in word:
                if self.is_character_korean(character):
                    characters = self.syllables_to_characters(character)
                    leading_consonant = characters[0]
                    vowel = characters[1]
                    batchim = None
                    if len(characters) == 4:
                        batchim = Complex.merge_characters(characters[2:4])
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


parser = ArgumentParser("With the help of this script you can transliterate Hangul text into Hungarian.")
parser.add_argument('string', nargs='?', help="Text that the user wants to translate.", default=None)
parser.add_argument("-i", "--input", nargs=1, metavar="input", help="Load a file.")
parser.add_argument("-o", "--output", nargs=1, metavar="output",
                    help="Create a new file with the transliteration.")
parser.add_argument("-d", "--display", action="store_true",
                    help="Whether the user wants to display the transliteration in the console")

args = parser.parse_args()

translator = Hangul()

if args.string is not None:
    print(translator.transliterate_text(args.string))

if args.output is not None and args.input is None:
    parser.error("Input wasn't provided even though output was.")
elif args.input is not None:
    input_name = args.input[0]
    with open(input_name, mode="r", encoding="utf-8") as file:
        original_text = file.read()
    transliteration = translator.transliterate_text(original_text)
    if args.display:
        print(transliteration)
    if args.output is not None:
        with open(args.output[0], mode="w", encoding="utf-8") as file:
            file.write(transliteration)