# Intagram_Crawler

This crawler fork from [ins-crawler](https://github.com/huaying/ins-crawler) and doing some changed. If you encounter any problems, please used the origin version.

1. Get Instagram posts/profile/hashtag data without using Instagram API. `crawler.py`

1. Make sure you have Chrome browser installed.
2. Download [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) and put it into bin folder: `./inscrawler/bin/chromedriver`
3. Install Selenium: `pip install -r requirements.txt`
4. `cp inscrawler/secret.py.dist inscrawler/secret.py`

### configure
```sh
./storage/__init__.py      # setting storage URL.
./inscrawler/secret.py     # setting login ID and password.
```
### Usage
```sh
positional arguments:
  mode                  options: [posts, profile, hashtag]

optional arguments:
  -h, --help                        # show this help message and exit.
  -tn NUMBER, --number NUMBER       # number of returned tags.
  -pn NUMBER, --number NUMBER       # number of returned posts.
  -u USERNAME, --username USERNAME  # instagram's username.
  -t TAG, --tag TAG                 # instagram's tag name.
  -o OUTPUT, --output OUTPUT        # output file name(json format).
```

### Example
```
python crawler.py posts -u cal_foodie -n 100 -o ./output
python crawler.py profile -u cal_foodie -o ./output
python crawler.py hashtag -t taiwan -o ./output
python crawler.py poststag -t TAG -tn 100 -pn 100
```
1. Return default 100 hashtag posts(mode: hashtag) and all user's posts(mode: posts) if not specifying the number of post `-n`, `--number`.
2. Save the result in storage if not specifying the output path of post `-o`, `--output`.
3. It takes much longer to get data if the post number is over about 1000 since Instagram has set up the rate limit for data request.
4. Don't use this repo crawler Instagram if the user has more than 10000 posts.

