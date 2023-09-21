import requests
import re
import execjs
import pymysql
import time
def save_to_mysql(data):
    # 连接数据库
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='db')
    # 创建游标对象
    cursor = conn.cursor()
    # 定义 SQL 语句
    insert_sql = "INSERT INTO job VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # 批量插入数据
    cursor.executemany(insert_sql, data)
    # 提交
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

def get_acw_sc__v2(arg1):
    with open("test_ok.js", "r") as f:
        js_code = f.read()
    return execjs.compile(js_code).call("acw_sc__v2",arg1)


# 7 * 1000
headers = {
}
cookies = {
 }
url = "https://we.51job.com/api/job/search-pc"
keyword_list = ['python','java','go',"c","c++","php","android"]
items_list = []
for keyword in keyword_list:
    print(f"{keyword}---crawl")
    params = {
        "api_key": "51job",
        "timestamp": str(int(time.time())),
        "keyword": keyword,
        "searchType": "2",
        "function": "",
        "industry": "",
        "jobArea": "000000",
        "jobArea2": "",
        "landmark": "",
        "metro": "",
        "salary": "",
        "workYear": "",
        "degree": "",
        "companyType": "",
        "companySize": "",
        "jobType": "",
        "issueDate": "",
        "sortType": "0",
        "pageNum": "1",
        "requestId": "2858f2ed1c9486461fe77d5d40cd0a01",
        "pageSize": "1000",
        "source": "1",
        "accountId": "202084973",
        "pageCode": "sou|sou|soulb"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    while "acw_sc__v2" in response.text:
        arg1 = re.findall("var arg1='(.*?)'", response.text)[0]
        acw_sc__v2 = get_acw_sc__v2(arg1)
        cookies.update({"acw_sc__v2":acw_sc__v2})
        print("acw_sc__v2:",acw_sc__v2)
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        # print(response.text)
        time.sleep(0.5)
    items = response.json()['resultbody']['job']['items']
    # field = ['职位','公司','薪资', '城市','经验','学历','公司性质','公司规模','公司领域','标签','职位详情页','公司详情页']
    for item in items:
        item_tuple = (
            item['jobName'],
            item['fullCompanyName'],
            item['provideSalaryString'],
            item['jobAreaString'],
            item['workYearString'],
            item['degreeString'],
            item['companyTypeString'],
            item['companySizeString'],
            item['industryType1Str'],
            ','.join(item['jobTags']),
            item['jobHref'],
            item['companyHref']
        )
        items_list.append(item_tuple)
print("spider finished")
save_to_mysql(items_list)
print("all finished")

