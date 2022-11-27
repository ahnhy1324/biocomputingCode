import sys
import scoring




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

    def calcDensity(self, data):
        cnt = 0
        for node in data:
            cnt = cnt + len(self.nodes_dict[node]["neighbor"])
        return cnt / (len(data) * (len(data) - 1))

    def find_divided(self, data):
        clusters = []
        old_data = set()
        print(len(data))
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
                self.FinalCluster.append(list(tmp_data))
            else:
                clusters.append(list(tmp_data))
        return clusters

    def merging(self, data):
        return 0

    def __init__(self):
        self.FinalCluster = []
        data = self.loadfile('biogrid_human_ppi_cln.txt')
        self.nodes_dict = {}
        self.clusters = []
        for protein in data:
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
            print("density :  ", density)

    ###################################################################################################

    #                                          clustering

    ###################################################################################################
    def my_algorythm(self):
        pass
    ###################################################################################################

    #                                            후처리

    ###################################################################################################
    def final(self):
        self.FinalCluster.extend(self.clusters)
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
