
from message import Message
from scrape import Scrape


def main():

    distance = '50'
    zip_ = '80223'
    min_price = '300'
    max_price = '1200'
    has_pic = '1'  # 0 to disable
    bundle = '1'  # 0 to disable

    main_search = 'https://denver.craigslist.org/search/bia?h\
asPic={}&bundleDuplicates={}&search_distance={}&postal={}&min_price=\
{}&max_price={}'.format(has_pic, bundle, distance, zip_, min_price, max_price)

    post_list = Scrape.scrape(Scrape(), main_search)
    scored_posts = Scrape.search(Scrape(), post_list)
    ranked_matches = scored_posts[0]
    missed_posts = scored_posts[1]
    formatted_matches = Message.format(ranked_matches)

    if len(missed_posts) > 0:

        formatted_misses = Message._format_miss(missed_posts)
        formatted_matches = formatted_matches + formatted_misses

    Message.send(formatted_matches)

if __name__ == '__main__':

    main()
