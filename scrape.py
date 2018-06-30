
import os
import re
import requests 
from bs4 import BeautifulSoup


def main():

    pass


class Scrape:

    def scrape(self, page):

        response = requests.get(page)
        soup = BeautifulSoup(response.content, 'lxml')
        soup = soup.find_all(class_='result-title hdrlnk')
        links = []

        for hit in soup:

            result = []

            title = re.findall(r'>(.*?)<', str(hit))[0].lower()
            url = re.findall(r'href="(.*?)">', str(hit))

            result.append(title)
            result.append(url[0])
            links.append(result)

        return links

    def search(self, posts):

        final_scores = []
        sizes = ['size 53', '53 cm', '53cm', 'size 54', '54 cm', '54cm',
                 'size 55', '55 cm', '55cm', '56 cm', '56cm', 'size 56']

        keywords = ['cannondale', 'trek', 'specialized', 'salsa', 'kona',
                    'giant', 'colnago', 'ktm', '6800', 'ridley', 'khs',
                    'canyon', 'bmc', 'bianchi', 'cervelo', 'pinarello',
                    'soma', 'gt', 'focus', 'fuji', 'gunnar', 'jamis',
                    'kestrel', 'lynskey', 'merida', 'norco', 'orbea',
                    'scott', 'serotta', 'felt', '105', '5800', 'ultegra',
                    'di2', 'dura', 'dura-ace', 'r8000', '170mm', 'gravel',
                    'carbon', 'reynolds', 'columbus', 'titanium', 'stainless',
                    'force', 'sram', 'lemond', 'caadx', 'rove', 'diverge',
                    'checkpoint', 'synapse', '853', 'endurace', 'poprad',
                    'warbird', 'renegade']

        for post in posts:

            missed_links = []

            try:

                k_cheat = ['keywords', 'keyword']
                response = requests.get(post[1])
                link_soup = BeautifulSoup(response.content, 'lxml')

                descrpt = link_soup.find(id='postingbody')
                descrpt = re.findall(r'<\/div>([\s\S]*)</section>',
                                     str(descrpt))[0].strip().lower()
                descrpt = re.sub(r'<[^<]+?>', '', descrpt)
                descrpt = re.sub(r'[\.,:;!?(){}\[\]\\/]', ' ', descrpt)
                descrpt = descrpt.replace('\n', '')

                price = link_soup.find(class_='price')
                price = re.findall(r'\$.*<', str(price))[0][:-1]

                search = post[0] + ' ' + descrpt

                if any(k in descrpt for k in k_cheat):

                    d_split = descrpt.split(' ')

                    for k in k_cheat:

                        try:

                            descrpt = ' '.join(d_split[:d_split.index(k)])

                        except:

                            pass

                if any(size in search for size in sizes):

                    def key_search(keyword):

                        if keyword in descrpt:

                            return 1

                        else:

                            return 0

                    points = sum(map(key_search, keywords))
                    final_scores.append(post + [points, price])

            except Exception as e:

                missed_links.append(post)

        return [sorted(final_scores, key=lambda x: x[2], reverse=True),
                missed_links]


if __name__ == '__main__':

    main()
