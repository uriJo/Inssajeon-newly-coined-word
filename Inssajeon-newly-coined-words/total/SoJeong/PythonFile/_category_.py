
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from keras.models import load_model
from sklearn.feature_extraction.text import TfidfVectorizer
import re

komoran = Komoran()
kkma = Kkma()
model = load_model('/Model/category.h5')

def categoryModel(word):
    file = open('/Result/pos.txt')
    XWord = []
    for i in file:
        i = re.sub('\n', '', i)
        XWord.append(i)

    # 학습
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer.fit(XWord[1:])
    X = tfidf_vectorizer.transform(XWord[1:])
    X = X.toarray()
    category = ""
    #초성
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
    
    #komoran 분석 단어용
    def NA(word):
        choSung = []
        otherTagging = kkma.pos(word)
        for i in otherTagging:
            choSung.append(i[1])
        return choSung
    if conl(word) == True:
        category = "초성어"
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


result = categoryModel("개이득")
