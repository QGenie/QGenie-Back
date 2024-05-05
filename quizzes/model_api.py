# from transformers import AutoTokenizer,AutoModelForSeq2SeqLM


# model = AutoModelForSeq2SeqLM.from_pretrained("MIIB-NLP/Arabic-question-generation")
# tokenizer = AutoTokenizer.from_pretrained("MIIB-NLP/Arabic-question-generation")

# def get_question(context,answer):
#   text="context: " +context + " " + "answer: " + answer + " </s>"
#   text_encoding = tokenizer.encode_plus(
#       text,return_tensors="pt"
#   )
#   model.eval()
#   generated_ids =  model.generate(
#     input_ids=text_encoding['input_ids'],
#     attention_mask=text_encoding['attention_mask'],
#     max_length=64,
#     num_beams=5,
#     num_return_sequences=1
#   )
#   return tokenizer.decode(generated_ids[0],skip_special_tokens=True,clean_up_tokenization_spaces=True).replace('question: ',' ')


# def arabic_question(context, answer):
#     return get_question(context,answer)



# def english_question(text, answer):
#     return 'What is the color of the sky?'


# def get_questions(context, answer, lang):
#     if lang == 'arabic':
#         return get_question(context,answer)
#     elif lang == 'english':
#         return english_question(context, answer)
#     else:
#         return []