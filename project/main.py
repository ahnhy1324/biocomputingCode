import sys

def LoadFile(filename):
    # 파일 존재여부
    global file
    data = []
    try:
        file = open(filename, 'r')
    except:
        sys.stderr.write("No input file\n")
        exit(1)
    for line in file:
        data.append(line.replace('\n', '').split('\t'))
    return data


data = LoadFile('biogrid_human_ppi_cln.txt')
nodes_dict = {}
for protein in data:
    if nodes_dict.get(protein[0]):
        nodes_dict[protein[0]]['neighbor'].append(protein[1])
    else:
        nodes_dict[protein[0]] = {'neighbor':[protein[1]], 'count':0}
    nodes_dict[protein[0]]['count'] = len(nodes_dict[protein[0]]['neighbor'])
    if nodes_dict.get(protein[1]):
        nodes_dict[protein[1]]['neighbor'].append(protein[0])
    else:
        nodes_dict[protein[1]] = {'neighbor':[protein[0]], 'count':0}
    nodes_dict[protein[1]]['count'] = len(nodes_dict[protein[1]]['neighbor'])
###################################################################################################

#                                            전처리

###################################################################################################
protein_type = {'isolate': {}, 'low_value': {}, 'valuable': {}}

# 독립네트워크, 독립은 아니지만 엣지가 하나인 노드, 엣지가 여러개인 노드 분리
for node in nodes_dict.items():
    if node[1]['count'] == 1 and nodes_dict.get(node[1]['neighbor'][0])['count'] == 1:
        protein_type['isolate'][node[0]] = node[1]
    elif node[1]['count'] == 1:
        protein_type['low_value'][node[0]] = node[1]
    else:
        protein_type['valuable'][node[0]] = node[1]



pass