# coding=UTF-8
from selenium.webdriver.common.keys import Keys
from .browser import Browser
from .utils import instagram_int
from .utils import retry
from .utils import randmized_sleep
from . import secret
from time import sleep, time
from config import user_name,user_desc,user_photo,user_statistics,posts_class_name,each_post_class_name,user_ID_class_name
from config import version


class InsCrawler:
    URL = 'https://www.instagram.com'
    RETRY_LIMIT = 10

    def __init__(self, has_screen=False):
        self.browser = Browser(has_screen,version)
        self.page_height = 0

    def login(self):
        browser = self.browser
        url = '%s/accounts/login/' % (InsCrawler.URL)
        browser.get(url)

        u_input = browser.find_one('input[name="username"]')
        u_input.send_keys(secret.username)
        p_input = browser.find_one('input[name="password"]')
        p_input.send_keys(secret.password)
        p_input.send_keys(Keys.RETURN)

        @retry()
        def check_login():
            if browser.find_one('input[name="username"]'):
                raise Exception()

        check_login()

    def get_user_profile(self, username):
        print('Check user profile ... ')
        browser = self.browser
        url = '%s/%s/' % (InsCrawler.URL, username)
        browser.get(url)
        try:
            name = browser.find_one(user_name)
            desc = browser.find_one(user_desc)
            photo = browser.find_one(user_photo)
            statistics = [ele.text for ele in browser.find(user_statistics)]
            post_num, follower_num, following_num = statistics
            return {
                'name': name.text,
                'desc': desc.text if desc else None,
                'photo_url': photo.get_attribute('src'),
                'post_num': post_num,
                'follower_num': follower_num,
                'following_num': following_num
            }
        except:
            return 'No found'

    def get_user_posts(self, tag, username, number=None):
        user_profile = self.get_user_profile(username)
        if user_profile != 'No found':
            if not number:
                number = instagram_int(user_profile['post_num'])
            return self._get_posts(tag,number,username)

    def get_latest_posts_by_tag(self, tag, num):
        url = '%s/explore/tags/%s/' % (InsCrawler.URL, tag)
        self.browser.get(url)
        return self._get_tag(num)

    def get_user_posts_from_tag(self, tag, num):
        url = '%s/explore/tags/%s/' % (InsCrawler.URL, tag)
        self.browser.get(url)
        user_list = self._get_all_tags_owner(num,tag)
        return user_list

    def auto_like(self, tag='', maximum=1000):
        self.login()
        browser = self.browser
        if tag:
            url = '%s/explore/tags/%s/' % (InsCrawler.URL, tag)
        else:
            url = '%s/explore/' % (InsCrawler.URL)
        self.browser.get(url)
        ele_posts = browser.find_one('._mck9w a')
        ele_posts.click()

        for _ in range(maximum):
            heart = browser.find_one('._8scx2.coreSpriteHeartOpen')
            if heart:
                heart.click()
                randmized_sleep(2)

            left_arrow = browser.find_one('.coreSpriteRightPaginationArrow')
            if left_arrow:
                left_arrow.click()
                randmized_sleep(2)
            else:
                break

    def _get_posts(self,tag, num, username):
        '''
            To get posts, we have to click on the load more
            button and make the browser call post api.
        '''
        TIMEOUT = 30
        browser = self.browser
        dict_posts = {}
        pre_post_num = 0
        wait_time = 1

        def start_fetching(pre_post_num, wait_time):
            ele_posts = browser.find(posts_class_name)
            Id = 0
            for ele in ele_posts:
                Id +=1
                key = ele.get_attribute('href')
                if key not in dict_posts:
                    try:
                        ele_img = browser.find_one(each_post_class_name, ele)
                        content = ele_img.get_attribute('alt')
                        img_url = ele_img.get_attribute('src')
                        dict_posts[key] = {
                            'id': str(tag)+'-'+username+'-'+str(Id),
                            'tag': str(tag),
                            'post_owner':username,
                            'content': content,
                            'img_url': img_url
                        }
                    except:
                        continue

            if pre_post_num == len(dict_posts):
                print('Number of fetched posts: %s' % pre_post_num)
                print('Wait for %s sec...' % (wait_time))
                sleep(wait_time)
                wait_time *= 2
                browser.scroll_up(300)
            else:
                wait_time = 1

            pre_post_num = len(dict_posts)
            browser.scroll_down()

            return pre_post_num, wait_time

        print('Starting fetching userID: '+username+' ...')
        while len(dict_posts) < num and wait_time < TIMEOUT:
            pre_post_num, wait_time = start_fetching(pre_post_num, wait_time)


            loading = browser.find_one('._anzsd._o5uzb')
            if (not loading and wait_time > TIMEOUT/2):
                break

        posts = list(dict_posts.values())
        print('Done. Fetched %s posts.' % len(posts))
        return posts[:num]

    def _get_tag(self, num):
        '''
            To get tags, we have to click on the load more
            button and make the browser call post api.
        '''
        Start_time = time()
        TIMEOUT = 600
        browser = self.browser
        dict_posts = {}
        pre_post_num = 0
        wait_time = 1

        def start_fetching(pre_post_num, wait_time):
            ele_posts = browser.find(posts_class_name)
            for ele in ele_posts:
                key = ele.get_attribute('href')
                if key not in dict_posts:
                    ele_img = browser.find_one(each_post_class_name, ele)
                    content = ele_img.get_attribute('alt')
                    img_url = ele_img.get_attribute('src')
                    dict_posts[key] = {
                        'post_owner':'',
                        'content': content,
                        'img_url': img_url
                    }

            if pre_post_num == len(dict_posts):
                print('Number of fetched posts: %s' % pre_post_num)
                print('Wait for %s sec...' % (wait_time))
                sleep(wait_time)
                wait_time *= 2
                browser.scroll_up(300)
            else:
                wait_time = 1

            pre_post_num = len(dict_posts)
            browser.scroll_down()
            return pre_post_num, wait_time

        print('Strating fetching...')
        while len(dict_posts) < num and wait_time < TIMEOUT:
            pre_post_num, wait_time = start_fetching(pre_post_num, wait_time)

            loading = browser.find_one('._anzsd._o5uzb')
            if (not loading and wait_time > TIMEOUT/2):
                break


        # connect to href url and get post owner.
        for key in dict_posts:
            browser.get(key)
            post_owner = browser.find_one(user_ID_class_name)
            ID = post_owner.get_attribute('title')
            dict_posts[key]['post_owner'] = ID
        browser.scroll_down()

        posts = list(dict_posts.values())
        print('Done. Fetched %s posts.' % (min(len(posts), num)))
        print('Running time:',time()-Start_time)
        return posts[:num]

    # get all user ID who used this tag.
    def _get_all_tags_owner(self, num, tag):
        '''
            To get all post_owner who used this tag, we have to click on the load more
            button and make the browser call post api.
        '''
        Start_time = time()
        TIMEOUT = 600
        browser = self.browser
        all_tag_url = []
        all_post_owner = []
        pre_post_num = 0
        wait_time = 1

        def start_fetching(pre_post_num, wait_time):
            ele_posts = browser.find(posts_class_name)
            if len(ele_posts)==0:
                print("Didn't find any elements in web page.")
                return pre_post_num,wait_time

            for ele in ele_posts:
                key = ele.get_attribute('href')
                if key not in all_tag_url:
                    all_tag_url.append(key)

            if pre_post_num == len(all_tag_url):
                print('Number of fetched posts: %s' % pre_post_num)
                print('Wait for %s sec...' % (wait_time))
                sleep(wait_time)
                wait_time *= 2
                browser.scroll_up(300)
            else:
                wait_time = 1

            pre_post_num = len(all_tag_url)
            browser.scroll_down()
            return pre_post_num, wait_time

        print('Starting fetching ... tag '+tag)
        while len(all_tag_url) < num and wait_time < TIMEOUT:
            pre_post_num, wait_time = start_fetching(pre_post_num, wait_time)

            loading = browser.find_one('._anzsd._o5uzb')
            if (not loading and wait_time > TIMEOUT/2):
                break


        # connect to href url and get post owner.
        for url in all_tag_url:
            browser.get(url)
            try:
                post_owner = browser.find_one(user_ID_class_name)
                ID = post_owner.get_attribute('title')
                if ID not in all_post_owner:
                    all_post_owner.append(ID)
            except:
                continue
        browser.scroll_down()

        print('Done. Fetched %s IDs.' % (min(len(all_post_owner), num)))
        print('Running time:',time()-Start_time)
        return all_post_owner
