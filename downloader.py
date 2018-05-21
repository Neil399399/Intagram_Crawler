# coding=UTF-8
from urllib.request import urlretrieve
from storage.solr import search
import sys
import os
import argparse

def usage():
    return '''
        python3 download.py user -s solr -u userID -o output_dir
        python3 download.py tag -s solr -t tag -o output_dir
    '''
# arg.
def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()

# get data from storage.
def get_data(storage,mode,key,number):
    if storage == 'solr':            
        return search(mode,key,number)
    else:
        print('No this storage/Data.')

# download image.
def download_img(search_result,output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    num = 0
    for data in search_result:
        num +=1
        try:
            urlretrieve(data['img_url_str'][0],output_dir+'/'+data['post_owner_str'][0]+'_'+str(num)+'.jpg')
        except:
            continue
    print('Finished download.')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Instagram Downloader',usage=usage())
    parser.add_argument('mode',help='options: [user, tag]')
    parser.add_argument('-s', '--storage',help='Storage.')
    parser.add_argument('-d', '--download',help='what you want download.')
    parser.add_argument('-u', '--userID',help='Instagram userID in storage.')
    parser.add_argument('-t', '--tag',help='Instagram tag in storage.')
    parser.add_argument('-n', '--number',type=int,help='number of the data you want take.')
    parser.add_argument('-o', '--output',help='output folder.')

    args = parser.parse_args()

    if args.mode == 'user':
        arg_required('userID')
        arg_required('download')
        if args.download == 'image':
            download_img(get_data(args.storage,'post_owner_str',args.userID,args.number),args.output)
    elif args.mode == 'tag':
        arg_required('tag')
        arg_required('download')
        if args.download == 'image':
            download_img(get_data(args.storage,'tag_str',args.tag,args.number),args.output)
    else:
        usage()
