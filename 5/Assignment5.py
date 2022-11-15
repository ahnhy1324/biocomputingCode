# 2017253019 안희영
# Assignment 5

import sys
import datetime
import numpy as np


# 파일 로드
def LoadFile(args):
    # 파일 존재여부
    global file
    data = []
    try:
        file = open(args, 'r')
    except:
        sys.stderr.write("No input file\n")
        exit(1)
    for line in file:
        data.append(line.upper().replace('\n',''))
    if len(data) == 0:
        sys.stderr.write("No string found\n")
    else:
        return data
    exit(1)

def LoadData(args):
    str1 = LoadFile(args[1])
    str2 = LoadFile(args[2])
    if len(str1) + len(str2) == 2:
        sys.stderr.write("No multiple patterns found\n")
        exit()
    elif len(str1) == 1:
        text = str1
        pattern = str2
    elif len(str2) == 1:
        text = str2
        pattern = str1
    else:
        sys.stderr.write("No text found\n")
        exit()
    return np.asarray(text), np.asarray(pattern)


def pop(data):
    return data[1::]


def ConstructFa(pattern):
    cnt = 0
    NextState = 1
    Tree = {}  # {}


    for i in pattern:
        cnt += len(i)
    for i in range(cnt+1):
        Tree[i] = {'fail':0, 'hit':-1, 'data':''}
    for i in range(len(pattern)):
        NowState = 0
        for e in range(len(pattern[i])):
            if Tree[NowState].get(pattern[i][e]):#이미 존재하는 경우
                NowState = Tree[NowState].get(pattern[i][e])
            else:
                Tree[NowState][pattern[i][e]] = NextState
                Tree[NextState]['data'] = pattern[i][:e + 1]
                NowState = NextState
                NextState = NextState + 1
            if e == len(pattern[i]) - 1:# 패턴의 마지막인 경우
                Tree[NowState]['hit'] = i
    #여기까지가 트리 생성, 이후 Fail 노드 생성
    for i in range(len(Tree)):
        nowstate = 0
        tmp = pop(Tree[i].get('data'))
        while len(tmp):
            flg = 0
            nowstate = 0
            for char in tmp:
                if Tree[nowstate].get(char):
                    nowstate = Tree[nowstate].get(char)
                    flg = flg + 1
                else:
                    break
            if flg == len(tmp):
                break
            tmp = pop(tmp)
        if len(tmp):
            Tree[i]['fail'] = nowstate
    return Tree

def test():
    return 0
def FindMatch(text, Tree, num_pattern):
    text = text +'\n'
    Nowstate = 0
    output = [[] for _ in range(num_pattern)]
    for i in range(len(text)):
        while True:
            tmp = Tree[Nowstate].get(text[i])
            if Tree[Nowstate]['hit'] > -1:
                output[Tree[Nowstate]['hit']].append(i - 1)
            if tmp:
                Nowstate = tmp
                break
            else:
                if Nowstate==0:
                    break
                else:
                    Nowstate = Tree[Nowstate].get('fail')
    return output

def ShowFind(result, pattern):
    cnt = 0
    for i in result:
        cnt = cnt + len(i)
    if cnt:
        for pat in range(len(pattern)):
            for i in range(len(result[pat])):
                result[pat][i] = result[pat][i] - len(pattern[pat])+1
            print('pattern: ', pattern[pat],'\nlocation:',end=' ')
            if len(result[pat]):
                print(result[pat])
            else:print('none')
    else:
        print("No match found")

if __name__ == '__main__':
    text, pattern = LoadData(sys.argv)
    start_time = datetime.datetime.now()
    Tree = ConstructFa(pattern)
    finded = FindMatch(text[0],Tree, len(pattern))
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print('text: ',text[0])
    ShowFind(finded, pattern)
    print('동작시간: ', elapsed_time.microseconds, 'ms')
