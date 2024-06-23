import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data (run this only once)
nltk.download('stopwords')
nltk.download('punkt')

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove punctuation and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    # Convert text to lowercase
    text = text.lower()
    # Tokenize text
    words = word_tokenize(text)
    # Remove stopwords("and," "the," "is,")

    stop_words = set(stopwords.words('english'))
    
    words = [word for word in words if word not in stop_words]
    # Join words back into a single string
    cleaned_text = ' '.join(words)
    return cleaned_text
