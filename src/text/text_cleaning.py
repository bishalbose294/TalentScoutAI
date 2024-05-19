import re
from nltk.stem import WordNetLemmatizer
from src.utils.commonutils import CommonUtils

class TextCleaner:

    def __init__(self) -> None:
        self.lemmatizer = WordNetLemmatizer()
        self.comonUtils = CommonUtils()
        self.stopwords = self.comonUtils.loadStropwords()
        self.abbr_words = self.comonUtils.loadAbbreviations()
        pass

    def __remove_html_tags(self, text):
        clean_text = re.sub(r'<.*?>', '', text)
        return clean_text

    def __remove_special_characters(self, text):
        clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return clean_text

    def __convert_to_lowercase(self, text):
        lowercased_text = text.lower()
        return lowercased_text

    def __change_abbr(self, text):
        abbreviation = ' '.join([self.abbr_words[t] if t in self.abbr_words else t for t in text.split(" ")]) 
        return abbreviation

    def __remove_whitespace(self, text):
        cleaned_text = ' '.join(text.split())
        return cleaned_text

    def __lemmatize_text(self, tokens):
        lemmatized_tokens = ' '.join([self.lemmatizer.lemmatize(word) for word in tokens.split()])
        return lemmatized_tokens

    def remove_stopwords(self, tokens):
        filtered_tokens = ' '.join([word for word in tokens.split() if word not in self.stopwords])
        return filtered_tokens

    def remove_numbers(self, text):
        result = re.sub(r'[0-9]+', ' ', text)
        result = self.__remove_whitespace(result)
        return result

    def clean_text(self, text):
        sentence = self.__remove_html_tags(text)
        sentence = self.__change_abbr(sentence)
        sentence = self.__lemmatize_text(sentence)
        sentence = self.__remove_special_characters(sentence)
        sentence = self.__convert_to_lowercase(sentence)
        sentence = self.__remove_whitespace(sentence)
        return sentence
        pass