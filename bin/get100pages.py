from bs4 import BeautifulSoup,Tag
from urllib import request
import urllib
from urllib.error import HTTPError
from time import sleep
from bs4.element import Comment
import os
import re

encoding = ['utf-8','gbk']


class HtmlFile:
    def __init__(self,bs_page,file_name):
        self.bs_page = bs_page
        self.file_name = file_name


class HandlePages:
    def __init__(self,url_file=None,page_directory = None,url=None):
        self.page_list = []
        self.news_url = "https://news.sina.com.cn/"
        self.page_list = []
        if url_file:
            self.url_list = list(open(url_file))
            self.get_page_list()
        else:
            # 测试用
            self.url_list = ['http://book.zongheng.com/chapter/966275/61160947.html']
        if page_directory:
            self.get_page_list_from_directory(page_directory)
        if url:
            self.url_list = self.url_list if self.url_list else []
            self.url_list.append(url)
            self.get_page_list()

    def get_page_list(self):
        for url in self.url_list:
            res = self.get_html(url)
            coding = res.headers.get_content_charset()
            # 这里不该这么写，应该用将所有编码方式放在一个列表里，用遍历的方式找到正确编码
            if not coding:
                coding = 'utf8'
            bs_page = BeautifulSoup(res.read().decode(coding), features="lxml")
            hf = HtmlFile(bs_page,url)
            self.page_list.append(hf)
        return self.page_list

    def get_page_list_from_directory(self,dire):
        files = os.listdir(dire)
        for file in files:
            if not os.path.isdir(file):
                print(file)
                try:
                    for code in encoding:
                        bs_page = BeautifulSoup(open(dire + "/" + file,encoding=code),features='lxml')
                        break
                except ValueError as err:
                    print(err)
                self.page_list.append(HtmlFile(bs_page,file))

    # def show_sensitive_word(self):
    #     s_word = "首页"
    #     for page in self.page_list:
    #         for x in page.find_all(text=s_word):
    #             x.parent.insert(x.parent.index(x), Tag(x, 'br'))

    def get_html(self,url):
        headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
        data1 = urllib.request.Request(url, headers=headers)
        res = request.urlopen(data1)
        return res

    def search_news_pages(self):
        res = self.get_html(self.news_url)
        coding = res.headers.get_content_charset()
        if not coding:
            coding = "utf8"
        bs_page = BeautifulSoup(res.read().decode(coding), features="lxml")
        i = 0
        for link in bs_page.find_all('a'):
            try:
                h = link['href']
                if not h.endswith('html'):
                    continue
                print(h)
                html = self.get_html(h).read()
                sleep(1)
            except HTTPError:
                continue
            except KeyError:
                continue
            with open('../news_page/' + str(i) + ".html","wb") as f:
                f.write(html)
                i += 1

    # 返回页面的所有文本内容
    def get_sentence_list(self) -> list:
        sentence_list = []
        for file in self.page_list:
            page = file.bs_page
            texts = page.findAll(text=True)
            visible_texts = filter(self.tag_visible, texts)
            tmp_list = []
            for text in visible_texts:
                if text and text != '\n':
                    tmp_list.append(text)
            sentence_list.append(tmp_list)
        return sentence_list

    # 将网页中的所有敏感词标红，返回页面
    @staticmethod
    def mark_sensitive_words(page,words,file):
        for word in words:
            sen_regexp = re.compile('.*'+word+'.*')
            texts = page.findAll(text=sen_regexp)
            for text in texts:
                text.parent["style"] = "color:red"
        f = open(file,'wb')
        f.write(page.prettify().encode(encoding='utf8'))
        # print(page.prettify(),file=f)

    def tag_visible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True



if __name__ == '__main__':
    s_test = HandlePages(page_directory='/Users/qinzeyu/PycharmProjects/SensitiveWord/news_page')
    sentences = s_test.get_sentence_list()
    for sentence in sentences:
        print(sentence)

