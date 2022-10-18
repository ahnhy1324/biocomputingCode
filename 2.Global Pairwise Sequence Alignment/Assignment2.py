# 2017253019 안희영
# Assignment 2

import sys
import datetime
import numpy as np
import textwrap

GeneElements = ['A', 'T', 'C', 'G']

Gap = -1
missmatch = -1
match = 1


def valid_gene(qqq):  # ATCG 이외의 문자열 확인
    for i in GeneElements:
        if i in qqq:
            qqq = qqq.replace(i, '')
    return len(qqq)


# 파일 로드
def load_data(args):
    seq = ''
    flag = 0
    test = []
    # 파일 존재여부
    try:
        file = open(args, 'r')
    except:
        sys.stderr.write("No input file\n")
        exit(1)
    for line in file:
        data = ''.join(line.split())  # 공백제거
        if len(data):
            if flag == 2:
                if data[0] == '>':
                    break;
                seq += data
            elif flag == 1:
                if data[0] == '>':
                    flag = 2
                    test.append(seq.upper())
                    print('Sequence2 : ' + line.rstrip())
                    seq = ""
                else:
                    seq += data
            elif data[0] == '>':
                flag = 1
                print('Sequence1 : ' + line.rstrip())
            else:  # Sequence 이전의 주석 출력
                print(line)
    test.append(seq.upper())
    print('------------------------------------------------------------')
    if flag == 0:
        sys.stderr.write("No correct format\n")  # >로 시작하는 문장 없음
    elif len(test[0]) == 0 or valid_gene(test[0].upper()):  # 프로틴 시퀸스가 없음 or atcg 이외의 문자
        sys.stderr.write("No protein sequence\n")
    elif len(test[1]) == 0:  # 시퀸스가 하나인 경우
        sys.stderr.write("Need one more sequence\n")
    elif valid_gene(test[1].upper()):
        sys.stderr.write("No protein sequence\n")  # 두번째 시퀸스에 atcg 이외의 문자
    else:
        return test
    exit(1)


def find(data):
    # 시작지점:0, 대각선:1,  seq1 gap:2  seq2 gap:3
    table = np.zeros((len(data[1]) + 1, len(data[0]) + 1))
    tracker = np.zeros((len(data[1]) + 1, len(data[0]) + 1))
    tmp = []
    for seq2 in range(len(data[1]) + 1):
        for seq1 in range(len(data[0]) + 1):
            if seq1 == 0 and seq2 == 0:
                pass
            elif seq1 == 0:
                table[seq2][seq1] = table[seq2 - 1][seq1] + Gap
                tracker[seq2][seq1] = 3
            elif seq2 == 0:
                table[seq2][seq1] = table[seq2][seq1 - 1] + Gap
                tracker[seq2][seq1] = 2
            else:
                if data[0][seq1 - 1] == data[1][seq2 - 1]:
                    diagonal = match
                else:
                    diagonal = missmatch
                tmp.append(diagonal + table[seq2 - 1][seq1 - 1])
                tmp.append(table[seq2 - 1][seq1] + Gap)
                tmp.append(table[seq2][seq1 - 1] + Gap)
                if max(tmp) == diagonal + table[seq2 - 1][seq1 - 1]:
                    tracker[seq2][seq1] = 1
                    table[seq2][seq1] = diagonal + table[seq2 - 1][seq1 - 1]
                elif max(tmp) == table[seq2][seq1 - 1] + Gap:
                    tracker[seq2][seq1] = 2
                    table[seq2][seq1] = table[seq2][seq1 - 1] + Gap
                elif max(tmp) == table[seq2 - 1][seq1] + Gap:
                    tracker[seq2][seq1] = 3
                    table[seq2][seq1] = table[seq2 - 1][seq1] + Gap
                tmp.clear()
    return tracker


def backtracking(track, seq):
    xPoint = len(seq[0])
    yPoint = len(seq[1])
    seq1, seq2 = "", ""
    k, j = 0, 0
    while True:
        heading = track[yPoint][xPoint]
        if heading == 0:
            break
        elif heading == 1:
            seq1 = seq[0][xPoint - 1] + seq1
            seq2 = seq[1][yPoint - 1] + seq2
            yPoint -= 1
            xPoint -= 1
            k += 1
            j += 1
        elif heading == 2:
            seq2 = '_' + seq2
            seq1 = seq[0][xPoint - 1] + seq1
            xPoint = xPoint - 1
            k += 1
        elif heading == 3:
            seq1 = '_' + seq1
            seq2 = seq[1][yPoint - 1] + seq2
            yPoint = yPoint - 1
            j += 1
    for z, q in zip(textwrap.wrap(seq1, width=60), textwrap.wrap(seq2, width=60)):
        print(z, '\n', q, '\n\n')


if __name__ == '__main__':
    SeqList = load_data(sys.argv[1])
    print(len(SeqList[0])*len(SeqList[1]))
    start_time = datetime.datetime.now()
    result = find(SeqList)
    backtracking(result, SeqList)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print('동작시간: ', elapsed_time.microseconds, 'ms')
