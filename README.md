# 자료구조와 알고리즘 팀프로젝트 : 서울 지하철 1~5호선 최단 경로 탐색 알고리즘

## 팀 구성
- 팀장: 김은주
- 팀원: 김수현, 장승호

## 기간
2025-05-08 ~ 2025-06-08

## 역할 분담
- 김은주: TNR (with dijkstra, dial's), 데이터에 가중치 도입, 벤치마킹 진행
- 장승호: UCS, Dijkstra, 데이터에 급행, 분기 시스템 도입
- 김수현: A* 및 BFS, 1. 역 이름 일치 기반, 2. 환승 예측 기반, 3. 노선 내 거리 기반, 4. 혼합의 총 네 가지 휴리스틱 함수 고안

## 활동 내용 및 일정
- 5/8~5/16: 각자 개별 알고리즘 구현
- 5/16(금)(23:00~24:00): 비대면 zoom 회의를 통해 역할 분담 및 개선 방향 탐색
- 5/22(목)(12:00~2:00): 오프라인 스터디룸에서 각자 구현한 알고리즘 발표
- 6/3(화): 각자 ppt제작을 완료하여 비대면 zoom 회의를 통한 설명
- 6/3~: 피피티 최종 종합 및 정리 및 최종발표 준비

## 프로젝트 구조
## 1. `data`

- ### `img/`
  - 알고리즘 성능, 엣지 가중치 분포 등 다양한 시각화 이미지 파일 저장
    - `algorithm_benchmark.png` : 알고리즘별 성능 비교 그래프
    - `edge weight frequency distribution.png` : 엣지 가중치 빈도 분포 시각화
    - `TG edge weight distribution.png` : 환승 그래프 엣지 가중치 분포

- ### `raw/`
  - 원본 및 테스트용 CSV 데이터 저장
    - `subway_data.csv` : 서울 지하철 네트워크 원본 데이터
    - `test_nodes.csv` : 테스트용 노드 데이터

---

## 2. `docs`

- 프로젝트 관련 문서 파일 저장
  - `best subway route in seoul.pptx` : 발표 자료(PPT)
  - `발표문.txt` : 발표 스크립트
  - `진행 보고서.docx` : 진행 보고서 

---

## 3. `notebooks`

- 실험, 분석, 검증용 Jupyter 노트북 파일 저장
  - `A_Star_Algorithm_retry.ipynb` : A* 알고리즘 실험
  - `dijkstra_ucs_phase_1~4.ipynb` : Dijkstra/UCS 단계별 실험
  - `graph_HashTable_분기(분기,환승배제x)(4).ipynb` : 해시테이블 기반 실험

---

## 4. `src`

- 프로젝트의 주요 소스 코드가 저장된 디렉토리

- ### `algorithms/`
  - 경로 탐색/최적화 알고리즘 구현
    - `a_star.py` : A* 알고리즘
    - `dijkstra_1.py` : Dijkstra 알고리즘(1단계 데이터 기반)
    - `ucs_and_dijkstra_2.py`, `ucs_and_dijkstra_3.py` : UCS, Dijkstra 변형(2,3단계 데이터 기반)
    - `transit_node_routing.py` : Transit Node Routing(TNR) 구현

- ### `benchmarking/`
  - 알고리즘 성능 측정 및 시각화 코드
    - `benchmarking.py` : 벤치마킹 자동화/측정
    - `visualize_benchmarking.py` : 결과 시각화

- ### `data/`
  - 데이터 전처리 및 크롤링, 유틸리티 코드
    - `crawling.py` : 데이터 크롤러
    - `data_structure.py` : 데이터 구조 관리
    - `process_data_w_branch_express_1/2/3.py` : 분기/급행 처리 데이터 가공
    - `process_data_w_weight.py` : 가중치 반영 전처리
    - `utils.py` : 유틸 함수
