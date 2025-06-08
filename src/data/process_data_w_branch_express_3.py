# --- 데이터 정의 (단계 3 - 확장) ---
# 1호선 급행 정차역 정의 (단계 3에 추가)
from collections import defaultdict

express_1_line_stations = [
    "연천", "동두천", "덕계", "의정부", "창동", "월계", "광운대", "석계", "회기", "청량리",
    "신설동", "동대문", "종로3가", "서울역", "노량진", "신길", "구로", "금천구청", "안양",
    "군포", "당정", "성균관대", "화서", "수원", "세류", "병점", "오산", "평택지제", "평택",
    "직산", "천안", "신창"
]

# 1호선 분기점 역 정의 (여기서만 '분기 환승' 3분 적용)
branch_stations_1_line = ["구로", "병점", "금천구청"]
# 2호선 지선 분기점 (일반 환승 2분 적용)
branch_stations_2_line = ["성수", "신도림"]
# 5호선 지선 분기점 (일반 환승 2분 적용)
branch_stations_5_line = ["강동"]

# 확장된 지하철 노선 정의 (단계 3)
# 각 노선은 이제 '노선명', '타입'(normal/express/branch), 그리고 '역 리스트'를 가짐
# (노선명_타입, 역이름) 튜플이 그래프 노드의 기본 형태가 됩니다.
subway_lines_extended_step3 = {
    '1_일반': {
        'type': 'normal',
        'stations': ["소요산","동두천","보산","동두천중앙","지행","덕정","덕계","양주","녹양","가능",
                     "의정부","회룡","망월사","도봉산","도봉","방학","창동","녹천","월계","성북",
                     "석계","신이문","외대앞","회기","청량리","제기동","신설동","동묘앞","동대문","종로5가",
                     "종로3가","종각","시청","서울역","남영","용산","노량진","대방","신길","영등포",
                     "신도림","구로", "가산디지털단지","독산","금천구청","석수","관악","안양","명학",
                     "금정","군포","당정","의왕","성균관대","화서","수원","세류","병점","세마","오산대","오산","진위","송탄","서정리","지제","평택","성환","직산","두정",
                     "천안","봉명","쌍용","아산","배방","온양온천","신창"]
    },
    '1_급행': {
        'type': 'express',
        'stations': express_1_line_stations
    },
    '1_인천': {
        'type': 'branch',
        'stations': ["구로","구일","개봉","오류동","온수","역곡","소사","부천","중동",
                     "송내","부개","부평","백운","동암","간석","주안","도화","제물포","도원","동인천","인천"]
    },
    '1_서동탄': {
        'type': 'branch',
        'stations': ["병점","서동탄"]
    },
    '1_광명': {
        'type': 'branch',
        'stations': ["금천구청","광명"]
    },
    # 1호선에만 추가된 행선지 (예시, 실제 노선과 다를 수 있음)
    # 이 부분은 명확한 '행선지'가 아닌, 실제 지선 노선으로 이미 구현된 것과 동일하게 작동합니다.
    # '소요산행', '연천행', '구로행' 등은 1_일반, 1_급행, 1_인천 등의 노선이 이미 포함하고 있으므로
    # 별도 '행선지' 노선을 추가하기보다, 사용자가 특정 역을 선택했을 때
    # 그 역이 포함된 모든 '노선_타입'을 시작/도착 노드로 고려하는 현재 방식이 더 적절합니다.
    # 예를 들어, '서울역'에서 '소요산행'을 탄다는 것은 '1_일반' 노선을 타는 것을 의미합니다.

    # 기존 2, 3, 4, 5호선
    '2': { 'type': 'normal', 'stations': ["시청","을지로입구","을지로3가","을지로4가","동대문역사문화공원","신당","상왕십리","왕십리","한양대","뚝섬","성수","건대입구","구의","강변","잠실나루","잠실","신천","종합운동장","삼성","선릉","역삼","강남","교대","서초","방배","사당","낙성대","서울대입구","봉천","신림","신대방","구로디지털단지","대림","신도림","문래","영등포구청","당산","합정","홍대입구","신촌","이대","아현","충정로","시청"] },
    '2_신설동': { 'type': 'branch', 'stations': ["성수","용답","신답","용두","신설동"] },
    '2_까치산': { 'type': 'branch', 'stations': ["신도림","도림천","양천구청","신정네거리","까치산"] },
    '3': { 'type': 'normal', 'stations': ["대화","주엽","정발산","마두","백석","대곡","화정","원당","삼송","지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"] },
    '4': { 'type': 'normal', 'stations': ["진접","오남","별내별가람","당고개","상계","노원","창동","쌍문","수유","미아","미아삼거리","길음","성신여대입구","한성대입구","혜화","동대문","동대문역사문화공원","충무로","명동","회현","서울역","숙대입구","삼각지","신용산","이촌","동작","이수","사당","남태령","선바위","경마공원","대공원","과천","정부과천청사","인덕원","평촌","범계","금정","산본","수리산","대야미","반월","상록수","한대앞","중앙","고잔","공단","안산","신길온천","정왕","오이도"] },
    '5_하남검단산': { 'type': 'normal', 'stations': ["방화","개화산","김포공항","송정","마곡","발산","우장산","화곡","까치산","신정","목동","오목교","양평","영등포구청","영등포시장","신길","여의도","여의나루","마포","공덕","애오개","충정로","서대문","광화문","종로3가","을지로4가","동대문역사문화공원","청구","신금호","행당","왕십리","마장","답십리","장한평","군자","아차산","광나루","천호","강동","길동","굽은다리","명일","고덕","상일동","강일","미사","하남풍산","하남시청","하남검단산"] },
    '5_마천': { 'type': 'branch', 'stations': ["강동","둔촌동","올림픽공원","방이","오금","개롱","거여","마천"] }
}

# 그래프 생성 (단계 3 기준)
graph_step3 = defaultdict(list)
station_to_nodes_step3 = defaultdict(list) # 역 이름 -> (노선_타입, 역이름) 매핑

for line_full_name, line_info in subway_lines_extended_step3.items():
    stations = line_info['stations']

    for i in range(len(stations)):
        station_name = stations[i]
        current_node = (line_full_name, station_name)
        station_to_nodes_step3[station_name].append(current_node)

        if i < len(stations) - 1:
            next_station_name = stations[i+1]
            next_node = (line_full_name, next_station_name)

            # 급행은 역 간 이동 시간을 2분으로 동일하게 유지
            graph_step3[current_node].append((next_node, 2))
            graph_step3[next_node].append((current_node, 2))

# 환승 엣지 추가 (단계 3 - 분기 환승 3분, 행선지 변경 1분)
for station_name, nodes_at_station in station_to_nodes_step3.items():
    for i in range(len(nodes_at_station)):
        for j in range(i + 1, len(nodes_at_station)):
            node1 = nodes_at_station[i] # (line_full_name1, station_name)
            node2 = nodes_at_station[j] # (line_full_name2, station_name)

            line_full_name1, _ = node1
            line_full_name2, _ = node2

            line_num1 = line_full_name1.split('_')[0]
            line_num2 = line_full_name2.split('_')[0]

            cost = 0

            if line_num1 == line_num2: # 같은 호선(호선 번호) 내 환승
                if line_num1 == '1':
                    is_node1_branch_line = '_인천' in line_full_name1 or '_서동탄' in line_full_name1 or '_광명' in line_full_name1
                    is_node2_branch_line = '_인천' in line_full_name2 or '_서동탄' in line_full_name2 or '_광명' in line_full_name2

                    is_node1_express = '_급행' in line_full_name1
                    is_node2_express = '_급행' in line_full_name2

                    # 1호선 일반 <-> 지선 환승 (분기 환승: 3분)
                    if (is_node1_branch_line or is_node2_branch_line) and \
                       ((line_full_name1 == '1_일반' or line_full_name2 == '1_일반')) and \
                       station_name in branch_stations_1_line:
                        cost = 3
                    # 1호선 일반 <-> 급행 환승 (행선지 변경 환승: 1분)
                    # 단, 급행이 서는 역에서만 가능
                    elif (is_node1_express != is_node2_express) and \
                         (station_name in express_1_line_stations) and \
                         (station_name not in branch_stations_1_line): # 분기역이 아닌 곳에서
                        cost = 1
                    else: # 그 외 같은 호선 내 환승 (예: 급행-지선 직접 환승 등, 이런 경우는 아마 없을 것)
                        cost = 2
                # 2호선 지선 환승 (일반 노선 간 환승과 동일하게 2분)
                elif line_num1 == '2': # 2호선 지선 환승
                    if (line_full_name1 == '2' and line_full_name2.startswith('2')) or \
                       (line_full_name2 == '2' and line_full_name1.startswith('2')):
                        if station_name in branch_stations_2_line:
                            cost = 3 # 분기 환승: 3분
                        else:
                            cost = 2 # 분기역이 아닌 2호선 내 환승
                elif line_num1 == '5': # 5호선 지선 환승
                    if (line_full_name1 == '5하남검단산' and line_full_name2 == '5마천') or \
                       (line_full_name2 == '5하남검단산' and line_full_name1 == '5마천'):
                        if station_name in branch_stations_5_line:
                            cost = 3 # 분기 환승: 3분
                        else:
                            cost = 2 # 분기역이 아닌 5호선 내 환승
                else: # 그 외 같은 노선 내 다른 타입 간 환승 (일반 2분)
                    cost = 2
            else: # 다른 호선 간 환승
                cost = 2 # 일반 노선 간 환승: 2분

            if cost > 0:
                graph_step3[node1].append((node2, cost))
                graph_step3[node2].append((node1, cost))