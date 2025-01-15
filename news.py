import requests
from newspaper import Article
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def fetch_trending_articles(api_key, keywords):
    url = "https://newsapi.org/v2/everything"
    articles = []

    for keyword in keywords:
        params = {
            'q': keyword,
            'sortBy': 'popularity',
            'apiKey': api_key,
            'language': 'en',
            'pageSize': 5
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for article_data in data.get('articles', []):
                try:
                    # Create Article object
                    article = Article(article_data['url'])
                    # Download and parse article
                    article.download()
                    article.parse()
                    
                    # Only store title and full text content
                    articles.append({
                        'title': article.title,
                        'content': article.text
                    })
                except Exception as e:
                    print(f"Error processing article: {str(e)}")
                    continue
        else:
            print(f"Error fetching articles for keyword '{keyword}': {response.status_code}")

    return articles