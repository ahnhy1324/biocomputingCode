# args1로 네트워크 결과물을 입력받습니다.
# 네트워크 결과물 : 클러스터 한 개를 한 줄로 모아서, 노드를 공백으로 구분하여 출력한다고 생각하고 프로그래밍했습니다.

import sys

#def jaccard_similality(list1, list2):   # 자카르 유사도
#    s1 = set(list1)
#    s2 = set(list2)
#   
#    return float(len((s1.intersection(s2)) / len(s1.union(s2))))        # 클러스터 교집합 데이터 내부 클러스터 / 클러스터 합집합 데이터 내부 클러스터
class fscore:
    def __init__(self, filename = 'complexes_human_cln_flt.txt'):
        self.data_file = ''
        try:
            with open(filename, 'r') as file:
                self.data_file = file.readlines()
        except FileNotFoundError:
            print('No data file')
            exit(1)
        for i in range(0, len(self.data_file)):
            self.data_file[i] = self.data_file[i].rstrip().replace("\n", "").split(" ")
        

    def f_measure(self, list, data):  # f score
        s1 = set(list)
        s2 = set(data)
        presition = float(len(s1.intersection(s2)) / len(s2))    # 클러스터 교집합 데이터 내부 클러스터 / 클러스터
        recall = float(len(s1.intersection(s2)) / len(s1))
        if(recall == 0 and presition == 0):
            return 0
            # 두개가 0이면 계산에서 0으로 나눌 수 없다는 오류가 나와서 따로 0으로 출력합니다.
        else:
            return float((2.0 * presition * recall) / (presition + recall))
        

    def F_score(self, cluster, read_score = False):
        #for i in cluster_count:
        #print(i + 1, '번째 클러스터 : ', cluster[i])
        result = float(0)
        cluster_count = len(cluster)
        data_count = len(self.data_file)
        score = [0 for i in range(0, cluster_count)]
        for i in range(0, cluster_count - 1):
            #print(i + 1, '번째 클러스터 계산중...')
            for j in range(0, data_count - 1):
                score[i] = max(score[i], self.f_measure(cluster[i], self.data_file[j]))

                # i번째 줄의 점수로 기존 점수와 f score 계산을 통해 나온 것 중에서 가장 큰 점수로 집어넣습니다.
        for i in range(cluster_count):
            if read_score:
                print(i + 1, '번째 클러스터의 f score : ', score[i])
            result = float(result + score[i])
            #print(i+1,'번째 score를 더한 result : ', result)
            
        print('cluster_count : ', cluster_count)
        result = float(result / cluster_count)
            
        print('f score : ', result)
