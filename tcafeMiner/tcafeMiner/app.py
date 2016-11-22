import logging
import requests
import random
from bs4 import BeautifulSoup
from selenium import webdriver

log = logging.getLogger(__name__)

prefixAttendanceGame = "javascript: " \
                        "(function()" \
                        "{" \
                            "var cbInt = 0;" \
                            "cbInt = window.setInterval(function()" \
                            "{" \
                                "if (counter > 0)" \
                                "{" \
                                    "window.clearInterval(cbInt);" \
                                    "cbInt = window.setInterval(function()" \
                                    "{" \
                                        "counter = "

postfixAttendanceGame =                    ";" \
                                        "document.getElementById('btn_stop').click();" \
                                        "window.clearInterval(cbInt);" \
                                    "}, 1);" \
                                "}" \
                                "else" \
                                "{" \
                                    "document.getElementById('btn_start').click();" \
                                    "this.total_count = 0;" \
                                "}" \
                            "}, 100);" \
                            "} )();"

def main():
        log.info('start mining')

        urlTwitter = 'https://twitter.com/tcafenet'

        r = requests.get(urlTwitter)
        soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')

        urlTcafe = 'http://tcafe1.com/'

        rsoup = soup.find("span", {"class": "js-display-url"})

        if rsoup is not None:
                urlTcafe = str(rsoup.previous + rsoup.next).lower()
                log.info('Checked url is : ' + urlTcafe)

        log.info('trying to login...')

        randNum = random.random()
        loginUrl = urlTcafe + '/bbs/login_check.php?' + str(randNum)
        loginUrl = loginUrl + '&mb_id=' + 'algorist' + \
            '&mb_password=' + '0428tkskdl'

        driver = webdriver.PhantomJS('/usr/local/bin/phantomjs')
        driver.get(loginUrl)

        if driver.current_url != str(urlTcafe + '/?udt=1'):
            return 0

        driver.get(str(urlTcafe + '/attendance/attendance.php?3'))

        # 1 : 달인 100 : 능력자
        driver.execute_script(prefixAttendanceGame + '1' + postfixAttendanceGame)

        log.info('end mining')
        return 0
