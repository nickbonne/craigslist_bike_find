
import re
import requests
from bs4 import BeautifulSoup


def main():

    pass


class Scrape:

    def scrape_search_pg(page):

        response = requests.get(page)
        soup = BeautifulSoup(response.content, 'lxml')
        soup = soup.find_all(class_='result-title hdrlnk')
        links = []
        titles = []

        for hit in soup:

            result = []

            title = re.findall(r'>(.*?)<', str(hit))[0].lower()
            url = re.findall(r'href="(.*?)">', str(hit))[0]

            if 'women' not in title and \
               title not in titles:

                result.append([title, url])
                titles.append(title)
                links.append(result)

        return links

    def scrape_post_pg(url):

        key_cheat = ['keywords', 'keyword']

        response = requests.get(url)
        page_soup = BeautifulSoup(response.content, 'lxml')

        price = page_soup.find(class_='price')
        price = re.findall(r'\$.*<', str(price))[0][:-1]

        size = page_soup.find(class_='attrgroup')

        try:

            size = re.findall(r'(?<=dimensions:\s<b>).*(?=<\/b>)',
                              str(size).lower())[0]

        except:

            size = ''

        item_descrpt = page_soup.find(id='postingbody')
        # finds the item's description <div>
        item_descrpt = re.findall(r'<\/div>([\s\S]*)</section>',
                                  str(item_descrpt))[0].strip().lower()
        # removes <a> tags and their contents
        item_descrpt = re.sub(r'(<a\s.+>)', '', item_descrpt)
        # remove html tags
        item_descrpt = re.sub(r'<[^<]+?>', '', item_descrpt)
        # remove some nonalpha characters
        item_descrpt = re.sub(r'[\:;!?(){}\[\]\\/]',
                              ' ', item_descrpt)
        # remove line breaks
        item_descrpt = item_descrpt.replace('\n', '')

        # removes anything after "keyword" or "keywords"
        # in item description
        if any(k in item_descrpt for k in key_cheat):

            d_split = item_descrpt.split(' ')

            for k in key_cheat:

                try:

                    item_descrpt = ' '.join(d_split[:d_split.index(k)])

                except:

                    pass

        # fixing sizing found in item_descrpt for filter
        # "size 54" becomes "size54"
        # "54 cm" becomes "54cm"
        try:

            size_fix = re.search(r'(size\s\d{2}(\.(?=\d)\d{0,1})?)',
                                 item_descrpt).group(0)
            size_fix = re.sub(r'\s', '', size_fix)
            item_descrpt = re.sub(r'(size\s\d{2}(\.(?=\d)\d{0,1})?)', size_fix,
                                  item_descrpt)

        except:

            pass

        try:

            size_fix = re.findall(r'(\d{2}(\.\d)?\scm)', item_descrpt).group(0)
            size_fix = re.sub(r'\s', '', size)
            item_descrpt = re.sub(r'(\d{2}(\.\d)?\scm)',
                                  size_fix, item_descrpt)

        except:

            pass

        return item_descrpt, price, size


if __name__ == '__main__':

    main()
