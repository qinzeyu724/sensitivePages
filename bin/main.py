from bin.get100pages import HandlePages
from bin.divide_words import HandleSentence
import os
print(os.getcwd())

pages = HandlePages(page_directory='/Users/qinzeyu/PycharmProjects/SensitiveWord/news_page')
# pages = HandlePages(url='http://cn.chinadaily.com.cn/a/202008/09/WS5f2f431ea310a859d09dcc84.html')
page = pages.get_sentence_list()
sensitive_words = []
for sentences in page:
    hs = HandleSentence(sentences)
    hs.get_sensitive_words_list_from_file(file='../assistingfile/words/1级.txt', grade=1)
    hs.get_sensitive_words_list_from_file(file='../assistingfile/words/2级.txt', grade=2)
    hs.get_sensitive_words_list_from_file(file='../assistingfile/words/3级.txt', grade=3)
    hs.compute_sensitivity()
    print(hs.sensitivity)
    print(hs.containing_sensitive_words)
    sensitive_words.append(hs.containing_sensitive_words)

i = 0
for page,sensitive_words in zip(pages.page_list,sensitive_words):
    i += 1
    page = HandlePages.mark_sensitive_words(page,sensitive_words,"../sensitive_pages/"+str(i)+".html")