# 2017253019 안희영
# Assignment 1, String Manipulation with Regular Expression

import sys
import itertools
import datetime
import re

lowComp_MinLen = 2
lowComp_MaxLen = 5
GeneElements = ['A', 'T', 'C', 'G']


# 찾아낼 유전자 반복 테이블 생성
def makeGeneTable():
    result = []
    for i in range(lowComp_MaxLen - lowComp_MinLen + 1):
        result += list(itertools.product(GeneElements, repeat=i + 2))
    for i in range(len(result)):
        result[i] = ''.join(result[i])
    return result


def valid_gene(qqq):  # ATCG 이외의 문자열 확인
    for i in GeneElements:
        if i in qqq:
            qqq = qqq.replace(i, '')
    return len(qqq)


# 파일 로드
def load_data(args):
    seq = ''
    flag = 0
    # 파일 존재여부
    try:
        file = open(args, 'r')
    except:
        sys.stderr.write("No input file\n")
        exit(1)

    for line in file:
        data = ''.join(line.split())  # 공백제거
        if len(data):
            if flag == 1:
                if data[0] == '>':
                    break;
                seq += data
            elif data[0] == '>':
                flag = 1
                print('Sequence : ' + line.rstrip())
            else:  # Sequence 이전의 주석 출력
                print(line)
    print('--------------------------------------------------------------------------------------------')
    if flag == 0:
        sys.stderr.write("No correct format\n")
    elif len(seq) == 0 or valid_gene(seq.upper()):
        sys.stderr.write("No DNA sequence\n")
    else:
        return seq.upper()
    exit(1)


def find_target(data):
    sp = 0
    target = re.compile(r'([ATCG]{2,5})\1(\1)+')
    if len(target.findall(data[sp:])):
        while True:
            i = target.search(data[sp:])
            if not i:
                break
            print(i.span()[0]+sp)
            sp = i.span()[1]+sp
            if len(data[sp:]) < 5:
                break
    else:
        print("No low-complexity region found")


if __name__ == '__main__':
    Sequence = ''
    Gene_table = makeGeneTable()
    Sequence = load_data(sys.argv[1])
    start_time = datetime.datetime.now()
    find_target(Sequence)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print('동작시간: ', elapsed_time.microseconds, 'ms')
