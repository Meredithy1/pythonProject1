import requests
from lxml import etree
from datetime import datetime, timedelta


def scrape_guangdong_policy_data(start_date, end_date):
    base_url = "https://www.gd.gov.cn/gkmlpt/policy"

    # 生成日期范围
    date_range = generate_date_range(start_date, end_date)

    # 存储政策信息
    policy_data = []

    for date in date_range:
        url = base_url + date + "/index.html"

        # 发送请求并获取页面内容
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        html = response.text

        # 使用lxml解析页面内容
        parser = etree.HTMLParser()
        tree = etree.fromstring(html, parser)

        # 获取政策信息项，并存储到列表中
        policies = tree.xpath('//div[@class="doc_box"]')

        for policy in policies:
            index = policy.xpath('.//a/span[@class="num"]/text()')[0]
            agency = policy.xpath('.//span[@class="source"]/text()')[0]
            pub_date = policy.xpath('.//span[@class="date"]/text()')[0]
            title = policy.xpath('.//a/h3/text()')[0]
            text = policy.xpath('.//a/p/text()')[0]
            attachment = policy.xpath('.//a/@href')[0]

            # 将政策信息存储到字典中
            policy_info = {
                'index': index,
                'agency': agency,
                'pub_date': pub_date,
                'title': title,
                'text': text,
                'attachment': attachment
            }

            # 将政策信息添加到列表中
            policy_data.append(policy_info)

    return policy_data


# 生成日期范围的函数
def generate_date_range(start_date, end_date):
    date_range = []
    start_dt = datetime.strptime(start_date, '%Y%m%d')
    end_dt = datetime.strptime(end_date, '%Y%m%d')

    current_dt = start_dt
    while current_dt <= end_dt:
        date_range.append(current_dt.strftime('%Y/%m%d'))
        current_dt += timedelta(days=1)

    return date_range


# 输入指定的日期范围
start_date = '20220101'
end_date = '20230601'

# 调用爬虫函数并获取政策信息
policy_data = scrape_guangdong_policy_data(start_date, end_date)

# 输出政策信息
for policy in policy_data:
    print("索引号:", policy['index'])
    print("发布机构:", policy['agency'])
    print("发布日期:", policy['pub_date'])
    print("政策标题:", policy['title'])
    print("政策正文:", policy['text'])
    print("政策附件链接:", policy['attachment'])
    print("------------------------")