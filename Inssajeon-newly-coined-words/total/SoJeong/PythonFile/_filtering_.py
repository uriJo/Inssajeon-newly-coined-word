from hangul_utils import split_syllable_char, join_jamos
import re
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor
from soynlp.tokenizer import MaxScoreTokenizer


choKo = {'ㄱ':['ㄱ','ㄲ','ㅋ'], 'ㅅ' : ['ㅅ','ㅆ'], 'ㄷ' : ['ㄷ', 'ㄸ', 'ㅌ'], 'ㅈ' : ['ㅈ','ㅉ','ㅊ'], 'ㅂ' : ['ㅂ', 'ㅃ','ㅍ']}
jungKo = {'ㅏ' : ['ㅏ','ㅑ'], 'ㅗ': ['ㅗ', 'ㅛ'], 'ㅐ' : ['ㅐ','ㅒ','ㅔ','ㅖ','ㅙ','ㅚ','ㅝ','ㅞ'], 'ㅜ' : ['ㅜ','ㅠ'], 'ㅓ' : ['ㅓ','ㅕ'], 'ㅣ' : ['ㅟ','ㅢ','ㅣ']}
jongKo = {'ㄱ' : ['ㄱ', 'ㄲ','ㅋ'], 'ㅂ' : ['ㅂ', 'ㅍ'], 'ㄷ' : ['ㄷ','ㅌ', 'ㅅ','ㅈ','ㅉ','ㅊ']}

final = []

def filtering(word):
    for tm, i in enumerate(word):
        wordList = list(word)
        ttestList = wordList[:]
        temp = list(split_syllable_char(i))
        tt = temp[:]

        def cho(temp):
            try:
                for i in choKo[temp]:
                    tt[0] = i
                    ttt = join_jamos(tt)
                    ttestList[tm] = ttt
                    final.append(join_jamos(ttestList))
            except:
                EOFError

        def jung(temp):
            try:
                for i in jungKo[temp]:
                    tt[1] = i
                    ttt = join_jamos(tt)
                    ttestList[tm] = ttt
                    final.append(join_jamos(ttestList))
            except:
                EOFError
        def jong(temp):
            try:
                for i in jongKo[temp[2]]:
                    tt[2] = i
                    ttt = join_jamos(tt)
                    ttestList[tm] = ttt
                    final.append(join_jamos(ttestList))
            except:
                EOFError

        for i in range(3):
            if temp[0] in choKo:
                cho(temp[0])
                if temp[1] in jungKo:
                    jung(temp[1])
                    if temp[2] in jongKo:
                        jong(temp[2])
                    elif temp[2] is None:
                        tt[2] = ''
                else:
                    if temp[2] in jongKo:
                        jong(temp[2])
                    elif temp[2] is None:
                        tt[2] = ''
            else:
                if temp[1] in jungKo:
                    jung(temp[1])
                    if temp[2] in jongKo:
                        jong(temp[2])
                    elif temp[2] is None:
                        tt[2] = ''
                else:
                    if temp[2] in jongKo:
                        jong(temp[2])
                    elif temp[2] is None:
                        tt[2] = ''

ppsd = open('/Text/Filtering/ppsd.txt','r', encoding = 'utf-8')
ppsd_fil = open('/Result/ppsd_fil.txt', 'w', encoding = 'utf-8')

fil = open('/Text/Filtering/fil.txt', encoding = 'utf-8')
ban = open('/Text/Filtering/banned.txt', encoding = 'utf-8')

filWord = []
banWord = []
for i in fil:
    temp = re.sub("\n", "", i)
    filWord.append(temp)
fil.close()

for word in filWord:
    filtering(word)

for i in ban:
  temp = re.sub("\n", "", i)
  final.append(temp)
ban.close()


final = set(final)
final = list(final)
print(len(final), final)


corpus = DoublespaceLineCorpus('/Text/Filtering/ppsd.txt', iter_sent=True)
word_extractor = WordExtractor()
word_extractor.train(corpus)
word_score = word_extractor.extract()
scores = {word: score.cohesion_forward for word, score in word_score.items()}

maxscore_tokenizer = MaxScoreTokenizer(scores=scores)

jj = []
ppsdList = []


for i in ppsd:
  ppsdList.append(i)

finalList = []

for i in ppsdList:
  string =""
  cont =0
  mkTokzer = maxscore_tokenizer.tokenize(i)
  string = ' '.join(mkTokzer)
  for k in final:
    if k in string:
      count = 1
      break
    else:
      count =0
  if count != 1:
    ppsd_fil.write(i+'\n')
    finalList.append(i)

ppsd.close()
ppsd_fil.close()
