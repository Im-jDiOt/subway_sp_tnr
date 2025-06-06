# --- 알고리즘 정의 (heapq 라이브러리 사용, 단계 3 그래프 사용) ---
# UCS 함수 (단계 2와 동일하지만 graph_step3 사용)
import heapq
from data.process_data_w_branch_express_3 import station_to_nodes_step3


def ucs_shortest_path_step3(graph, start_station_name, end_station_name):
    start_nodes = station_to_nodes_step3.get(start_station_name, [])
    end_nodes = station_to_nodes_step3.get(end_station_name, [])

    if not start_nodes or not end_nodes: return None, float('inf')

    pq = [] # (cost, node, path)
    visited_cost = {}

    for s_node in start_nodes:
      if s_node not in visited_cost or 0 < visited_cost[s_node]:
        heapq.heappush(pq, (0, s_node, [s_node]))
        visited_cost[s_node] = 0

    min_cost = float('inf')
    shortest_path = None

    while pq:
        cost, node, path = heapq.heappop(pq)

        if cost > visited_cost.get(node, float('inf')):
            continue

        if node in end_nodes: # 목표 노드에 도달했으면 (여러 목표 노드 중 최소값)
          return path, cost

        for neighbor, weight in graph[node]:
            new_cost = cost + weight
            if new_cost < visited_cost.get(neighbor, float('inf')):
                visited_cost[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

    return None, float('inf')

# 다익스트라 함수 (단계 2와 동일하지만 graph_step3 사용)
def dijkstra_shortest_path_step3(graph, start_station_name, end_station_name):
    start_nodes = station_to_nodes_step3.get(start_station_name, [])
    end_nodes = station_to_nodes_step3.get(end_station_name, [])
    if not start_nodes or not end_nodes: return None, float('inf')

    pq = [] # (cost, node)
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}

    for s_node in start_nodes:
        dist[s_node] = 0
        heapq.heappush(pq, (0, s_node))

    min_cost = float('inf')
    final_end_node = None

    while pq:
        cost, u = heapq.heappop(pq)

        if cost > dist[u]:
            continue

        if u in end_nodes:
            if cost < min_cost:
                min_cost = cost
                final_end_node = u
            continue

        for v, weight in graph[u]:
            new_cost = cost + weight
            if new_cost < dist[v]:
                dist[v] = new_cost
                prev[v] = u
                heapq.heappush(pq, (new_cost, v))

    if final_end_node:
        path = []
        curr = final_end_node
        while curr:
            path.append(curr)
            curr = prev[curr]
        return list(reversed(path)), min_cost
    else:
        return None, float('inf')
