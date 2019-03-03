from    selenium import webdriver
from    bs4 import BeautifulSoup
import  time, os, sys
from    datetime import datetime
import  logging

log_format = '%(asctime)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format=log_format, datefmt='%m/%d %I:%M:%S %p')
fh = logging.FileHandler(os.path.join('.', 'log.txt'))
fh.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(fh)

urls = ["https://study.163.com/course/introduction/1208894818.htm",
        'https://study.163.com/course/introduction/1006498024.htm',
        'https://study.163.com/course/introduction/1003590004.htm',
        'https://study.163.com/course/introduction/1003599014.htm',
        'https://study.163.com/course/introduction/1208943817.htm',
        'https://study.163.com/course/introduction/1005781015.htm',
        'https://study.163.com/course/introduction/1005695008.htm',
        'https://study.163.com/course/introduction/1003606092.htm',
        'https://study.163.com/course/introduction/1005214052.htm'
        ]

options = webdriver.ChromeOptions()
options.add_argument("headless")


data = dict()


while True:

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    
    for url in urls:

        try:
            courseid = url.split('/')[-1].split('.')[0]

            driver.get(url)

            soup=BeautifulSoup(driver.page_source, 'lxml')
            # print(soup.prettify())


            res = soup.find('div', class_='u-courseHead').find('div', class_='u-coursetitle f-fl')

            num = int(''.join(filter(str.isdigit, res.div.span.string)))
            title = res.h2.span.string


            try:
                delta = num - data[courseid]
                data[courseid] = num
            except KeyError as err:
                print(err, 'KeyError')
                data[courseid] = 0
                # print(data.keys())
                delta = 0

            if delta > 0:
                logging.info("%s: %d\t%d\t%s", courseid, num, delta, title)



        except (AttributeError,ValueError) as err:
            print(err, 'url:', url)





    # free up memory
    driver.close()
    driver.quit()
    time.sleep(60*10)