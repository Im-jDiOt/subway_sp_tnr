import csv
from collections import defaultdict, Counter
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt

# node_id_dict = {node: id}
# id_node_dict = {id: node}
# line_node_dict = {line: [node1, node2, ...]}
# node_lid_dict = {node: local_id}
# name_lines_dict = {name: [line1, line2, ...]}
#     transfer_nodes_list = [[(line1, transfer1), (line2, transfer1), ...], [(line1, transfer2), (line2, transfer2)],...] (line별)
#     transfer_nodes = [transfer_node1, transfer_node2, ...] (
#     line_transfer_nodes_dict = {line: [(transfer_node1, id1), (transfer_node2, id2), ...]}
# node_adjacent_transfer_dict = {node: [transfer_node1], node2: [transfer_node2, transfer_node3], ...}
# G = all nodes & all edges
# TG = transfer nodes & edges for them

node_id_dict = dict()
id_node_dict = dict()
line_node_dict = defaultdict(list)
node_lid_dict = dict()
name_lines_dict = defaultdict(list)
transfer_nodes_list = []
transfer_nodes = []
line_transfer_nodes_dict = defaultdict(list)
node_adjacent_transfer_dict = dict()
G = nx.Graph()
TG = nx.Graph()

with open(r'C:\Users\USER\PycharmProjects\Subway_Shortest_Path\data\results\subway_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)

    idx = 0
    for row in reader:
        from_id, from_line, from_name, to_id, to_line, to_name, duration = row

        from_node = (from_line, from_name)
        to_node = (to_line, to_name)

        if from_node not in node_id_dict:
            node_id_dict[from_node] = idx
            id_node_dict[idx] = from_node
            name_lines_dict[from_name].append(from_line)
            line_node_dict[from_line].append(from_node)
            G.add_node(from_node)
            idx += 1

        node_id_dict[to_node] = idx
        id_node_dict[idx] = to_node
        name_lines_dict[to_name].append(to_line)
        G.add_node(to_node)
        G.add_edge(from_node, to_node, weight=int(duration))
        line_node_dict[to_line].append(to_node)

        idx += 1

for _, nodes in line_node_dict.items():
    for lid, node in enumerate(nodes):
        node_lid_dict[node] = lid

for name, lines in name_lines_dict.items():
    if len(lines) > 1:
        transfer_nodes_list.append([(line, name) for line in lines])
        for line in lines:
            transfer_node = (line, name)
            transfer_nodes.append(transfer_node)
            TG.add_node(transfer_node)

for _transfer_nodes in transfer_nodes_list:
    for tnode1, tnode2 in combinations(_transfer_nodes, 2):
        G.add_edge(tnode1, tnode2, weight=2)
        TG.add_edge(tnode1, tnode2, weight=2)

for transfer_node in transfer_nodes:
    line_transfer_nodes_dict[transfer_node[0]].append((transfer_node, node_id_dict[transfer_node]))

for line, _transfer_nodes in line_transfer_nodes_dict.items():
    _transfer_nodes.sort(key=lambda x: x[1])
    for i in range(len(_transfer_nodes)-1):
        tnode1, tid1 = _transfer_nodes[i]
        tnode2, tid2 = _transfer_nodes[i+1]

        line_nodes = line_node_dict[line]
        lid1 = node_lid_dict[tnode1]
        lid2 = node_lid_dict[tnode2]
        if lid1 > lid2:
            path = line_nodes[lid2:lid1+1][::-1]
        else:
            path = line_nodes[lid1:lid2+1]
        weight = sum(G[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
        TG.add_edge(tnode1, tnode2, weight=weight)

# TODO 빈 리스트 존재, 시청(종점) 노드의 인접 환승역에 시청 추가
segmentt = []
for line, nodes in line_node_dict.items():
    prev = 0
    prev_tnode = None

    segment = []
    t_point= []
    for _transfer_node in line_transfer_nodes_dict[line]:
        tid = node_lid_dict[_transfer_node[0]]
        segment.append(nodes[prev:tid])
        if not prev_tnode: t_point.append([_transfer_node[0]])
        else: t_point.append([prev_tnode, _transfer_node[0]])
        prev = tid+1
        prev_tnode = _transfer_node[0]

    segment.append(nodes[prev:])
    t_point.append([prev_tnode])

    for i, seg in enumerate(segment):
        for node in seg:
            node_adjacent_transfer_dict[node] = t_point[i]

    segmentt.append(segment)

G.add_edge(('2', '시청'), ('2', '시청(종점)'), weight=0.0000001)
TG.add_edge(('2', '충정로'), ('2', '시청(종점)'), weight = 2)
TG.add_edge(('2', '시청'), ('2', '시청(종점)'), weight=0.0000001)
node_adjacent_transfer_dict[('2', '시청(종점)')].append(('2', '시청'))

segment_lengths = []
for segments in segmentt:
    for segment in segments:
        segment_lengths.append(len(segment))

length_counts = Counter(segment_lengths)
print(length_counts)
print(sum(segment_lengths)/len(segment_lengths))

# print(len(node_id_dict))
# print(len(transfer_nodes))
# print(G)
# print('== node_id_dict ==')
# print(node_id_dict)
# print('== id_node_dict ==')
# print(id_node_dict)
# print('== name_lines_dict ==')
# print('== line_node_dict ==')
# print(line_node_dict)
# print(name_lines_dict)
# print('== transfer_nodes ==')
# print(transfer_nodes)
# print('== transfer_nodes_list ==')
# print(transfer_nodes_list)
# print('== line_transfer_nodes_dict ==')
# print(line_transfer_nodes_dict)
# print(sum([len(v) for v in line_transfer_nodes_dict.values()]))
# print('== node_lid_dict ==')
# print(node_lid_dict)
# print('== node_adjacent_transfer_dict ==')
# print(node_adjacent_transfer_dict)
print('== G ==')
print(G)
# print(G.edges(data=True))
print('== TG ==')
print(TG)
# print(TG.edges(data=True))
#
#
# # visualization
# def visualize_graph(G):
#     plt.rc('font', family='Malgun Gothic')
#     plt.rcParams['axes.unicode_minus'] = False
#
#     pos = nx.kamada_kawai_layout(G)
#     plt.figure(figsize=(12, 12))
#
#     color = {
#         '1':'blue',
#         '2':'green',
#         '3':'orange',
#         '4': 'skyblue',
#         '5':'purple'
#     }
#
#     nx.draw(
#         G,
#         pos,
#         with_labels=True,
#         labels={node: node for node in G.nodes()},
#         node_size=30,
#         node_color=[color[node[0]] for node in G.nodes()],
#         font_size=10,
#         font_family='Malgun Gothic',
#         edge_color='gray',
#         linewidths=0.5
#     )
#
#     # 간선 가중치 라벨 그리기
#     edge_labels = nx.get_edge_attributes(G, 'weight')
#     nx.draw_networkx_edge_labels(
#         G,
#         pos,
#         edge_labels=edge_labels,
#         font_size=8,
#         font_family='Malgun Gothic'
#     )
#
#     plt.axis('off')
#     plt.show()
# visualize_graph(G)
# visualize_graph(TG)

# import matplotlib.pyplot as plt
# from collections import Counter
#
# # 간선 가중치 추출 및 빈도 계산
# weights = [data['weight'] for _, _, data in TG.edges(data=True)]
# counter = Counter(weights)
#
# # 막대그래프 그리기
# plt.figure(figsize=(8, 4))
# plt.bar(counter.keys(), counter.values(), color='skyblue', edgecolor='gray')
# plt.xlabel('weight')
# plt.ylabel('frequency')
# plt.title('Edge Weight Frequency Distribution')
# plt.xticks(sorted(counter.keys()))
# plt.show()




