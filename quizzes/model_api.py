def simple_question(text):
    return [{ 'question': 'What is the color of the sky?', 'answer': "Blue"}, {'question': 'Why we are here?', 'answer': 'To learn'}]

def multiple_choices(text):
    return [{'question': 'What is the color of the sky?', 'choices': ['Blue', 'Red', 'Green', 'Yellow'], 'answer': 'Blue'}, {'question': 'Why we are here?', 'choices': ['To learn', 'To play', 'To eat', 'To sleep'], 'answer': 'To learn'}]

def match_answer(text):
    return {'question': ['What is the color of the sky?', 'Why we are here?'], 'answer': ['Blue', 'To learn']}

def true_false(text):
    return [{'question': 'The sky is blue.', 'answer': 'True'}, {'question': 'We are here to learn.', 'answer': 'True'}]

def fill_blank(text):
    return [{'question': 'The sky is __.', 'answer': 'blue'}, {'question': 'We are here to __.', 'answer': 'learn'}]

def get_questions(text, question_type):
    if question_type == 'simple':
        return simple_question(text)
    elif question_type == 'multiple':
        return multiple_choices(text)
    elif question_type == 'match':
        return match_answer(text)
    elif question_type == 'true_false':
        return true_false(text)
    elif question_type == 'fill':
        return fill_blank(text)
    else:
        return []