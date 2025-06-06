from data.process_data_w_branch_express_1 import station_to_nodes
from data.data_structure import MinHeap

# --- 다익스트라 알고리즘 (MinHeap 사용) ---
def dijkstra_custom_pq(graph, start_station_name, end_station_name):
    start_nodes = station_to_nodes.get(start_station_name, [])
    end_nodes = station_to_nodes.get(end_station_name, [])

    if not start_nodes:
        return f"오류: 출발역 '{start_station_name}'을(를) 찾을 수 없습니다.", None
    if not end_nodes:
        return f"오류: 도착역 '{end_station_name}'을(를) 찾을 수 없습니다.", None

    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}

    pq = MinHeap()

    for s_node in start_nodes:
        dist[s_node] = 0
        pq.push((0, s_node))

    min_cost = float('inf')
    final_end_node = None

    while not pq.is_empty():
        cost, u = pq.pop()

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
                pq.push((new_cost, v))

    if final_end_node:
        path = []
        curr = final_end_node
        while curr:
            path.append(curr)
            curr = prev[curr]
        final_path = list(reversed(path))

        # 경로 출력 형식 맞추기
        formatted_path = []
        for i, (line, station) in enumerate(final_path):
            if i == 0:
                formatted_path.append(f"출발: [{line}호선] {station}")
            else:
                prev_line, prev_station = final_path[i-1]
                if line.split(' ')[0][0] != prev_line.split(' ')[0][0]: # 호선 번호가 다르면
                    formatted_path.append(f"환승: [{prev_line}호선] {prev_station} -> [{line}호선] {station}")
                elif line != prev_line: # 같은 호선 내 지선/본선 변경
                     formatted_path.append(f"환승: [{prev_line} -> {line}] {station}")
                else:
                    formatted_path.append(f"이동: {prev_station} -> {station} ({line}호선)")

        return f"최소 시간: {min_cost}분", formatted_path
    else:
        return f"경로를 찾을 수 없습니다.", None