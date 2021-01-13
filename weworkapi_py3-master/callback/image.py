from selenium import webdriver
import os

# driver = webdriver.PhantomJS(executable_path=r'D:\Python\Python37\Scripts\phantomjs.exe')
# driver = webdriver.chrome(executable_path=r'D:\Python\Python37\Scripts\chromedriver.exe')
driver=webdriver.Chrome()
# urls = open("urls.txt")
# for url in urls:
#     driver.get(url)
url = 'http://192.168.191.128:3000/grafana/'
driver.get(url)
content = driver.page_source
print(content)
driver.save_screenshot(str(hash(url)) + '.png')

driver.close()