import networkx as nx
from src.data.process_data_w_weight import node_adjacent_transfer_dict, line_node_dict, G, TG, \
    transfer_nodes

def node2transit(node):
    """'
    :param node: (line, name)
    :type node: tuple
    :return: (all possible path= [node1, node2, ...] and time = minutes), adjacent transfer nodes=[tnode1, tnode2]
    :rtype: list

    입력으로 노드를 받음.
    해당 노드의 인접 환승역, 인접 환승역까지의 경로, 시간을 반환함.
    이 때 경로는 방향을 고려함.

    노드에서 인접 환승역까지의 path는
    그냥 단일한 라인 경로에서 환승 없이 이루어지는 단순한 경로이기에
    슬라이스를 통해 구현을 함.
    -> O(v') 시간 복잡도 (이 때 v'은 잘린 경로의 노드 수이며 이는 v에 비해 정말정말 작음. )

    time 또한 단순히 경로의 가중치를 합하는 걸로 해서 마찬가지로 O(v') 시간 복잡도.

    path = nx.shortest_path(G, source=node, target=tnode, weight='weight')
    time = nx.shortest_path_length(G, source=node, target=tnode, weight='weight')
    이렇게 구현하면 (O((E + V) log V)) 걸리는데 이를 꽤나 줄일 수 있음.
    """
    line, name = node
    res = []
    if node in transfer_nodes:
        return [([node], 0), [node]]
    if node == ('2', '시청(종점)'):
        return [([('2', '시청(종점)'), ('2', '충정로')], 2), ([('2', '시청(종점)'), ('2', '시청')], 0), [('2', '충정로'), ('2', '시청')]]
    for tnode in (tnodes:=node_adjacent_transfer_dict[node]):
        line_path = line_node_dict[line]
        node_idx = line_path.index(node)
        tnode_idx = line_path.index(tnode)
        if node_idx > tnode_idx:
            path = line_path[tnode_idx:node_idx+1][::-1]
            time = sum(G[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
        else:
            path=line_path[node_idx:tnode_idx+1]
            time = sum(G[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
        res.append((path, time))
    res.append(tnodes)
    return res

def transit2transit(tg):
    """
    :param tg: transfer graph
    :type tg: networkx.Graph
    :return: all possible combinations of the shortest transfer paths and their times {(tnode1, tnode2) : (path, time)}
    :rtype: dict

    APSP 알고리즘을 사용해 transit hash table을 만드는
    transit node routing에서 가장 핵심적인 부분!!

    일단 여기에선 nx에서 제공하는 기본적인 apsp 알고리즘(dijkstra로 구현되어 있음)을 사용함.
    이 알고리즘은 O((E + VlogV) V) 시간 복잡도를 가짐.
    """
    res = {}

    all_pairs = dict(nx.all_pairs_dijkstra(tg, weight='weight'))

    for source in tg.nodes:
        distances, paths = all_pairs[source]

        for target in tg.nodes:
            if source != target:
                path = paths[target]
                time = distances[target]

                res[(source, target)] = (path, time)
            else:
                res[(source, target)] = ([source], 0)

    return res


import math
from collections import deque

def transit2transit_dial(tg):
    """
    :param tg: transfer graph (networkx.Graph)
    :return: {(tnode1, tnode2): (path, time)} 형태의 APSP 결과
    """

    def single_source_dial(graph, source):
        """
        Dial's algorithm을 이용해 단일 출발점(source)에서 다른 모든 노드까지
        최단 경로 거리(distances)와 predecessor(경로 재구성용)를 구한다.
        시간복잡도는 O((CV+E)V) 임. 이때 C는 엣지 가중치의 최대값.

        Returns:
            distances: {node: 최단거리(int or float('inf'))}
            predecessor: {node: 해당 노드로 최단 경로를 따라갈 때 직전 노드}
        """
        # 1) 모든 노드의 거리를 무한대로 초기화, source는 0
        distances = {v: math.inf for v in graph.nodes()}
        predecessor = {}
        distances[source] = 0  # source까지 거리는 0

        # 2) 그래프 전체에서 “정수” 엣지 가중치의 최댓값 W를 구한다
        #    (실제로 graph[u][v]['weight']가 2.0 같은 실수형일 수 있으므로 int()로 변환)
        W = 0
        for u, v, data in graph.edges(data=True):
            w_raw = data.get('weight', 1)
            w_int = int(w_raw)
            if w_int > W:
                W = w_int

        # 3) 노드 개수 n, 최대 거리(max_dist) = W * (n - 1)
        n = graph.number_of_nodes()
        max_dist = W * (n - 1)

        # 4) 버킷 배열(buckets) 생성: 거리 d마다 해당 거리에 속한 노드들(deque) 저장
        #    인덱스 0부터 max_dist까지
        buckets = [deque() for _ in range(max_dist + 1)]
        buckets[0].append(source)

        # 5) 거리 idx = 0부터 max_dist까지 순서대로 버킷을 탐색하며 노드를 꺼내 처리
        idx = 0
        while idx <= max_dist:
            # 현재 버킷에 노드가 없으면 다음 idx로
            if not buckets[idx]:
                idx += 1
                continue

            u = buckets[idx].popleft()
            # 이미 더 작은 거리로 처리된 노드라면 건너뛰기
            if distances[u] < idx:
                continue

            # 인접한 간선들을 완화(relax)한다.
            for v in graph.neighbors(u):
                # 엣지 가중치를 정수로 변환
                w_raw = graph[u][v].get('weight', 1)
                w_int = int(w_raw)
                new_dist = distances[u] + w_int

                # 만약 new_dist가 기존 distances[v]보다 작으면 갱신
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessor[v] = u
                    # new_dist가 max_dist 이하일 때만 해당 버킷에 추가
                    if new_dist <= max_dist:
                        buckets[new_dist].append(v)
            # 같은 idx 버킷에 아직 노드가 남아있다면 계속 처리 (while idx 고정)

        return distances, predecessor

    # 6) 각 노드를 source로 하여 Dial-based SSSP를 실행하고, 경로(path)와 거리(time)를 재구성
    res = {}
    for source in tg.nodes():
        distances, pred = single_source_dial(tg, source)
        for target in tg.nodes():
            if source == target:
                # 자기 자신으로 가는 경로: [source], 시간 0
                res[(source, target)] = ([source], 0)
            else:
                if distances[target] == math.inf:
                    # 도달 불가능한 경우: 빈 경로, 무한대 시간
                    res[(source, target)] = ([], math.inf)
                else:
                    # predecessor를 따라 역으로 거슬러 올라가며 경로 reconstruct
                    path = []
                    cur = target
                    while cur != source:
                        path.append(cur)
                        cur = pred[cur]
                    path.append(source)
                    path.reverse()
                    res[(source, target)] = (path, distances[target])

    return res


def transit_node_routing(node1, node2, t2t):
    """
    :param node1: (line, name) of the first node
    :type node1: tuple
    :param node2: (line, name) of the second node
    :type node2: tuple
    :param t2t: transfer to transfer hash table
    :type t2t: dict
    :return: the shortest paths and their times between two nodes
    :rtype:  tuple

    노드1에서 노드2까지의 경로를 찾는 함수.
    노드1과 노드2가 같은 라인 segment에 있는 경우에는 그냥 단순히 슬라이스로 경로를 찾음.
    만약 다른 라인에 있다면, 환승역을 거쳐서 가는 경로를 찾아야 함.

if share transfer:
    if x and y are in same line segment
        return slice of line segment
    if x and y are in different line segment but share same transfer node(which means two nodes are in same line)
        if not len(adjacent transfer nodes of x) == 2 & len(adjacent transfer nodes of y) == 2:
            return slice of line
        if len(adjacent transfer nodes of x) == 2 & len(adjacent transfer nodes of y) == 2:
            return min(slice of line, path w/ apsp)
if not share transfer:
    return min of x to y path transit transfer node
    """
    if node1==node2: # 1
        return [node1], 0

    *node2transit_cases1, adjacent_transfers1 = node2transit(node1)
    *node2transit_cases2, adjacent_transfers2 = node2transit(node2)
    common_transfers = set(adjacent_transfers1) & set(adjacent_transfers2) # 2,3,4,5

    if common_transfers:
        cond1 = adjacent_transfers1 == adjacent_transfers2 # 2,4,5
        cond2 = node1 in transfer_nodes # 3
        cond3 = node2 in transfer_nodes # 3
        if cond1 or cond2 or cond3: # case1: x&y are in the same line segment
            line1=node1[0]
            line_path = line_node_dict[line1]
            node1_idx = line_path.index(node1)
            node2_idx = line_path.index(node2)
            if node1_idx > node2_idx:
                path = line_path[node2_idx:node1_idx + 1][::-1]
                time = sum(G[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
            else:
                path = line_path[node1_idx:node2_idx + 1]
                time = sum(G[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
            return path, time
        else: # 6,7,8 case2: x&y share common transfer node
            common_transfer = common_transfers.pop()
            path1, time1 = node2transit_cases1[adjacent_transfers1.index(common_transfer)]
            path2, time2 = node2transit_cases2[adjacent_transfers2.index(common_transfer)]
            path = path1 + path2[1:] # path2[::-1][1:]
            time = time1 + time2
            if len(adjacent_transfers1)==2 and len(adjacent_transfers2)==2:
                tnode1 = [t for t in adjacent_transfers1 if t != common_transfer][0]
                tnode2 = [t for t in adjacent_transfers2 if t != common_transfer][0]
                node12transfer_path, node12transfer_time = node2transit_cases1[adjacent_transfers1.index(tnode1)]
                node22transfer_path, node22transfer_time = node2transit_cases2[adjacent_transfers2.index(tnode2)]
                transfer2transfer_path, transfer2transfer_time = t2t[(tnode1, tnode2)]
                path2 = node12transfer_path + transfer2transfer_path[1:-1] + node22transfer_path[::-1]
                time2 = node12transfer_time + transfer2transfer_time + node22transfer_time
                if time2<time:
                    return path2, time2
            return path, time
    else:
        min_time = float('inf')
        res = None
        for i1, tnode1 in enumerate(adjacent_transfers1):
            for i2, tnode2 in enumerate(adjacent_transfers2):
                node12transfer_path, node12transfer_time = node2transit_cases1[i1]
                node22transfer_path, node22transfer_time = node2transit_cases2[i2]
                transfer2transfer_path, transfer2transfer_time = t2t[(tnode1, tnode2)]
                time = node12transfer_time + transfer2transfer_time + node22transfer_time
                if time < min_time:
                    min_time = time
                    path = node12transfer_path + transfer2transfer_path[1:-1] + node22transfer_path[::-1]
                    res = (path, time)
        return res


if __name__ == "__main__":
    GREEN = '\033[92m'  # 초록색
    RED = '\033[91m'  # 빨간색
    RESET = '\033[0m'  # 색상 초기화

    # NUM_OF_TEST = 1000
    #
    # all_g_nodes = list(G.nodes)
    # test_nodes = []
    # error_msgs = []
    # with open('test_nodes.csv', 'r', encoding='utf-8') as f:
    #     reader = csv.reader(f)
    #     next(reader)
    #     for row in reader:
    #         node1 = (row[0], row[1])
    #         node2 = (row[2], row[3])
    #         test_nodes.append([node1, node2])
    #
    # # for _ in range(NUM_OF_TEST):
    # #     node1 = random.choice(all_g_nodes)
    # #     node2 = random.choice(all_g_nodes)
    # #     test_nodes.append([node1, node2])
    #
    # print('== Precomputing transit2transit table ==')
    # precomputed_start_time = time.time()
    # t2t_table = transit2transit(TG)
    # # t2t_table = transit2transit_dial(TG)
    # precomputed_end_time = time.time()
    # precomputed_time = precomputed_end_time - precomputed_start_time
    # print('Precomputed transit2transit table in {:.6f} seconds'.format(precomputed_time))
    #
    # total_execution_time = 0
    #
    # for i, (node1, node2) in enumerate(test_nodes):
    #     print(f'\n== Test Case {i+1}/{len(test_nodes)}: {node1} -> {node2} ==')
    #     start_time = time.time()
    #     try:
    #         my_path, my_time = transit_node_routing(node1, node2, t2t_table)
    #         end_time = time.time()
    #         execution_time = end_time - start_time
    #         total_execution_time += execution_time
    #
    #         print(f'Execution time: {execution_time:.6f} seconds')
    #         print('My path:', my_path)
    #         print('My time:', int(my_time) if isinstance(my_time, (int, float)) else my_time)
    #
    #         answer_path = nx.dijkstra_path(G, source=node1, target=node2, weight='weight')
    #         answer_time = nx.dijkstra_path_length(G, source=node1, target=node2, weight='weight')
    #         print('Answer path:', answer_path)
    #         print("Answer time", int(answer_time))
    #
    #         if int(my_time) == int(answer_time):
    #             print(f'{GREEN}Success!{RESET}')
    #         else:
    #             print(f'{RED}Fail!{RESET}')
    #             print(f'My time: {int(my_time)}, Answer time: {int(answer_time)}')
    #             print(f'My path: {my_path}, Answer path: {answer_path}')
    #             error_msgs.append(f'Fail for [{node1}, {node2}]: My time: {int(my_time)}, Answer time: {int(answer_time)}')
    #     except Exception as e:
    #         print(f'{RED}Error during transit_node_routing for [{node1}, {node2}]: {e}{RESET}')
    #         error_msgs.append(f'Error for [{node1}, {node2}]: {e}')
    #
    # print(f"precompuation+execution: {precomputed_time + total_execution_time:.6f} seconds")
    # print(f"avg execution per {NUM_OF_TEST} test case: {(total_execution_time) / NUM_OF_TEST:.6f} seconds")
    # print(f"avg precompuation+execution per {NUM_OF_TEST} test case: {(precomputed_time +total_execution_time)/ NUM_OF_TEST:.6f} seconds")
    #
    # if error_msgs:
    #     print(f'\n{RED}Errors encountered during tests:{RESET}')
    #     for msg in error_msgs:
    #         print(msg)

    # import csv
    #
    # # test_nodes: [(node1, node2), ...] 또는 [[node1, node2], ...] 형태
    # with open('test_nodes.csv', 'w', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['node1_line', 'node1_name', 'node2_line', 'node2_name'])
    #     for node1, node2 in test_nodes:
    #         writer.writerow([node1[0], node1[1], node2[0], node2[1]])


    case1_1 = [('1', '창동'), ('1', '창동')]
    case1_1_2 = [('3', '수서'), ('3', '수서')]
    case2_2 = [('1', '도봉'), ('1', '창동')]
    case2_3 = [('4', '미아'), ('4', '창동')]
    case2_4 = [('1', '지행'), ('1', '청산')]
    case2_5 = [('3', '수서'), ('3', '양재')]
    case3_6 = [('1','도봉'), ('4', '노원')]
    case3_7 = [('3', '수서'), ('5', '개롱')]
    case3_8 = [('1', '관악'), ('4', '과천')]
    case4_9 = [('1', '동대문'), ('5', '충정로')]
    case4_10 = [('4', '노원'), ('5', '충정로')]
    case4_11 = [('4', '미아'), ('5', '영등포구청')]
    case4_12 = [('3', '주엽'), ('1', '오산')]
    case4_13 = [('3', '옥수'), ('4', '반월')]
    case4_14 = [('3', '옥수'), ('1', '관악')]

    test_case = [('5', '광화문'), ('2', '을지로입구')]
    test_case2 = [('2', '충정로'), ('2', '시청')]
    test_case3 = [('1', '의정부'), ('2', '홍대입구')]

    error_case1 = [('1', '보산'), ('1', '동묘앞')]
    error_case2 = [('1', '회기'), ('4', '동대문역사문화공원')]
    error_case3 = [('2', '서초'), ('2', '역삼')]

    test_nodes = [test_case3]

    for node1, node2 in test_nodes:
        print(f'== {node1} -> {node2} ==')
        my_path, my_time = transit_node_routing(node1, node2, transit2transit(TG))
        answer_path = nx.dijkstra_path(G, source=node1, target=node2, weight='weight')
        answer_time = nx.dijkstra_path_length(G, source=node1, target=node2, weight='weight')

        print('My path:', my_path)
        print('My time:', int(my_time))
        print('Answer path:', answer_path)
        print('Answer time:', answer_time)
        if int(my_time) == int(answer_time):
            print(f'{GREEN}Success!{RESET}')
        else:
            print(f'{RED}Fail!{RESET}')








