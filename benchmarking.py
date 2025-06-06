import random
import time
import csv

# ======= (1) 데이터 로드 =======
# -- 1단계 (a_star, dijkstra_1)
from data.process_data_w_branch_express_1 import graph as graph1, station_to_nodes as station_to_nodes1
from a_star import a_star_with_real_transfer_penalty, h_station_name, h_transfer_required, h_index_distance, h_combined, h_ensemble_min
import dijkstra_1

# -- 2단계 (ucs_and_dijkstra_2)
from data.process_data_w_branch_express_2 import graph_step2, station_to_nodes_step2
from ucs_and_dijkstra_2 import ucs_shortest_path_heapq as ucs2, dijkstra_shortest_path_heapq as dijkstra2

# -- 3단계 (ucs_and_dijkstra_3)
from data.process_data_w_branch_express_3 import graph_step3, station_to_nodes_step3
from ucs_and_dijkstra_3 import ucs_shortest_path_step3 as ucs3, dijkstra_shortest_path_step3 as dijkstra3

# -- transit_node_routing
from transit_node_routing import transit2transit, transit2transit_dial, transit_node_routing
from data.process_data_w_weight import TG

# ======= (2) 함수형 유틸 =======
def get_random_node_pairs(node_list, num_pairs=1000):
    pairs = set()
    nodes = list(node_list)
    while len(pairs) < num_pairs:
        start, end = random.sample(nodes, 2)
        pairs.add((start, end))
    return list(pairs)

def get_random_station_name_pairs(station_to_nodes, num_pairs=1000):
    stations = list(station_to_nodes.keys())
    pairs = set()
    while len(pairs) < num_pairs:
        s, e = random.sample(stations, 2)
        pairs.add((s, e))
    return list(pairs)

def measure_execution_time(func, pairs, desc='', verbose=False):
    t0 = time.time()
    results = []
    for start, end in pairs:
        result = func(start, end)
        results.append(result)
    t1 = time.time()
    total_time = t1 - t0
    avg_time = total_time / len(pairs)
    if verbose:
        print(f"== {desc} ==")
        print(f"  Total time: {total_time:.4f} sec")
        print(f"  Avg time: {avg_time*1000:.3f} ms")
    return total_time, avg_time, results

def measure_precomputation_and_execution(precompute_func, solve_func, pairs, desc='', verbose=False):
    t0 = time.time()
    precomp = precompute_func()
    t1 = time.time()
    precomp_time = t1 - t0

    t2 = time.time()
    results = []
    for start, end in pairs:
        result = solve_func(start, end, precomp)
        results.append(result)
    t3 = time.time()
    exec_time = t3 - t2

    total_time = precomp_time + exec_time
    avg_time = total_time / len(pairs)
    if verbose:
        print(f"== {desc} ==")
        print(f"  Precomputation: {precomp_time:.4f} sec, Execution: {exec_time:.4f} sec")
        print(f"  Total: {total_time:.4f} sec, Avg: {avg_time*1000:.3f} ms")
    return precomp_time, exec_time, total_time, avg_time, results

def print_individual_costs(algorithm_name, func, pairs):
    costs = []
    print(f'\n== {algorithm_name} ==')
    for idx, (start, end) in enumerate(pairs):
        cost = func(start, end)
        print(f"[{idx}] start: {start}, end: {end}, cost: {cost}")
        costs.append(cost)
    # summary
    valid_costs = [c for c in costs if c != float('inf')]
    print(f"  -- total: {len(costs)}개, 유효경로: {len(valid_costs)}개")
    if valid_costs:
        print(f"  -- min: {min(valid_costs)}, max: {max(valid_costs)}, avg: {sum(valid_costs)/len(valid_costs):.2f}")
    else:
        print("  -- 유효경로 없음")

# ======= (3) 각 실험 =======
def run_experiments():
    print('\n===== 실험 결과 비교 (process_data_w_branch_express_1.py) =====')
    # 1. (노선, 역) 전체 노드 쌍
    node_list1 = list(graph1.keys())
    pairs1 = get_random_node_pairs(node_list1, 1000)
    # --- A* 모든 휴리스틱 비교
    heuristics = [
        ('h_station_name', h_station_name),
        ('h_transfer_required', h_transfer_required),
        ('h_index_distance', h_index_distance),
        ('h_combined', h_combined),
        ('h_ensemble_min', h_ensemble_min)
    ]
    for h_name, h_func in heuristics:
        def a_star_func(start, end):
            path, cost = a_star_with_real_transfer_penalty(graph1, start, end, h_func)
            return cost
        total, avg, _ = measure_execution_time(a_star_func, pairs1)
        print(f'A*: {h_name:>15} | total: {total:.3f}s | avg: {avg*1000:.3f}ms')

    # --- Dijkstra (노선,역) signature로 변경
    def dijkstra_func(start, end):
        _, path = dijkstra_1.dijkstra_custom_pq(graph1, start, end)
        if path is None:
            return float('inf')
        else:
            return len(path) - 1  # 또는 직접 비용 계산
    total, avg, _ = measure_execution_time(dijkstra_func, pairs1)
    print(f'Dijkstra:             | total: {total:.3f}s | avg: {avg*1000:.3f}ms')

    print('\n===== 실험 결과 비교 (process_data_w_branch_express_2.py) =====')
    # === 랜덤 페어를 "역이름"으로 만듦 ===
    pairs2 = get_random_station_name_pairs(station_to_nodes_step2, 1000)
    total, avg, _ = measure_execution_time(lambda s, e: ucs2(graph_step2, s, e)[1], pairs2)
    print(f'UCS:                  | total: {total:.3f}s | avg: {avg*1000:.3f}ms')
    total, avg, _ = measure_execution_time(lambda s, e: dijkstra2(graph_step2, s, e)[1], pairs2)
    print(f'Dijkstra:             | total: {total:.3f}s | avg: {avg*1000:.3f}ms')

    print('\n===== 실험 결과 비교 (process_data_w_branch_express_3.py) =====')
    # === 랜덤 페어를 "역이름"으로 만듦 ===
    pairs3 = get_random_station_name_pairs(station_to_nodes_step3, 1000)
    total, avg, _ = measure_execution_time(lambda s, e: ucs3(graph_step3, s, e)[1], pairs3)
    print(f'UCS:                  | total: {total:.3f}s | avg: {avg*1000:.3f}ms')
    total, avg, _ = measure_execution_time(lambda s, e: dijkstra3(graph_step3, s, e)[1], pairs3)
    print(f'Dijkstra:             | total: {total:.3f}s | avg: {avg*1000:.3f}ms')

    print('\n===== 실험 결과 비교 (test_nodes.csv) =====')
    test_pairs = []
    with open('test_nodes.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            test_pairs.append( ((row[0], row[1]), (row[2], row[3])) )
    # t2t: transit2transit
    print('== t2t: transit2transit ==')
    precomp, exec, total, avg, _ = measure_precomputation_and_execution(
        lambda: transit2transit(TG),
        lambda s, e, t2t: transit_node_routing(s, e, t2t)[1],
        test_pairs
    )
    print(f'  Precomp: {precomp:.3f}s, Exec: {exec:.3f}s, Total: {total:.3f}s, Avg: {avg*1000:.3f}ms')

    # t2t: transit2transit_dial
    print('== t2t: transit2transit_dial ==')
    precomp, exec, total, avg, _ = measure_precomputation_and_execution(
        lambda: transit2transit_dial(TG),
        lambda s, e, t2t: transit_node_routing(s, e, t2t)[1],
        test_pairs
    )
    print(f'  Precomp: {precomp:.3f}s, Exec: {exec:.3f}s, Total: {total:.3f}s, Avg: {avg*1000:.3f}ms')

# ===== UCS/Dijkstra 개별 출력 =====
def run_and_print_individual_costs():
    # 2단계
    pairs2 = get_random_station_name_pairs(station_to_nodes_step2, 30)
    print_individual_costs(
        "UCS (step2)",
        lambda s, e: ucs2(graph_step2, s, e)[1],
        pairs2
    )
    print_individual_costs(
        "Dijkstra (step2)",
        lambda s, e: dijkstra2(graph_step2, s, e)[1],
        pairs2
    )
    # 3단계
    pairs3 = get_random_station_name_pairs(station_to_nodes_step3, 30)
    print_individual_costs(
        "UCS (step3)",
        lambda s, e: ucs3(graph_step3, s, e)[1],
        pairs3
    )
    print_individual_costs(
        "Dijkstra (step3)",
        lambda s, e: dijkstra3(graph_step3, s, e)[1],
        pairs3
    )

if __name__ == '__main__':
    run_experiments()
    # run_and_print_individual_costs()  # 필요 시 주석 해제하여 개별 비용도 출력

# result
# ===== 실험 결과 비교 (process_data_w_branch_express_1.py) =====
# A*:  h_station_name | total: 0.412s | avg: 0.412ms
# A*: h_transfer_required | total: 0.463s | avg: 0.463ms
# A*: h_index_distance | total: 0.477s | avg: 0.477ms
# A*:      h_combined | total: 0.612s | avg: 0.612ms
# A*:  h_ensemble_min | total: 0.640s | avg: 0.640ms
# Dijkstra:             | total: 0.522s | avg: 0.522ms
#
# ===== 실험 결과 비교 (process_data_w_branch_express_2.py) =====
# UCS:                  | total: 0.252s | avg: 0.252ms
# Dijkstra:             | total: 0.367s | avg: 0.367ms
#
# ===== 실험 결과 비교 (process_data_w_branch_express_3.py) =====
# UCS:                  | total: 0.302s | avg: 0.302ms
# Dijkstra:             | total: 0.417s | avg: 0.417ms
#
# ===== 실험 결과 비교 (test_nodes.csv) =====
# == t2t: transit2transit ==
#   Precomp: 0.008s, Exec: 0.019s, Total: 0.027s, Avg: 0.027ms
# == t2t: transit2transit_dial ==
#   Precomp: 0.067s, Exec: 0.021s, Total: 0.088s, Avg: 0.088ms
