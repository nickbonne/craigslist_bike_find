
from scrape import Scrape
from nltk.tokenize import word_tokenize


def main():

    pass


class Filter:

    brands = ['bianchi', 'bmc', 'cannondale', 'canyon', 'cervelo',
              'colnago', 'felt', 'focus', 'fuji', 'giant', 'gt',
              'gunnar', 'jamis', 'kestrel', 'khs', 'kona', 'ktm',
              'lemond', 'lynskey', 'merida', 'niner', 'norco',
              'orbea', 'pinarello', 'ridley', 'salsa', 'scott',
              'serotta', 'soma', 'specialized', 'trek']

    models = ['caadx', 'cadd10', 'caad12', 'checkpoint', 'diverge',
              'endurace', 'poprad', 'renegade', 'roubaix', 'rove',
              'synapse', 'vaya', 'warbird']

    others = ['105', '170mm', '5800', '6800', '853', 'caad', 'carbon',
              'columbus', 'di2', 'dura-ace', 'force', 'r8000',
              'reynolds', 'sram', 'titanium', 'ultegra']

    sizes = ['size53', '53 cm', '53cm', 'size54', '54 cm', '54cm',
             'size55', '55 cm', '55cm', '56 cm', '56cm', 'size56']

    keys = brands + models + others
    all_ = brands + models + sizes + others

    bad = ['women', 'women\'s', 'kids', 'youth', 'mtb', 'triathlon',
                    '29er', '29in', '29\"', '26in']

    def __init__(self, post):

        self.post = post

        self.title = str(post[0])
        self.url = str(post[1])
        self.size = ''
        self.price = ''
        self.item = ''
        self.score = 0

    # weeds out junk posts and adds price attribute to passing posts
    def quick_filter(self):

        title = word_tokenize(self.title)

        if set(title) & set(Filter.all_) and \
           not set(title) & set(Filter.bad):

            item_info = Scrape.scrape_post_pg(self.url)
            self.price = item_info[1]
            self.post = self.post + list(item_info)
            self.size = item_info[2]

            return self

    # only returns posts with a token that matches a Filter.size
    # self.item set to tokenized list for keyword search if size token match
    def size_filter(self):

        item_descrpt = word_tokenize(self.post[2])

        size = set(item_descrpt) & set(Filter.sizes)

        if self.size != '':

            pass

        else:

            try:

                self.size = list(size)[0]

            except:

                pass

        if set(Filter.sizes) & set([self.size]):

            self.item = item_descrpt

            return self


class Keywords(Filter):

    def find(self):

        title_hits = list(set(word_tokenize(self.title)) & set(Filter.keys))
        descrpt_hits = list((set(self.item) & set(Filter.keys)) -
                            set(title_hits))

        return [title_hits, descrpt_hits]

    def score(self, key_counts):

        title_score = 2 * len(key_counts[0])
        descrpt__score = len(key_counts[1])

        self.score = title_score + descrpt__score

        return [self.title, self.url, self.score, self.price]


if __name__ == '__main__':

    main()
