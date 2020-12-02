from transformers import *
from datasets import *
import torch.nn as nn
import torch.utils.data as Data
from torch.utils.data import Dataset
import torch
from textblob import TextBlob

# for korean: https://colab.research.google.com/drive/1tIf0Ugdqg4qT7gcxia3tL7und64Rv1dP

class Analyzer:
    def __init__(self, english_path='./checkpoint.pt', korean_path='./kor_model.pt'):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.kor_tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case=False)
        self.model = None
        self.kor_model = None
        self.english_path = english_path
        self.load_english_model(english_path)
        self.load_korean_model(korean_path)

    def tokenize(self, text):
        return self.tokenizer(text, padding='max_length', max_length=256, truncation=True, return_tensors='pt')

    def tokenize_kor(self, text):
        return self.kor_tokenizer(text, padding='max_length', max_length=128, truncation=True, return_tensors='pt')

    def load_english_model(self, path):
        config = BertConfig.from_pretrained('bert-base-uncased')
        config.num_labels = 2
        self.model = BertForSequenceClassification.from_pretrained("bert-base-uncased", config=config).to(self.device)
        self.model = nn.DataParallel(self.model)
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint, strict=False)

    def load_korean_model(self, path):
        #self.kor_model = BertForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=2).to(self.device)
        self.kor_model = torch.load(path, map_location=self.device)

    def analyze_sentences(self, texts):
        if type(texts) != list or len(texts) == 0 or type(texts[0]) != str:
            raise AssertionError("The input type of analyze_sentences should be a list of text,"
                                 " containing at least one string sentence!")
        inputs = self.tokenize(texts)
        for key in inputs.keys():
            inputs[key] = inputs[key].to(self.device)
        output = self.model(**inputs)[0].argmax(1)
        normalized = output * 2 - 1
        return list(normalized.cpu().numpy())

    def analyze_korean_sentences(self, texts):
        if type(texts) != list or len(texts) == 0 or type(texts[0]) != str:
            raise AssertionError("The input type of analyze_sentences should be a list of text,"
                                 " containing at least one string sentence!")
        inputs = self.tokenize_kor(texts)
        for key in inputs.keys():
            inputs[key] = inputs[key].to(self.device)
        output = self.kor_model(**inputs)[0].argmax(1)
        normalized = output * 2 - 1
        return list(normalized.numpy())

if __name__ == '__main__':
    # Example usage
    # from sentiment import Analyzer
    analyzer = Analyzer()
    sample_text = ["I am so happy", "This is so sad ..", "This is a neutral sentence."]
    out = analyzer.analyze_sentences(sample_text)
    print(f"Example output for english sentence: {sample_text}\n{out}") # outputs [1, -1, 1]
    sample_kor_text = ["연기는 별로지만 재미 하나는 진짜 끝내줌!", "주연배우가 아깝다. 총체적 난국..."]
    out_kor = analyzer.analyze_korean_sentences(sample_kor_text)
    print(f"Example output for Korean sentence: {sample_kor_text}\n{out_kor}") # outputs [1, -1]

