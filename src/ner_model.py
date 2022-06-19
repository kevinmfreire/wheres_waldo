from transformers import BertTokenizer, TFBertForTokenClassification
from transformers import pipeline

tokenizer = BertTokenizer.from_pretrained("dslim/bert-base-NER")
model = TFBertForTokenClassification.from_pretrained("dslim/bert-base-NER")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)
example = "My name is Kevin , I live in Canada and I work for Apple"

ner_results = nlp(example)
print(ner_results)