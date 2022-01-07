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
    hyperlinks = []
    dead_links = []
    dead_links_full = []
    name_list = []
    value_list = []
    protocol = "https://"


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
            try:
                response = req.get(url)
            except ConnectionError:
                return render_template("index.html")

            soup = BeautifulSoup(response.content, 'html.parser')

            # SCRAPING SITE
            if len(url) != 0 and len(tag) == 0 and len(atr) == 0 and len(val) == 0:
                    final = []
                    all_elements = [x for x in soup.find_all(True)]
                    src_list = [x.get("src") for x in all_elements if x.get("src") != None]
                    data_src_list = [x.get("data-src") for x in all_elements if x.get("data-src") != None]
                    href_list = [x.get("href") for x in all_elements if x.get("href") != None]
                    added_lists = list(set(src_list + data_src_list + href_list))
                    filtered = [x for x in added_lists if x.startswith("/") or x.startswith("http")]
                    for i in filtered:
                        if i.startswith("/"):
                            i = f"https://{domain_name}{i}"
                        final.append(i)
                    for link in final:
                        try:
                            status_code = req.get(link, timeout=4).status_code
                        except Exception as err:
                            print(err)
                            continue
                        if status_code == 404:
                            dead_links_full.append(str(link))

            # SCRAPING TAG
            elif len(url) != 0 and len(tag) != 0 and len(atr) == 0 and len(val) == 0:
                if tag.endswith('@'):
                    tag = tag.removesuffix('@')
                    scraped_tags = soup.find_all(tag)
                    for single_tag in scraped_tags:
                        name_list.append(single_tag.text)
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
                        value_list.append(single_tag[atr])
                elif atr.endswith('#'):
                    atr = atr.removesuffix('#')
                    scraped_tags = [x[atr] for x in soup.find_all(tag, attrs={atr: True})]
                    filtered_content = [x.strip() for x in scraped_tags if x.startswith("http") or x.startswith("/")]
                    filtered_content = list(set(filtered_content))
                    for link in filtered_content:
                        if link.startswith("/"):
                            link = protocol + domain_name + link
                            hyperlinks.append(link)
                        else:
                            hyperlinks.append(link)
                elif atr.endswith('!'):
                    atr = atr.removesuffix('!')
                    scraped_tags = [x[atr] for x in soup.find_all(tag, attrs={atr: True})]
                    filtered_content = [x.strip() for x in scraped_tags if x.startswith("http") or x.startswith("/")]
                    filtered_content = list(set(filtered_content))
                    for link in filtered_content:
                        if link.startswith("/"):
                            link = protocol + domain_name + link
                        try:
                            status_code = req.get(link, timeout=4).status_code
                        except Exception as err:
                            print(err)
                            continue
                        if status_code == 404:
                            dead_links.append(str(link))
                elif atr.endswith('@'):
                    atr = atr.removesuffix('@')
                    scraped_tags = soup.find_all(tag, attrs={atr: True})
                    for single_tag in scraped_tags:
                        name_list.append(single_tag.text)
                else:
                    scraped_tags = soup.find_all(tag, attrs={atr: True})
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag)

            # SCRAPING ATTRIBUTE VALUE
            elif len(url) != 0 and len(tag) != 0 and len(atr) != 0 and len(val) != 0:
                if val.endswith('@'):
                    val = val.removesuffix('@')
                    scraped_tags = soup.find_all(tag, attrs={atr: val})
                    for single_tag in scraped_tags:
                        name_list.append(single_tag.text)
                else:
                    scraped_tags = soup.find_all(tag, attrs={atr: val})
                    for single_tag in scraped_tags:
                        list_tag.append(single_tag)
            else:
                pass

        # USED TAGS/ATTRIBUTES/VALUES LABEL
        used_tags = f'{tag} {atr} {val}'

    return render_template(
        'index.html',
        url = url,
        dead_links_full = dead_links_full,
        list_tag = list_tag,
        name_list = name_list,
        value_list = value_list,
        used_tags = used_tags,
        dead_links = dead_links,
        hyperlinks = hyperlinks
        )


if __name__ == '__main__':
    app.run(debug=True)
