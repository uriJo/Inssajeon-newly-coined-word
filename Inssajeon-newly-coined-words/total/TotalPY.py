# 결과 Final/final.json
from collections import OrderedDict
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor
from soynlp.tokenizer import MaxScoreTokenizer
import pandas as pd
from konlpy.tag import Okt, Kkma, Komoran
from keras.models import load_model
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import hunspell
from gensim.models import FastText
import json
import time

start = time.time()  # 시작 시간 저장
okt = Okt()
kkma = Kkma()
komoran = Komoran()
model = load_model('model/category.h5')
fastText = FastText.load('model/ft_model.model')
h = hunspell.HunSpell('hunspell-dict-ko-master/data/ko.dic',
                      'hunspell-dict-ko-master/data/ko.aff')  # 맞춤법 검사기
def categoryModel(word):
    file = open("data/pos.txt")
    XWord = []
    for i in file:
        i = re.sub(' \n', '', i)
        XWord.append(i)

    # 학습
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer.fit(XWord[1:])
    X = tfidf_vectorizer.transform(XWord[1:])
    X = X.toarray()
    model = load_model('/content/drive/My Drive/URP_COLAB/sojeong_for_test/category.h5')
    category = ""

    def conl(word):
        con = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ']
        col = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']
        i = 0
        try:
            if word[0] in con:
                while i < len(word):
                    if word[i] in con:
                        i = i + 1
                    else:
                        break
            if word[0] in col:
                while i < len(word):
                    if word[i] in col:
                        i = i + 1
                    else:
                        break
            if i == len(word):
                return True
            else:
                return False
        except:
            EOFError

    wordToPos = []

    def NA(word):
        choSung = []
        otherTagging = kkma.pos(word)
        for i in otherTagging:
            choSung.append(i[1])
        return choSung

    if conl(word) == True:
        category = "초성어"
        return category
    else:
        tagging = komoran.pos(word)
        for i in tagging:
            if i[1] == 'NA':
                choTemp = NA(word)
                wordToPos.extend(choTemp)
            else:
                wordToPos.append(i[1])
        stringList = []
        stringList.append(' '.join(wordToPos))

        xhat = tfidf_vectorizer.transform(stringList).toarray()
        yhat = model.predict_classes(xhat)
        if yhat[0] == 0:
            category = "합성어"
        elif yhat[0] == 1:
            category = "줄임말"
        else:
            category = "기타"
        return category



with open('data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
    data = json.load(f)

corpus = DoublespaceLineCorpus("text/ppsd.txt", iter_sent=True)
len(corpus)
word_extractor = WordExtractor(remove_subwords=True)
word_extractor.train(corpus)
word_score = word_extractor.extract()  # word_score 뽑힌 모든 단어들의 DICTIONARY
scores = {word: score.cohesion_forward for word, score in word_score.items()}
maxscore_tokenizer = MaxScoreTokenizer(scores=scores)

sejong = []

f = open("data/sejong.txt", 'r', encoding='utf-8')  # sejong.txt => 세종 말뭉치
for line in f:
    line = re.sub('\n', '', line)
    sejong.append(line)
f.close()


def data_list(wordname):
    pol = 0
    for i in range(0, len(data)):
        if (data[i]['word'] == wordname) or (data[i]['word_root'] == wordname):
            pol = int(data[i]['polarity'])
    return pol


def KKMcheck(t):  # 합성 명사일경우 (국토교통부) > True / 4글자 이상일떄 수행?
    flag = True
    tmp = False
    tm = kkma.pos(t)
    for n, v in tm:
        tmp = (v == 'NNG') | (v == 'NNP')
        tmp = flag and tmp
    return tmp


def nameCheck(text):
    result = False
    if len(text) == 3:
        if (text[0] == '김') or (text[0] == '이') or (text[0] == '박') or (text[0] == '황'):
            result = True
        if (text == '확진자') or (text == '손석희'):
            result = True
    return result


df = pd.DataFrame()
f1 = open("text/ppsd.txt", 'r', encoding='utf-8', errors='ignore')  # 제목 데이터

for line in f1:  # ppsd.txt 한줄씩 읽기
    resultOkt = 0
    resultSoy = 0
    resultSpace = 0
    resultSent = 0
    temp = ''
    text = line.__str__()
    text = re.sub('\n', '', text)
    list_okt = []
    list_max = maxscore_tokenizer.tokenize(text)
    tmp = okt.pos(text)

    for n, v in tmp:
        if (v == 'Noun') or (v == 'KoreanParticle'):
            list_okt.append(n)

    list_Mnoun = list(set(list_max).intersection(set(list_okt)))  # max token + okt
    listSpace = text.split(' ')

    for i in range(len(list_Mnoun)):
        if (len(list_Mnoun[i]) >= 2) and (len(list_Mnoun[i]) <= 5):
            if h.spell(list_Mnoun[i]) == True:
                continue
            if nameCheck(list_Mnoun[i]):
                continue
            if list_Mnoun[i] in sejong:
                continue
            if len(list_Mnoun[i]) >= 4:
                if KKMcheck(list_Mnoun[i]):
                    #print(list_Mnoun[i], 'in KKMCHECK')
                    continue
            for j in list_okt:
                resultOkt += data_list(j)

            for j in list_max:
                resultSoy += data_list(j)

            for j in listSpace:
                resultSpace += data_list(j)
                sumSent = resultOkt + resultSoy + resultSpace

            if sumSent != 0:
                resultSent = sumSent / 3
            else:
                resultSent = sumSent

            resultSent = round(resultSent, 4)
            temp = list_Mnoun[i] + '#' + text + ':' + resultSent.__str__()
            #print(temp)
            df = df.append(pd.Series([temp]), ignore_index=True)

f1.close()
df.sort_values(by=[0], ascending=True, ignore_index=True, inplace=True)
df = df.drop_duplicates([0], keep='first')
df.sort_values(by=[0], ascending=True, ignore_index=True, inplace=True)
#print(df[:200])

# df.to_csv('/content/drive/My Drive/temp.csv','w',encoding='utf-8')
# df=pd.read_csv('/content/drive/My Drive/temp.csv','w',encoding='utf-8')

fj = open('Newly.json', 'w', encoding='utf-8')

JSON = OrderedDict()
NewlyWord = OrderedDict()
Sentence = []
Similar = []
sen_list = []
count = 0
pre = ''

for index, row in df.iterrows():
    tmp = row.to_string(index=False).split('\n ')
    temp = tmp[1].split('#')
    if pre == temp[0]:  # 같은거 중복
        sen_list.append(temp[1])  # '야붕이 오늘도 출근한다 수고링' >>
        pre = temp[0]

    else:  # 다른거로 바뀜 > 이전샛 출력
        if pre in fastText.wv.vocab:
            similar_list = list(fastText.most_similar(positive=pre, topn=10, restrict_vocab=50000)) # fastText or word2vec
            for i in range(len(similar_list)):
                temp_str = similar_list[i][0].__str__() + " " + round(fastText.wv.similarity(similar_list[i][0].__str__(), pre), 7).__str__()
                Similar.append(temp_str)

            NewlyWord["similar"] = Similar # word2vec 유사 10개 단어 (window size = 10)
        else:
            NewlyWord["similar"] = "none"
        NewlyWord["category"] = categoryModel(pre)  # pre = 신조어 후보 단어
        count = 0
        for i in range(len(sen_list)):
            if count > 4:
                continue
            else:
                Sentence.append(sen_list[i].__str__())
                count += 1

        NewlyWord["sentence"] = Sentence
        JSON[pre.__str__()] = NewlyWord
        NewlyWord = {}
        Sentence = []
        Similar = []
        sen_list = []
        sen_list.append(temp[1])
    pre = temp[0]

json.dump(JSON, fj, indent=4, ensure_ascii=False)

print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
print('end ========================')
