import sys
import scoring
import math
import numpy as np
import time
import scipy
from sklearn.cluster import *


class Clustering:
    def loadfile(self, filename):
        data = []
        try:
            file = open(filename, 'r')
        except:
            sys.stderr.write("No input file\n")
            exit(1)
        for line in file:
            data.append(line.replace('\n', '').split('\t'))
        return data

    def whiltelist(self, filename):
        data = []
        try:
            file = open(filename, 'r')
        except:
            sys.stderr.write("No input file\n")
            exit(1)
        for line in file:
            data.append(line.replace(' \n', '').split(' '))
        return data

    def calcDensity(self, data):
        cnt = 0
        if len(data) < 2:
            return 0
        for node in data:
            cnt = cnt + len(self.nodes_dict[node]["neighbor"])
        return cnt / (len(data) * (len(data) - 1))

    def find_divided(self, data):
        clustered = []
        old_data = set()
        for i in list(data.keys()):
            if i in old_data:
                continue
            tmp_data = {i}
            tmp_data.update(data[i]['neighbor'])
            now_level = set(data[i]['neighbor'])
            cnt = 0
            while True:
                cnt += 1
                tmp = set()
                for node in now_level:
                    tmp.update(data[node]['neighbor'])
                tmp_data.update(now_level)
                now_level = tmp.difference(tmp_data)
                if len(now_level) == 0:
                    break
            old_data.update(tmp_data)
            if len(tmp_data) < 3:
                clustered.append(list(tmp_data))
            else:
                clustered.append(list(tmp_data))
        return clustered

    def entropy(self, data):
        cnt = 0
        entropy = 0
        for node in data:
            cnt += len(self.nodes_dict[node]['neighbor'])
        cnt = cnt / 2
        for node in data:
            p = len(self.nodes_dict[node]['neighbor']) / cnt
            entropy -= p * math.log(p, 2)
        return entropy

    def __init__(self):
        self.whitelist = self.whiltelist('complexes_human_cln_flt.txt')
        self.whitelistset = set()
        for i in self.whitelist:
            self.whitelistset.update(i)
        self.clustercnt = 0
        self.FinalCluster = []
        data = self.loadfile('biogrid_human_ppi_cln.txt')
        self.nodes_dict = {}
        self.clusters = []
        for protein in data:
            if protein[0] in self.whitelistset and protein[1] in self.whitelistset:
                if self.nodes_dict.get(protein[0]):
                    self.nodes_dict[protein[0]]['neighbor'].append(protein[1])
                else:
                    self.nodes_dict[protein[0]] = {'neighbor': [protein[1]], 'count': 0}
                self.nodes_dict[protein[0]]['count'] = len(self.nodes_dict[protein[0]]['neighbor'])
                if self.nodes_dict.get(protein[1]):
                    self.nodes_dict[protein[1]]['neighbor'].append(protein[0])
                else:
                    self.nodes_dict[protein[1]] = {'neighbor': [protein[0]], 'count': 0}
                self.nodes_dict[protein[1]]['count'] = len(self.nodes_dict[protein[1]]['neighbor'])
            else:
                if self.nodes_dict.get(protein[0]):
                    self.nodes_dict[protein[0]]['neighbor'].append(protein[1])
                else:
                    self.nodes_dict[protein[0]] = {'neighbor': [protein[1]], 'count': 0}
                self.nodes_dict[protein[0]]['count'] = len(self.nodes_dict[protein[0]]['neighbor'])
                if self.nodes_dict.get(protein[1]):
                    self.nodes_dict[protein[1]]['neighbor'].append(protein[0])
                else:
                    self.nodes_dict[protein[1]] = {'neighbor': [protein[0]], 'count': 0}
                self.nodes_dict[protein[1]]['count'] = len(self.nodes_dict[protein[1]]['neighbor'])
        ###################################################################################################

        #                                            전처리

        ###################################################################################################
        protein_type = {'isolate': {}, 'valuable': {}}

        # 노드가 두개 뿐인 그래프 분리
        for node in self.nodes_dict.items():
            if node[1]['count'] == 1 and self.nodes_dict.get(node[1]['neighbor'][0])['count'] == 1:
                protein_type['isolate'][node[0]] = node[1]
            else:
                protein_type['valuable'][node[0]] = node[1]
        self.clusters = self.find_divided(self.nodes_dict)

        for i in self.clusters:
            density = self.calcDensity(i)
            entropy = self.entropy(i)
            if entropy and len(i) > 3:
                self.FinalCluster.extend(self.DctBasedClustering(i))
            else:
                self.FinalCluster.append(i)

    ###################################################################################################

    #                                          clustering

    ###################################################################################################
    def DctBasedClustering(self, data):
        index = {}

        for i in range(len(data)):
            index[data[i]] = i
        distance = np.zeros((len(data), len(data)))

        start = time.time()
        entropy = 0
        for idx in range(len(data)):
            cnt = 0
            next_nodes = self.nodes_dict[data[idx]].get('neighbor')
            distance[idx][idx] = 0
            while True:
                cnt = cnt + 1
                tmp = set()
                for i in next_nodes:
                    if distance[idx][index[i]] == 0:
                        distance[idx][index[i]] = cnt
                        tmp.update(self.nodes_dict[i].get('neighbor'))
                if len(tmp):
                    next_nodes = list(tmp)
                else:
                    break
        for i in range(len(data)):
            distance[i][i] = 0
        dct = np.zeros((len(data), len(data)))
        for i in range(len(distance)):
            dct[i] = scipy.fft.dct(distance[i])
        if len(data)>3:
            DCTSIZE = int(len(data)/8)
            #LowFreq = int(DCTSIZE/2)
            #DCTSIZE = int(len(data) / 2)
            LowFreq = 1
            idct = np.zeros((len(data), len(data)))
            for i in range(len(distance)):
                #idct[i] = scipy.fft.idct(np.append(np.zeros(LowFreq),np.append(dct[i][LowFreq:DCTSIZE], np.zeros(len(data)-DCTSIZE))))
                #idct[i] = scipy.fft.idct(dct[i][LowFreq:DCTSIZE])
                distance[i] -= sum(distance[i])/len(data)
            distance -= distance.min()
            distance *= 1 / distance.max()
            CLUSTERINGMETHOD = DBSCAN(eps=0.3, min_samples=2).fit(distance)
            labels = CLUSTERINGMETHOD.labels_
            n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
            if n_clusters_:
                test = [[] for _ in range(n_clusters_)]
                for i in range(len(labels)):
                    test[labels[i]].append(data[i])
                print("time :", time.time() - start)
                return test
            else:
                print('!')
                return [data]
        else:
            return [data]

    ###################################################################################################

    #                                            후처리

    ###################################################################################################
    def final(self):
        cnt = 0
        for i in self.FinalCluster:
            cnt += len(i)
        print('평균 클러스터 크기: ', cnt/len(self.FinalCluster))
        return self.FinalCluster

    ###################################################################################################

    #                                         저장,스코어 계산

    ###################################################################################################
    def print_score(self, data):
        score = scoring.fscore()
        score.F_score(data)


def save_data(data):
    return data


if __name__ == '__main__':
    algorythm = Clustering()
    clusters = algorythm.final()
    algorythm.print_score(clusters)
