
from message import Message
from scrape import Scrape
from filter import Filter, Keywords


def main():

    distance = '30'
    zip_ = '80223'
    min_price = '300'
    max_price = '1500'
    has_pic = '1'  # 0 to disable
    bundle = '1'  # 0 to disable

    main_search = 'https://denver.craigslist.org/search/bia?h\
asPic={}&bundleDuplicates={}&search_distance={}&postal={}&min_price=\
{}&max_price={}'.format(has_pic, bundle, distance, zip_, min_price, max_price)

    post_list = Scrape.scrape_search_pg(main_search)
    results = []

    for post in post_list:

        post_Obj = Filter(post[0])
        result = Filter.quick_filter(post_Obj)

        if result:

            result = Filter.size_filter(post_Obj)

            if result:

                results.append(Keywords.score(post_Obj,
                               Keywords.find(post_Obj)))

    if len(results) > 0:

        results = sorted(results, key=lambda x: x[2], reverse=True)
        Message.send(Message.format(results))


if __name__ == '__main__':

    main()
