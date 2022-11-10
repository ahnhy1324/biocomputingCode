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


def ConstructFa(pattern):
    cnt = 0
    NextState = 1
    FaTrue = {}
    for i in pattern:
        cnt += len(i)
    for i in range(cnt+1):
        FaTrue[i] = {}
    for i in range(len(pattern)):
        NowState = 0
        for e in range(len(pattern[i])):
            if FaTrue[NowState].get(pattern[i][e]):
                NowState = FaTrue[NowState].get(pattern[i][e])[0]
            else: 
                FaTrue[NowState][pattern[i][e]] = [NextState,-1]
                if e == len(pattern[i])-1:
                    FaTrue[NowState][pattern[i][e]] = [NextState,i]
                NowState = NextState
                NextState += 1
    return FaTrue

def fail(que,ConstFa,pre_text,next_text):
    for i in range(len(que)):
        if ConstFa[que[len(que)-i-1]].get(pre_text):
            Nowstate = ConstFa[que[len(que)-i-1]].get(pre_text)[0]
            if ConstFa[Nowstate].get(next_text):
                Nowstate = ConstFa[Nowstate].get(next_text)[0]
            else:
                if len(que) != i:
                    Nowstate = fail(que[:len(que) - i],ConstFa,pre_text,next_text)
            print(Nowstate)           
            return Nowstate
    return 0
        

def FindMatch(text, ConstFa, pattern):
    Nowstate = 0
    que = []
    for i in range(len(text)):
        print(text[i],'--------')
        find = ConstFa[Nowstate].get(text[i])
        if find:
            que.append(Nowstate)
            if find[1] >-1:
                print(pattern[find[1]])
            Nowstate = find[0]
        else:
            Nowstate = fail(que[:len(que)],ConstFa,text[i-1],text[i])
    return text

def ShowFind(result, pattern):
    if len(result):
        for i in range(len(result)):
            pass
    else:
        print("No match found")
    return 0

if __name__ == '__main__':
    text, pattern = LoadData(sys.argv)
    start_time = datetime.datetime.now()
    ConstFa = ConstructFa(pattern)
    finded = FindMatch(text[0],ConstFa, pattern)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    ShowFind(finded, pattern)
    print('동작시간: ', elapsed_time.microseconds, 'ms')
