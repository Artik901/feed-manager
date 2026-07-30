import re


TRANSLIT = {
    "а":"a","б":"b","в":"v","г":"g","д":"d",
    "е":"e","ё":"e","ж":"zh","з":"z",
    "и":"i","й":"y","к":"k","л":"l",
    "м":"m","н":"n","о":"o","п":"p",
    "р":"r","с":"s","т":"t","у":"u",
    "ф":"f","х":"h","ц":"c","ч":"ch",
    "ш":"sh","щ":"sch","ъ":"",
    "ы":"y","ь":"","э":"e",
    "ю":"yu","я":"ya"
}


def translit(text):

    result = ""

    for char in text.lower():

        if char in TRANSLIT:
            result += TRANSLIT[char]
        else:
            result += char


    result = re.sub(
        r"[^a-z0-9]+",
        "_",
        result
    )


    result = result.strip("_")


    if not result:
        result = "feed"


    return result