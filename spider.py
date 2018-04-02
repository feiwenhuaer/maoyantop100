import requests
from requests.exceptions import RequestException
import re
import collections
import json
from multiprocessing import Pool


def get_one_page(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    dic = collections.OrderedDict()
    for item in items:
        dic['index'] = item[0]
        dic['image'] = item[1]
        dic['title'] = item[2]
        dic['actor'] = item[3].strip()[3:]
        dic['time'] = item[4].strip()[5:]
        dic['score'] = item[5] + item[6]
        yield dic


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        # sort_item = sorted(item.items(),key=lambda e:e[0])
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [x * 10 for x in range(10)])
