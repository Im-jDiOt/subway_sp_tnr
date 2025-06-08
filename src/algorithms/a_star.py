from src.data.data_structure import heappush, heappop
from src.data.process_data_w_branch_express_1 import subway_lines


def a_star_with_real_transfer_penalty(graph, start, goal, heuristic_func):
    queue = []
    heappush(queue, (0, 0, start))
    visited = set()
    dist = {start: 0}
    prev = {}

    while queue:
        f, g, current = heappop(queue)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            break

        for neighbor, weight in graph[current]:
            is_transfer = current[0] != neighbor[0]
            transfer_penalty = 2 if is_transfer else 0
            tentative_g = g + weight + transfer_penalty

            if neighbor not in dist or tentative_g < dist[neighbor]:
                dist[neighbor] = tentative_g
                h = heuristic_func(neighbor, goal)
                f = tentative_g + h
                heappush(queue, (f, tentative_g, neighbor))
                prev[neighbor] = current

    # ===== 경로 복원 =====
    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = prev.get(cur)
        if cur is None:
            return None, float('inf')  # 경로 없음
    path.append(start)
    path.reverse()
    return path, dist[goal]

# 1. 역 이름 일치 기반 (단순)
def h_station_name(current, goal):
    return 0 if current[1] == goal[1] else 2

# 2. 환승 예측 기반 (station_to_lines 활용)
def h_transfer_required(current, goal):
    if current[1] == goal[1]:
        return 0  # 같은 역이면 환승 없음
    cur_lines = set(subway_lines.get(current[1], []))
    goal_lines = set(subway_lines.get(goal[1], []))
    return 0 if cur_lines & goal_lines else 2  # 공통 노선이 있으면 환승 X

def h_index_distance(current, goal):
    if current[0] == goal[0]:
        try:
            idx1 = subway_lines[current[0]].index(current[1])
            idx2 = subway_lines[goal[0]].index(goal[1])
            return abs(idx1 - idx2) * 1
        except ValueError:
            pass  # 아래로 넘어감
    # 노선 다르거나 예외 시: 보수적 + 환승 고려
    return h_transfer_required(current, goal) + 1  # 최소 환승 2분 + 완만한 보정

# 4. 혼합 휴리스틱 (추천) — 위 3개 조합
def h_combined(current, goal):
    name_h = h_station_name(current, goal)
    transfer_h = h_transfer_required(current, goal)
    index_h = h_index_distance(current, goal)
    return max(name_h, transfer_h) + index_h // 2

#앙상블 구조
def h_ensemble_min(current, goal):
    return min(
        h_station_name(current, goal),
        h_transfer_required(current, goal),
        h_index_distance(current, goal)
    )
