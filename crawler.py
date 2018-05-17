from inscrawler import InsCrawler
import sys
import argparse
import json
from io import open
from storage.solr import writer


def usage():
    return '''
        python crawler.py posts -u cal_foodie -n 100 -o ./output
        python crawler.py profile -u cal_foodie -o ./output
        python crawler.py hashtag -t taiwan -o ./output

        The default number for fetching posts via hashtag is 100.
    '''


def get_posts_by_user(tag, username, number):
    ins_crawler = InsCrawler()
    return ins_crawler.get_user_posts(tag, username, number)


def get_profile(username):
    ins_crawler = InsCrawler()
    return ins_crawler.get_user_profile(username)


def get_posts_by_hashtag(tag, number):
    ins_crawler = InsCrawler()
    return ins_crawler.get_latest_posts_by_tag(tag, number)

# get user post from lateset tag.
def get_user_posts_by_tags(tag, number):
    ins_crawler = InsCrawler()
    return ins_crawler.get_user_posts_from_tag(tag, number)

def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()


def output(data, filepath):
    out = json.dumps(data, ensure_ascii=False)
    if filepath:
        with open(filepath, 'w') as f:
            f.write(out)
    else:
        print(out)

# save in solr.
def save_in_solr(data):
    print('Save in solr ...')
    print(writer(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Instagram Crawler',
                                     usage=usage())
    parser.add_argument('mode',
                        help='options: [posts, profile, hashtag]')
    parser.add_argument('-pn', '--postNumber',
                        type=int,
                        help='number of returned posts')
    parser.add_argument('-tn', '--tagNumber',
                        type=int,
                        help='number of returned tags')
    parser.add_argument('-u', '--username',
                        help='instagram\'s username')
    parser.add_argument('-t', '--tag',
                        help='instagram\'s tag name')
    parser.add_argument('-o', '--output', help='output file name(json format)')
    parser.add_argument('-s', '--solr', help='save output in solr stroage.')
    args = parser.parse_args()

    if args.mode == 'posts':
        arg_required('username')
        output(get_posts_by_user(None,args.username, args.number), args.output)
    elif args.mode == 'profile':
        arg_required('username')
        output(get_profile(args.username), args.output)
    elif args.mode == 'hashtag':
        arg_required('tag')
        output(
            get_posts_by_hashtag(args.tag, args.tagNumber or 100),args.output)
    elif args.mode == 'poststag':
        arg_required('tag')
        user_list = get_user_posts_by_tags(args.tag, args.tagNumber or 100)
        for userID in user_list:
            save_in_solr(get_posts_by_user(args.tag,userID,args.postNumber))
    else:
        usage()
