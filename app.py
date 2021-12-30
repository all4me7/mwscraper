from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests.exceptions import ConnectionError
import requests as req


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def main():
    # VARIABLES
    list_tag = []
    protocol = "https://"
    temp = []

    # GET VALUES FROM HTML 
    if request.method == 'POST':
        if 'approve' in request.form:
            url = request.form['url']
            tag = request.form['tag']
            atr = request.form['attribute']
            val = request.form['value']

            # FIXING URL'S 
            if url.startswith(protocol) is not True:
                url = protocol + url

            domain_name = urlparse(url).netloc

            # SOUP SETUP
            response = req.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # SCRAPING TAG
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

            #SCRAPING  ATTRIBUTE
            elif len(url) != 0 and len(tag) != 0 and len(atr) != 0 and len(val) == 0:
                if atr.endswith('$'):
                    atr = atr.removesuffix('$')
                    scraped_tags = soup.find_all(tag, attrs={atr: True})
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag[atr])
                elif atr.endswith('#'):
                    atr = atr.removesuffix('#')
                    scraped_tags = [x[atr] for x in soup.find_all(tag, attrs={atr: True})]
                    filtered_content = [x.strip() for x in scraped_tags if x.startswith("http") or x.startswith("/")]
                    filtered_content = list(set(filtered_content))
                    if len(filtered_content) > 0:
                        for link in filtered_content:
                            if link.startswith("/"):
                                link = protocol + domain_name + link
                                list_tag.append(link)
                            else:
                                list_tag.append(link)
                elif atr.endswith('!'):
                    atr = atr.removesuffix('!')
                    scraped_tags = [x[atr] for x in soup.find_all(tag, attrs={atr: True})]
                    filtered_content = [x.strip() for x in scraped_tags if x.startswith("http") or x.startswith("/")]
                    filtered_content = list(set(filtered_content))
                    if len(filtered_content) > 0:
                        for link in filtered_content:
                            if link.startswith("/"):
                                link = protocol + domain_name + link
                            try:
                                status_code = req.get(link, timeout=4).status_code
                            except:
                                continue       
                            if status_code == 404:
                                list_tag.append(link)
                    else:
                        list_tag.append("Dead links not found.")
                elif atr.endswith('*'):
                    atr = atr.removesuffix('*')
                    scraped_tags = soup.find_all(tag, attrs={atr: True})
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag.text)
                else:
                    scraped_tags = soup.find_all(tag, attrs={atr: True})
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag)    
            
            # SCRAPING ATTRIBUTE VALUE 
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
    app.run(debug=True)
