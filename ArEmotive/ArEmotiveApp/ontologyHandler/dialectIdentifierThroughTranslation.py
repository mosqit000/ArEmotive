import translators as ts
import ArEmotiveApp.ontologyHandler.stemmers as stem


def checkDialect(word):
    try:
        result = ts.google(word, from_language='ar', to_language='en')
        result = ts.google(result, from_language='en', to_language='ar')
        if result == stem.stem(word) or result == word:
            return "العربية_الفصحى"
        else:
            return "العربية_الشامية"
    except :
        return "العربية_الشامية"
