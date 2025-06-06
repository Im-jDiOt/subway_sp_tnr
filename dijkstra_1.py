from data.data_structure import MinHeap

def dijkstra_custom_pq(graph, start_node, end_node):
    # start_node, end_node: (line, station) tuple
    if start_node not in graph:
        return f"오류: 출발노드 '{start_node}'을(를) 찾을 수 없습니다.", None
    if end_node not in graph:
        return f"오류: 도착노드 '{end_node}'을(를) 찾을 수 없습니다.", None

    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    pq = MinHeap()

    dist[start_node] = 0
    pq.push((0, start_node))

    while not pq.is_empty():
        cost, u = pq.pop()

        if cost > dist[u]:
            continue

        if u == end_node:
            path = []
            curr = end_node
            while curr:
                path.append(curr)
                curr = prev[curr]
            final_path = list(reversed(path))
            return f"최소 시간: {cost}분", final_path

        for v, weight in graph[u]:
            new_cost = cost + weight
            if new_cost < dist[v]:
                dist[v] = new_cost
                prev[v] = u
                pq.push((new_cost, v))

    return f"경로를 찾을 수 없습니다.", None