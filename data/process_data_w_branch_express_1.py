from collections import defaultdict

# phase 1
subway_lines = {
    '1': ["소요산","동두천","보산","동두천중앙","지행","덕정","덕계","양주","녹양","가능",
          "의정부","회룡","망월사","도봉산","도봉","방학","창동","녹천","월계","성북",
          "석계","신이문","외대앞","회기","청량리","제기동","신설동","동묘앞","동대문","종로5가",
          "종로3가","종각","시청","서울역","남영","용산","노량진","대방","신길","영등포",
          "신도림","구로", "가산디지털단지","독산","금천구청","석수","관악","안양","명학",
          "금정","군포","당정","의왕","성균관대","화서","수원","세류","병점","세마","오산대","오산","진위","송탄","서정리","지제","평택","성환","직산","두정",
          "천안","봉명","쌍용","아산","배방","온양온천","신창"],
    '1인천':["구로","구일","개봉","오류동","온수","역곡","소사","부천","중동",
            "송내","부개","부평","백운","동암","간석","주안","도화","제물포","도원","동인천","인천"],
    '1서동탄': ["병점","서동탄"],
    '1광명' : ["금천구청","광명"],
    '2': ["시청","을지로입구","을지로3가","을지로4가","동대문역사문화공원","신당","상왕십리",
          "왕십리","한양대","뚝섬","성수","건대입구","구의","강변","잠실나루","잠실","신천",
          "종합운동장","삼성","선릉","역삼","강남","교대","서초","방배","사당","낙성대","서울대입구",
          "봉천","신림","신대방","구로디지털단지","대림","신도림","문래","영등포구청","당산","합정",
          "홍대입구","신촌","이대","아현","충정로","시청"],
    '2신설동' : ["성수","용답","신답","용두","신설동"],
    '2까치산' : ["신도림","도림천","양천구청","신정네거리","까치산"],
    '3': ["대화","주엽","정발산","마두","백석","대곡","화정","원당","삼송","지축",
          "구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가",
          "을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원",
          "고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청",
          "일원","수서","가락시장","경찰병원","오금"],
    '4': ["진접","오남","별내별가람","당고개","상계","노원","창동","쌍문","수유","미아",
          "미아삼거리","길음","성신여대입구","한성대입구","혜화","동대문","동대문역사문화공원",
          "충무로","명동","회현","서울역","숙대입구","삼각지","신용산","이촌","동작","이수",
          "사당","남태령","선바위","경마공원","대공원","과천","정부과천청사","인덕원","평촌",
          "범계","금정","산본","수리산","대야미","반월","상록수","한대앞","중앙","고잔","공단",
          "안산","신길온천","정왕","오이도"],
    '5하남검단산': ["방화","개화산","김포공항","송정","마곡","발산","우장산","화곡","까치산","신정",
                  "목동","오목교","양평","영등포구청","영등포시장","신길","여의도","여의나루","마포",
                  "공덕","애오개","충정로","서대문","광화문","종로3가","을지로4가","동대문역사문화공원",
                  "청구","신금호","행당","왕십리","마장","답십리","장한평","군자","아차산","광나루",
                  "천호","강동","길동","굽은다리","명일","고덕","상일동","강일","미사","하남풍산","하남시청","하남검단산"],
    '5마천':["강동","둔촌동","올림픽공원","방이",
            "오금","개롱","거여","마천"]
}

# 1호선 분기점 역 (여기서만 분기 환승 3분 적용)
branch_stations_1_line = ["구로", "병점", "금천구청"]
# 2호선 지선 분기점 (분기 환승 3분 적용)
branch_stations_2_line = ["성수", "신도림"]
# 5호선 지선 분기점 (분기 환승 3분 적용)
branch_stations_5_line = ["강동"]

# 그래프 생성
graph = defaultdict(list)
# 각 역이 어떤 (노선명, 역이름) 노드에 매핑되는지 추적
# '역이름': [('노선1', '역이름'), ('노선2', '역이름'), ...]
station_to_nodes = defaultdict(list)

for line_full_name, stations in subway_lines.items():
    for i in range(len(stations)):
        station_name = stations[i]

        # 현재 노드 정의: (노선명, 역이름)
        current_node = (line_full_name, station_name)
        station_to_nodes[station_name].append(current_node)

        # 다음 역으로 가는 엣지 추가 (2분)
        if i < len(stations) - 1:
            next_station_name = stations[i+1]
            next_node = (line_full_name, next_station_name)

            graph[current_node].append((next_node, 2))
            graph[next_node].append((current_node, 2))

# 환승 엣지 추가 (노선 간 환승, 분기 환승)
for station_name, nodes_at_station in station_to_nodes.items():
    for i in range(len(nodes_at_station)):
        for j in range(i + 1, len(nodes_at_station)):
            node1 = nodes_at_station[i] # (line_full_name1, station_name)
            node2 = nodes_at_station[j] # (line_full_name2, station_name)

            line_full_name1, _ = node1
            line_full_name2, _ = node2

            line_num1 = line_full_name1[0] # '1', '2', '3', '4', '5'
            line_num2 = line_full_name2[0]

            cost = 0

            if line_num1 == line_num2: # 같은 호선 내 환승
                # 1호선 일반 <-> 지선 환승 (분기 환승)
                if line_num1 == '1' and \
                   ((line_full_name1 == '1' and line_full_name2.startswith('1')) or \
                    (line_full_name2 == '1' and line_full_name1.startswith('1'))): # 1호선 본선과 지선 간

                    if station_name in branch_stations_1_line:
                        cost = 3 # 분기 환승: 3분
                    else: # 1호선 내 다른 타입이지만 분기역이 아닌 경우 (여긴 일반 환승으로 간주)
                        cost = 2
                # 2호선 환승
                elif line_num1 == '2' and \
                     ((line_full_name1 == '2' and line_full_name2.startswith('2')) or \
                      (line_full_name2 == '2' and line_full_name1.startswith('2'))):
                    if station_name in branch_stations_2_line:
                        cost = 3 # 분기 환승: 3분
                    else: # 2호선 내 다른 타입이지만 분기역이 아닌 경우 (여긴 일반 환승으로 간주)
                        cost = 2

                # 5호선 지선 환승
                elif line_num1 == '5' and \
                     ((line_full_name1 == '5하남검단산' and line_full_name2 == '5마천') or \
                      (line_full_name2 == '5하남검단산' and line_full_name1 == '5마천')):
                    if station_name in branch_stations_1_line:
                        cost = 3 # 분기 환승: 3분
                    else: # 5호선 내 다른 타입이지만 분기역이 아닌 경우 (여긴 일반 환승으로 간주)
                        cost = 2
                else:
                    cost = 2 # 그 외 같은 노선 내 환승 (예: 본선 내에서도 다른 지선)
            else: # 다른 호선 간 환승
                cost = 2 # 일반 노선 간 환승: 2분

            if cost > 0:
                graph[node1].append((node2, cost))
                graph[node2].append((node1, cost))