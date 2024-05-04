def arabic_question(text):
    return 'ما هو لون السماء؟'

def english_question(text):
    return 'What is the color of the sky?'


def get_questions(text, lang):
    if lang == 'arabic':
        return arabic_question(text)
    elif lang == 'english':
        return english_question(text)
    else:
        return []