import hanlp

tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')


class HandleSentence:

    # 传入一个str的列表
    def __init__(self,sentence_list=None):
        self.sentence_list = sentence_list
        self.sensitive_words_dic = {}
        self.sensitivity = 0
        # 列表中含有的敏感词
        self.containing_sensitive_words = set()

    # 返回分词
    def divide_sentence(self):
        return [tokenizer(sentence) for sentence in self.sentence_list]

    # 从文档中读取敏感词
    def get_sensitive_words_list_from_file(self, file, grade):
        words = set()
        with open(file) as f:
            for line in f.readlines():
                # print(line)
                words.add(line[:-1])
        self.sensitive_words_dic[grade] = words

    # 计算敏感度
    def compute_sensitivity(self):
        for sentence in self.divide_sentence():
            for word in sentence:
                if word in self.sensitive_words_dic[1]:
                    self.containing_sensitive_words.add(word)
                    self.sensitivity += 1
                elif word in self.sensitive_words_dic[2]:
                    self.containing_sensitive_words.add(word)
                    self.sensitivity += 2
                elif word in self.sensitive_words_dic[3]:
                    self.containing_sensitive_words.add(word)
                    self.sensitivity += 3
        return self.sensitivity


if __name__ == '__main__':
    hs = HandleSentence(['123','中共邪教'])
    hs.get_sensitive_words_list_from_file(file='/Users/qinzeyu/PycharmProjects/SensitiveWord/assistingfile/words/1级.txt',grade=1)
    hs.compute_sensitivity()
    print(hs.sensitivity)
    # print(hs.sensitive_words_dic[1])
