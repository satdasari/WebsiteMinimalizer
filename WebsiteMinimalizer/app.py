from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return render_template('index.html', results=f"Error: {e}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove hyperlinks
    for a in soup.find_all('a'):
        a.extract()
    
    # Extract headings and paragraphs
    content = ''
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        text = element.get_text()
        sentences = re.findall(r'([A-Z][^\.!?]*[\.!?])', text)
        cleaned_sentences = [s for s in sentences if len(s.split()) >= 4]
        cleaned_text = ' '.join(cleaned_sentences)
        
        if cleaned_text:
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                content += f"<{element.name}>{cleaned_text}</{element.name}>"
            else:
                content += f"<p>{cleaned_text}</p>"
    
    return render_template('index.html', results=content)

if __name__ == '__main__':
    app.run(debug=True)
