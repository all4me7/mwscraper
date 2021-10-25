from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests as req


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def main():
    # VARIABLES
    list_tag = []

    # GET VALUES FROM HTML 
    if request.method == 'POST':
        if 'approve' in request.form:
            url = request.form['url']
            tag = request.form['tag']
            atr = request.form['attribute']
            val = request.form['value']

            # FIXING URL'S 
            if url.startswith('https://'):
                pass
            else:
                url = 'https://' + url

            # SOUP SETUP
            response = req.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # TAG
            if len(url) != 0 and len(tag) != 0 and len(atr) == 0 and len(val) == 0:
                if tag.endswith('*'):
                    tag = tag.removesuffix('*')
                    scraped_tags = soup.find_all(tag)
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag.text)
                else:
                    scraped_tags = soup.find_all(tag)
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag)

            # ATTRIBUTE
            elif len(url) != 0 and len(tag) != 0 and len(atr) != 0 and len(val) == 0:
                if atr.endswith('$'):
                    atr = atr.removesuffix('$')
                    scraped_tags = soup.find_all(tag, attrs={atr: True})
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag[atr])
                elif atr.endswith('*'):
                    atr = atr.removesuffix('*')
                    scraped_tags = soup.find_all(tag, attrs={atr: True})
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag.text)
                else:
                    scraped_tags = soup.find_all(tag, attrs={atr: True})
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag)    
            
            # ATTRIBUTE VALUE 
            elif len(url) != 0 and len(tag) != 0 and len(atr) != 0 and len(val) != 0:
                if val.endswith('*'):
                    val = val.removesuffix('*')
                    scraped_tags = soup.find_all(tag, attrs={atr: val})
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag.text)
                else:
                    scraped_tags = soup.find_all(tag, attrs={atr: val})
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag)  
            else:
                pass

        # USED TAGS/ATTRIBUTES/VALUES LABEL        
        used_tags = f'{tag} {atr} {val}'
            
    return render_template('index.html', list_tag=list_tag, url=url, used_tags=used_tags)
    

if __name__ == '__main__':
    app.run()
