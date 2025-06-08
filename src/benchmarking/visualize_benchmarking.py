import matplotlib.pyplot as plt

labels = [
    "A* (h_station_name)", "A* (h_transfer_required)", "A* (h_index_distance)",
    "A* (h_combined)", "A* (h_ensemble_min)", "Dijkstra (step1)",
    "UCS (step2)", "Dijkstra (step2)",
    "UCS (step3)", "Dijkstra (step3)",
    "TNR (transit2transit)", "TNR (transit2transit_dial)"
]

avg_times = [
    0.412, 0.463, 0.477, 0.612, 0.640, 0.522,      # step1
    0.252, 0.367,                                   # step2
    0.302, 0.417,                                   # step3
    0.027, 0.088                                    # TNR
]

# 색상 정의 (step1, step2, step3, TNR)
colors = (
    ['#4F8BC9'] * 6 +    # step1 (A*, Dijkstra) - cobalt blue
    ['#E25278'] * 2 +    # step2 (UCS, Dijkstra) - deep pink
    ['#7BC96F'] * 2 +    # step3 (UCS, Dijkstra) - pale green
    ['#FFD700'] * 2  # TNR - gold
)

plt.figure(figsize=(11, 5))
bars = plt.bar(labels, avg_times, color=colors, edgecolor='grey', alpha=0.92)

plt.xticks(rotation=30, ha='right', fontsize=10)
plt.ylabel('Avg Time per Query (ms)', fontsize=12)
plt.title('Algorithm Benchmark: Average Query Time by Dataset', fontsize=14)
plt.grid(axis='y', linestyle=':', alpha=0.4)

# 각 바에 값 표시
for bar, avg in zip(bars, avg_times):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, f'{avg:.3f}',
             ha='center', va='bottom', fontsize=9)

# 범례 (custom)
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#4F8BC9', edgecolor='grey', label='add branch'),
    Patch(facecolor='#E25278', edgecolor='grey', label='add branch2'),
    Patch(facecolor='#7BC96F', edgecolor='grey', label='add branch+express'),
    Patch(facecolor='#FFD700', edgecolor='grey', label='add weight'),
]
plt.legend(handles=legend_elements, fontsize=10, loc='upper right')

plt.tight_layout()
plt.show()
