from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_tianyancha(username, password):
    # 初始化浏览器
    driver = webdriver.Chrome()  # 这里使用Chrome浏览器，需要下载对应的ChromeDriver并配置路径

    # 打开登录页面
    driver.get('https://www.tianyancha.com/login')

    # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.module.login-module')))

    # 输入用户名和密码
    driver.find_element(By.CSS_SELECTOR, 'input[name="mobile"]').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)

    # 点击登录按钮
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # 等待登录成功，并获取Cookie
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.nav.navbar-nav.navbar-right')))

    # 获取Cookie
    cookies = driver.get_cookies()

    # 关闭浏览器
    driver.quit()

    return cookies

def scrape_company_patents(company_name, cookies):
    # 初始化浏览器，设置Cookie
    driver = webdriver.Chrome()
    for cookie in cookies:
        driver.add_cookie(cookie)

    # 打开公司专利页面
    driver.get(f'https://www.tianyancha.com/search/patent?key={company_name}')

    # 等待专利数据加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.green-pager .ng-binding')))

    # 获取专利数据列表
    patent_elements = driver.find_elements(By.CSS_SELECTOR, '.search_pager .search-block.header+.search-block')

    # 存储专利数据
    patent_data = []
    for element in patent_elements:
        # 提取专利数据
        patent_title = element.find_element(By.CSS_SELECTOR, '.title a').get_attribute('title')
        patent_date = element.find_element(By.CSS_SELECTOR, '.date').text
        patent_number = element.find_element(By.CSS_SELECTOR, '.number').text
        patent_data.append({'title': patent_title, 'date': patent_date, 'number': patent_number})

    # 关闭浏览器
    driver.quit()

    return patent_data


# 输入企业名称和登录信息
company_name = '华为技术有限公司'
username = '17623192750'
password = 'liuchen106'

# 自动登录并获取Cookie
cookies = login_tianyancha(username, password)

# 爬取公司专利数据
patent_data = scrape_company_patents(company_name, cookies)

# 输出专利数据列表
for patent in patent_data:
    print('专利标题:', patent['title'])
    print('专利日期:', patent['date'])
    print('专利编号:', patent['number'])
    print('------------------------')