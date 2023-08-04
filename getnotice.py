from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as parse
from datetime import datetime, timedelta
import re
import sqlite3

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "threem.settings")
django.setup()
from notices.models import Notice


def get_notices():
    # 공지사항 메인 주소
    announce = "http://www.jbnu.ac.kr/kor/?menuID=139"
    sfv = parse.urlencode({ "sfv": "subject" })
    pno = lambda no : parse.urlencode({ "pno": no })

    # 현재 학기 공지만 가져오기 위한 구분자 생성
    sep = (datetime(datetime.now().year, 1, 1) - timedelta(days=1)).date()
    print(sep) # 올해 2월 말일
    
    # 공지사항 목록
    notices = []
#================================================================================================================
    def get_big_context(notices):
        sfv_memo = parse.urlencode({ "sfv": "memo" }) #수정
        bigperson = parse.urlencode({ "memo": "큰사람" })
        bigpersonsearch = announce + "&" + bigperson + "&" + sfv_memo
        no = 1 # 페이지 인덱스
        flag = 0 # 중단 깃발

        tr_list = []

        #큰사람
        while (True):
            url = bigpersonsearch + "&" + pno(no) # 페이지 주소
            res_big = req.urlopen(url)
            big_soup = BeautifulSoup(res_big, 'html.parser')

            i = 1 # 항목 인덱스
            while (True):
                # tr 하나가 공지 항목 하나
                # 등록 날짜 가져오기 - 큰사람과 벨트 모두 5번째 td에서 날짜 나옴.
                date = datetime.strptime(big_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ") > td:nth-of-type(5)").string, "%Y.%m.%d").date()

                # 올해 3월에 생성된 공지를 넘어가면
                if (date < sep):
                    flag = 1 # 중단 깃발 세우기
                    break

                tr_list.append(big_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ")"))

                # 다음 항목으로 넘어가기
                i = i + 1
                # 한 페이지에 9개의 항목이 존재 -> 이번 페이지 출력 종료
                if (i == 10):
                    break

            # 깃발이 세워졌으면 출력 종료
            if (flag == 1):
                break
    
            # 페이지 넘기기
            no = no + 1

        # 정규식으로 벨트 필수 항목 걸러내기
        for tr in tr_list:
            name = tr.select_one("td.left > span > a").get_text().strip()
            date = tr.select_one("td:nth-of-type(5)").string
            href = "https://www.jbnu.ac.kr/kor/" + tr.select_one("td.left > span > a").attrs['href']
            id = tr.select_one("th").string
            if (re.compile("화이트|white|옐로우|yellow|블루|blue|레드|red|블랙|black|큰사람|belt|벨트", re.IGNORECASE).search(name) == None):
                notice = { "_id": id, "name": name, "link": href, "belt": "NO", "date": date }
                notices.append(notice)
#=================================================================================================================
    def get_big(notices):
        bigperson = parse.urlencode({ "subject": "큰사람" })
        bigpersonsearch = announce + "&" + bigperson + "&" + sfv
        no = 1 # 페이지 인덱스
        flag = 0 # 중단 깃발

        tr_list = []

        #큰사람
        while (True):
            url = bigpersonsearch + "&" + pno(no) # 페이지 주소
            res_big = req.urlopen(url)
            big_soup = BeautifulSoup(res_big, 'html.parser')

            i = 1 # 항목 인덱스
            while (True):
                # tr 하나가 공지 항목 하나
                # 등록 날짜 가져오기 - 큰사람과 벨트 모두 5번째 td에서 날짜 나옴.
                date = datetime.strptime(big_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ") > td:nth-of-type(5)").string, "%Y.%m.%d").date()

                # 올해 3월에 생성된 공지를 넘어가면
                if (date < sep):
                    flag = 1 # 중단 깃발 세우기
                    break

                tr_list.append(big_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ")"))

                # 다음 항목으로 넘어가기
                i = i + 1
                # 한 페이지에 9개의 항목이 존재 -> 이번 페이지 출력 종료
                if (i == 10):
                    break

            # 깃발이 세워졌으면 출력 종료
            if (flag == 1):
                break
    
            # 페이지 넘기기
            no = no + 1

        # 정규식으로 벨트 필수 항목 걸러내기
        for tr in tr_list:
            name = tr.select_one("td.left > span > a").get_text().strip()
            date = tr.select_one("td:nth-of-type(5)").string
            href = "https://www.jbnu.ac.kr/kor/" + tr.select_one("td.left > span > a").attrs['href']
            id = tr.select_one("th").string
            if (re.compile("화이트|white|옐로우|yellow|블루|blue|레드|red|블랙|black", re.IGNORECASE).search(name) == None):
                notice = { "_id": id, "name": name, "link": href, "belt": "NO", "date": date }
                notices.append(notice)
#==============================================================================================================================
    def get_white(notices):
        white = parse.urlencode({"subject": "white"})
        whitesearch = announce + "&" + white + "&" + sfv
        no = 1 # 페이지 인덱스
        flag = 0 # 중단 깃발

        tr_list = []

        #큰사람
        while (True):
            wurl = whitesearch + "&" + pno(no) 
            res_white = req.urlopen(wurl)
            white_soup = BeautifulSoup(res_white, 'html.parser')

            i = 1 # 항목 인덱스
            while (True):
                # tr 하나가 공지 항목 하나
                # 등록 날짜 가져오기 - 큰사람과 벨트 모두 5번째 td에서 날짜 나옴.
                date = datetime.strptime(white_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ") > td:nth-of-type(5)").string, "%Y.%m.%d").date()

                # 올해 3월에 생성된 공지를 넘어가면
                if (date < sep):
                    flag = 1 # 중단 깃발 세우기
                    break

                tr_list.append(white_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ")"))

                # 다음 항목으로 넘어가기
                i = i + 1
                # 한 페이지에 9개의 항목이 존재 -> 이번 페이지 출력 종료
                if (i == 10):
                    break

            # 깃발이 세워졌으면 출력 종료
            if (flag == 1):
                break

            # 페이지 넘기기
            no = no + 1

        # 정규식으로 벨트 필수 항목 걸러내기 -> white로 바꿔줘야함. 
        for tr in tr_list:
            name = tr.select_one("td.left > span > a").get_text().strip()
            date = tr.select_one("td:nth-of-type(5)").string
            href = "https://www.jbnu.ac.kr/kor/" + tr.select_one("td.left > span > a").attrs['href']
            id = tr.select_one("th").string
            if (re.compile("벨트|belt", re.IGNORECASE).search(name)):
                notice = { "_id": id, "name": name, "link": href, "belt": "WHITE", "date": date }
                notices.append(notice)
#==============================================================================================================================
    def get_yellow(notices):
        yellow = parse.urlencode({"subject": "yellow"})
        yellowsearch = announce + "&" + yellow + "&" + sfv
        no = 1 # 페이지 인덱스
        flag = 0 # 중단 깃발

        tr_list = []

        #큰사람
        while (True):
            yurl = yellowsearch + "&" + pno(no) 
            res_yellow = req.urlopen(yurl)
            yellow_soup = BeautifulSoup(res_yellow, 'html.parser')

            i = 1 # 항목 인덱스
            while (True):
                # tr 하나가 공지 항목 하나
                # 등록 날짜 가져오기 - 큰사람과 벨트 모두 5번째 td에서 날짜 나옴.
                date = datetime.strptime(yellow_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ") > td:nth-of-type(5)").string, "%Y.%m.%d").date()

                # 올해 3월에 생성된 공지를 넘어가면
                if (date < sep):
                    flag = 1 # 중단 깃발 세우기
                    break

                tr_list.append(yellow_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ")"))

                # 다음 항목으로 넘어가기
                i = i + 1
                # 한 페이지에 9개의 항목이 존재 -> 이번 페이지 출력 종료
                if (i == 10):
                    break

            # 깃발이 세워졌으면 출력 종료
            if (flag == 1):
                break

            # 페이지 넘기기
            no = no + 1

        # 정규식으로 벨트 필수 항목 걸러내기 -> yellow로 바꿔줘야함. 
        for tr in tr_list:
            name = tr.select_one("td.left > span > a").get_text().strip()
            date = tr.select_one("td:nth-of-type(5)").string
            href = "https://www.jbnu.ac.kr/kor/" + tr.select_one("td.left > span > a").attrs['href']
            id = tr.select_one("th").string
            if (re.compile("벨트|belt", re.IGNORECASE).search(name)):
                notice = { "_id": id, "name": name, "link": href, "belt": "YELLOW", "date": date }
                notices.append(notice)
#==============================================================================================================================
    def get_blue(notices):
        blue = parse.urlencode({"subject": "blue"})
        bluesearch = announce + "&" + blue + "&" + sfv
        no = 1 # 페이지 인덱스
        flag = 0 # 중단 깃발

        tr_list = []

        #큰사람
        while (True):
            burl = bluesearch + "&" + pno(no) 
            res_blue = req.urlopen(burl)
            blue_soup = BeautifulSoup(res_blue, 'html.parser')

        
            i = 1 # 항목 인덱스
            while (True):
                # tr 하나가 공지 항목 하나
                # 등록 날짜 가져오기 - 큰사람과 벨트 모두 5번째 td에서 날짜 나옴.
                date = datetime.strptime(blue_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ") > td:nth-of-type(5)").string, "%Y.%m.%d").date()

                # 올해 3월에 생성된 공지를 넘어가면
                if (date < sep):
                    flag = 1 # 중단 깃발 세우기
                    break

                tr_list.append(blue_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ")"))

                # 다음 항목으로 넘어가기
                i = i + 1
                # 한 페이지에 9개의 항목이 존재 -> 이번 페이지 출력 종료
                if (i == 10):
                    break

            # 깃발이 세워졌으면 출력 종료
            if (flag == 1):
                break

            # 페이지 넘기기
            no = no + 1

        # 정규식으로 벨트 필수 항목 걸러내기 -> blue로 바꿔줘야함. 
        for tr in tr_list:
            name = tr.select_one("td.left > span > a").get_text().strip()
            date = tr.select_one("td:nth-of-type(5)").string
            href = "https://www.jbnu.ac.kr/kor/" + tr.select_one("td.left > span > a").attrs['href']
            id = tr.select_one("th").string
            if (re.compile("벨트|belt", re.IGNORECASE).search(name)):
                notice = { "_id": id, "name": name, "link": href, "belt": "BLUE", "date": date }
                notices.append(notice)
#==============================================================================================================================
    def get_red(notices):
        red = parse.urlencode({"subject": "red"})
        redsearch = announce + "&" + red + "&" + sfv
        no = 1 # 페이지 인덱스
        flag = 0 # 중단 깃발

        tr_list = []

        #큰사람
        while (True):
            rurl = redsearch + "&" + pno(no)  
            res_red = req.urlopen(rurl)
            red_soup = BeautifulSoup(res_red, 'html.parser')

        
            i = 1 # 항목 인덱스
            while (True):
                # tr 하나가 공지 항목 하나
                # 등록 날짜 가져오기 - 큰사람과 벨트 모두 5번째 td에서 날짜 나옴.
                date = datetime.strptime(red_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ") > td:nth-of-type(5)").string, "%Y.%m.%d").date()

                # 올해 3월에 생성된 공지를 넘어가면
                if (date < sep):
                    flag = 1 # 중단 깃발 세우기
                    break

                tr_list.append(red_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ")"))

                # 다음 항목으로 넘어가기
                i = i + 1
                # 한 페이지에 9개의 항목이 존재 -> 이번 페이지 출력 종료
                if (i == 10):
                    break

            # 깃발이 세워졌으면 출력 종료
            if (flag == 1):
                break

            # 페이지 넘기기
            no = no + 1

        # 정규식으로 벨트 필수 항목 걸러내기 -> red로 바꿔줘야함. 
        for tr in tr_list:
            name = tr.select_one("td.left > span > a").get_text().strip()
            date = tr.select_one("td:nth-of-type(5)").string
            href = "https://www.jbnu.ac.kr/kor/" + tr.select_one("td.left > span > a").attrs['href']
            id = tr.select_one("th").string
            if (re.compile("벨트|belt", re.IGNORECASE).search(name)):
                notice = { "_id": id, "name": name, "link": href, "belt": "RED", "date": date }
                notices.append(notice)
#==============================================================================================================================
    def get_black(notices):
        black = parse.urlencode({"subject": "black"})
        no = 1 # 페이지 인덱스
        flag = 0 # 중단 깃발
        # 검색했을 때 주소
        blacksearch = announce + "&" + black + "&" + sfv
        # 항목 리스트
        tr_list = []

        while (True):
            kurl = blacksearch + "&" + pno(no)  # 페이지 주소   
            res_black = req.urlopen(kurl)
            black_soup = BeautifulSoup(res_black, 'html.parser')
        
            i = 1 # 항목 인덱스
            while (True):
                # tr 하나가 공지 항목 하나
                # 등록 날짜 가져오기 - 큰사람과 벨트 모두 5번째 td에서 날짜 나옴.
                date = datetime.strptime(black_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ") > td:nth-of-type(5)").string, "%Y.%m.%d").date()

                # 올해 3월에 생성된 공지를 넘어가면
                if (date < sep):
                    flag = 1 # 중단 깃발 세우기
                    break

                tr_list.append(black_soup.select_one("#print_area > div.page_list > table > tbody > tr:nth-of-type(" + str(i) + ")"))

                # 다음 항목으로 넘어가기
                i = i + 1
                # 한 페이지에 9개의 항목이 존재 -> 이번 페이지 출력 종료
                if (i == 10):
                    break

            # 깃발이 세워졌으면 출력 종료
            if (flag == 1):
                break

            # 페이지 넘기기
            no = no + 1

        # 정규식으로 벨트 항목만 걸러내기 -> black으로 바꿔야함
        for tr in tr_list:
            name = tr.select_one("td.left > span > a").get_text().strip()
            date = tr.select_one("td:nth-of-type(5)").string
            href = "https://www.jbnu.ac.kr/kor/" + tr.select_one("td.left > span > a").attrs['href']
            id = tr.select_one("th").string
            if (re.compile("벨트|belt", re.IGNORECASE).search(name)):
                notice = { "_id": id, "name": name, "link": href, "belt": "BLACK", "date": date }
                notices.append(notice)
#==============================================================================================================================
    get_big(notices)
    get_white(notices)
    get_yellow(notices)
    get_blue(notices)
    get_red(notices)
    get_black(notices)
    get_big_context(notices)

    return notices
#==============================================================================================================================

# 공지사항 목록을 저장하기
def save_notices():
    notices =  get_notices()
    for notice in notices:
        Notice(_id=notice['_id'], name=notice['name'], link=notice['link'], belt=notice['belt'], date=notice['date']).save()