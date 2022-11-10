# 2017253019 안희영
# Assignment 3

import sys
import datetime


# 파일 로드
def load_data(args):
    # 파일 존재여부
    global file
    data = ''
    try:
        file = open(args, 'r')
    except:
        sys.stderr.write("No input file\n")
        exit(1)
    for line in file:
        data = line
    data = data.upper()
    if len(data) == 0:
        sys.stderr.write("No string found\n")
        exit(1)
    else:
        return data
    exit(1)


def exhaustive(text, pattern):
    n = len(text)
    m = len(pattern)
    cnt = 0
    for i in range(n - m):
        if pattern == text[i:i + m]:
            print(i)
            cnt += 1
    if cnt == 0:
        print('No match found')


def pattern_match(text, pattern, method):
    if method == 'KMP':
        KMP(text, pattern)
    if method == 'exhaustive':
        exhaustive(text, pattern)


def KMP_Prefix(pattern):
    m = len(pattern)
    shift_table = [0 for _ in range(len(pattern))]
    k = 0
    for q in range(m - 1):
        while k > 0 and pattern[k] != pattern[q + 1]:
            k = shift_table[k - 1]
        if pattern[k] == pattern[q + 1]:
            k += 1
        shift_table[q + 1] = k
    return shift_table


def KMP(text, pattern):
    n = len(text)
    m = len(pattern)
    q = 0
    found = []
    prefixed_data = KMP_Prefix(pattern)
    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = prefixed_data[q - 1]
        if pattern[q] == text[i]:
            q = q + 1
        if q == m:
            found.append(i - m + 1)
            q = prefixed_data[q - 1]
    if len(found):
        for i in found:
            print(i)
    else:
        print('No match found')


if __name__ == '__main__':
    str1 = load_data(sys.argv[1])
    str2 = load_data(sys.argv[2])
    start_time = datetime.datetime.now()
    if len(str1) < len(str2):
        pattern_match(str2, str1, 'exhaustive')
    else:
        pattern_match(str1, str2, 'exhaustive')
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print('동작시간: ', elapsed_time.microseconds, 'ms')
