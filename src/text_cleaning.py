import re
from nltk.stem import WordNetLemmatizer


abbr_words = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not", 
              "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not", 
              "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", 
              "how's": "how is", "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", 
              "I've": "I have", "i'd": "i would", "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have","i'm": "i am", 
              "i've": "i have", "isn't": "is not", "it'd": "it would", "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have",
              "it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have","mightn't": "might not",
              "mightn't've": "might not have", "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", 
              "needn't've": "need not have","o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", 
              "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would", "she'd've": "she would have", "she'll": "she will", 
              "she'll've": "she will have", "she's": "she is", "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", 
              "so've": "so have","so's": "so as", "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is", 
              "there'd": "there would", "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", 
              "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", 
              "to've": "to have", "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", 
              "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are", 
              "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is", 
              "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have", "why's": "why is", 
              "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have", "would've": "would have", 
              "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would","y'all'd've": "you all would have",
              "y'all're": "you all are","y'all've": "you all have", "you'd": "you would", "you'd've": "you would have", "you'll": "you will", 
              "you'll've": "you will have", "you're": "you are", "you've": "you have"}

stopwords = ["a", "able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act", "actually", "added", 
             "adj", "affected", "affecting", "affects", "after", "afterwards", "again", "against", "ah", "ain't", "all", "allow", 
             "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an", "and", 
             "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", 
             "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "are", "aren", "arent", "aren't", 
             "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "auth", "available", "away", "awfully", 
             "b", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", 
             "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", 
             "between", "beyond", "biol", "both", "brief", "briefly", "but", "by", "c", "ca", "came", "can", "cannot", "cant", 
             "can't", "cause", "causes", "certain", "certainly", "changes", "clearly", "c'mon", "co", "com", "come", "comes", 
             "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", 
             "could", "couldnt", "couldn't", "course", "c's", "currently", "d", "date", "definitely", "described", "despite", 
             "did", "didn't", "different", "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards", "due", "during", 
             "e", "each", "ed", "edu", "effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough", 
             "entirely", "especially", "et", "et-al", "etc", "even", "ever", "every", "everybody", "everyone", "everything", 
             "everywhere", "ex", "exactly", "example", "except", "f", "far", "few", "ff", "fifth", "first", "five", "fix", 
             "followed", "following", "follows", "for", "former", "formerly", "forth", "found", "four", "from", "further", 
             "furthermore", "g", "gave", "get", "gets", "getting", "give", "given", "gives", "giving", "go", "goes", "going", 
             "gone", "got", "gotten", "greetings", "h", "had", "hadn't", "happens", "hardly", "has", "hasn't", "have", "haven't", 
             "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", 
             "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hi", "hid", "him", "himself", "his", "hither", 
             "home", "hopefully", "how", "howbeit", "however", "how's", "hundred", "i", "id", "i'd", "ie", "if", "ignored", 
             "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", 
             "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "into", "invention", 
             "inward", "is", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "i've", "j", "just", "k", "keep", 
             "keeps", "kept", "kg", "km", "know", "known", "knows", "l", "largely", "last", "lately", "later", "latter", "latterly", 
             "least", "less", "lest", "let", "lets", "let's", "like", "liked", "likely", "line", "little", "'ll", "look", "looking", 
             "looks", "ltd", "m", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", 
             "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", 
             "much", "mug", "must", "mustn't", "my", "myself", "n", "na", "name", "namely", "nay", "nd", "near", "nearly", 
             "necessarily", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "ninety", 
             "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", 
             "now", "nowhere", "o", "obtain", "obtained", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "omitted", 
             "on", "once", "one", "ones", "only", "onto", "or", "ord", "other", "others", "otherwise", "ought", "our", "ours", 
             "ourselves", "out", "outside", "over", "overall", "owing", "own", "p", "page", "pages", "part", "particular", 
             "particularly", "past", "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", 
             "pp", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", 
             "put", "q", "que", "quickly", "quite", "qv", "r", "ran", "rather", "rd", "re", "readily", "really", "reasonably", 
             "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", 
             "respectively", "resulted", "resulting", "results", "right", "run", "s", "said", "same", "saw", "say", "saying", 
             "says", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", 
             "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "shall", "shan't", "she", "shed", "she'd", 
             "she'll", "shes", "she's", "should", "shouldn't", "show", "showed", "shown", "showns", "shows", "significant", 
             "significantly", "similar", "similarly", "since", "six", "slightly", "so", "some", "somebody", "somehow", "someone", 
             "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically", "specified", 
             "specify", "specifying", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", 
             "suggest", "sup", "sure", "t", "take", "taken", "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", 
             "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", 
             "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", 
             "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", 
             "they've", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", 
             "three", "throug", "through", "throughout", "thru", "thus", "til", "tip", "to", "together", "too", "took", "toward", 
             "towards", "tried", "tries", "truly", "try", "trying", "ts", "t's", "twice", "two", "u", "un", "under", "unfortunately", 
             "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "us", "use", "used", "useful", "usefully", 
             "usefulness", "uses", "using", "usually", "v", "value", "various", "'ve", "very", "via", "viz", "vol", "vols", "vs", "w", 
             "want", "wants", "was", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "went", "were", 
             "we're", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", 
             "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", 
             "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", 
             "whose", "why", "why's", "widely", "will", "willing", "wish", "with", "within", "without", "wonder", "wont", "won't", 
             "words", "world", "would", "wouldnt", "wouldn't", "www", "x", "y", "yes", "yet", "you", "youd", "you'd", "you'll", "your", 
             "youre", "you're", "yours", "yourself", "yourselves", "you've", "z", "zero"]


class TextCleaner:

    def __init__(self) -> None:
        self.lemmatizer = WordNetLemmatizer()
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
        abbreviation = ' '.join([abbr_words[t] if t in abbr_words else t for t in text.split(" ")]) 
        return abbreviation

    def __remove_whitespace(self, text):
        cleaned_text = ' '.join(text.split())
        return cleaned_text

    def __lemmatize_text(self, tokens):
        lemmatized_tokens = ' '.join([self.lemmatizer.lemmatize(word) for word in tokens.split()])
        return lemmatized_tokens

    def remove_stopwords(self, tokens):
        filtered_tokens = ' '.join([word for word in tokens.split() if word not in stopwords])
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