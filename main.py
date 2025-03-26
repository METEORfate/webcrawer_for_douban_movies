import requests,csv
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

movie_list = []

def main():
    for page in range(0,226,25):
        # 目标url
        url = f'https://movie.douban.com/top250?start={page}&filter='

        # 发送请求, 获取响应
        res = requests.get(url, headers=headers)
        html = res.text
        tree = etree.HTML(html)
        divs = tree.xpath('//div[@class="info"]')
        for div in divs:
            dic = {}
            # 电影中文标题
            dic['电影中文名'] = div.xpath('./div[@class="hd"]/a/span[@class="title"]/text()')[0]
            # 电影英文标题
            dic['电影英文名'] = div.xpath('./div[@class="hd"]/a/span[2]/text()')[0].strip('\xa0/\xa0')
            # 电影详情页链接
            dic['电影详情页链接'] = div.xpath('./div[@class="hd"]/a/@href')[0]
            # 导演
            dic['导演'] = div.xpath('./div[@class="bd"]/p/text()')[0].strip().split('导演: ')[1].split('主演: ')[0]
            # 主演
            try:
                act = div.xpath('./div[@class="bd"]/p/text()')[0].strip().split('导演: ')[1].split('主演: ')[1]
            except IndexError as e:
                print(end='')
            dic['主演'] = act
            # 上映年份
            dic['上映年份'] =  div.xpath('./div[@class="bd"]/p/text()')[1].strip().split('/')[0]
            # 国籍
            nationality = div.xpath('./div[@class="bd"]/p/text()')[1].strip().split('/')[1].strip()
            if len(nationality[0].encode('utf-8')) == 1:
                nationality = div.xpath('./div[@class="bd"]/p/text()')[1].strip().split('/')[2].strip()
            else:
                nationality = div.xpath('./div[@class="bd"]/p/text()')[1].strip().split('/')[1].strip()
            # print(nationality)
            dic['国籍'] = nationality
            # 类型
            genre = div.xpath('./div[@class="bd"]/p/text()')[1].strip().split('/')[2].strip()
            if len(div.xpath('./div[@class="bd"]/p/text()')[1].strip().split('/')[1].strip()[0].encode('utf-8')) == 1:
                genre = div.xpath('./div[@class="bd"]/p/text()')[1].strip().split('/')[3].strip()
            else:
                genre = div.xpath('./div[@class="bd"]/p/text()')[1].strip().split('/')[2].strip()
            dic['类型'] = genre
            # 评分 
            dic['评分'] = div.xpath('./div[@class="bd"]/div/span[2]/text()')[0]
            # 评分人数
            dic['评分人数'] = div.xpath('./div[@class="bd"]/div/span[4]/text()')[0]
            movie_list.append(dic)
            # print(len(moive_list))  # 检查数据是否全部爬取成功
        print(f'----------------------第{int(page/25+1)}页爬取完成--------------------------------------')
    print('-----------------------爬虫结束-------------------------------')
    # 数据保存
    with open('豆瓣电影Top250.csv', 'w', encoding='utf-8-sig', newline='') as f:
        # 1. 创建对象
        writer = csv.DictWriter(f, fieldnames=('电影中文名', '电影英文名', '电影详情页链接', '导演', '主演', '上映年份', '国籍', '类型', '评分', '评分人数'))
        # 2. 写入表头
        writer.writeheader()
        # 3. 写入数据
        writer.writerows(movie_list)
if __name__ == '__main__':
    main()