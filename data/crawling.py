from collections import defaultdict
from utils import init_driver, parse_html, extract_data
import time
import csv

line_idxs = defaultdict(list)

# 1호선 -> 97~108, 110~127, 199, 128~141, 172~180, 1181, 181~190, 1401~1413, 1415~1416
line_idxs[1] += list(range(97, 109))
line_idxs[1] += list(range(110, 128))
line_idxs[1] += [199]
line_idxs[1] += list(range(128, 142))
line_idxs[1] += list(range(172, 181))
line_idxs[1] += [1181]
line_idxs[1] += list(range(181, 191))
line_idxs[1] += list(range(1401, 1414))
line_idxs[1] += list(range(1415, 1417))

# 2호선 -> 201~243, 201
line_idxs[2] += list(range(201, 244))
line_idxs[2] += [201]

# 3호선-> 310~317, 370, 318~352
line_idxs[3] += list(range(310, 318))
line_idxs[3] += [370]
line_idxs[3] += list(range(318, 353))

# 4호선 -> 405~406, 408~456
line_idxs[4] += list(range(405, 407))
line_idxs[4] += list(range(408, 457))

# 5호선 ->510~548, 469~575
line_idxs[5] += list(range(510, 549))
line_idxs[5] += list(range(569,576))


driver = init_driver()
with open('results/subway_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['from_id', 'from_line', 'from_name', 'to_id', 'to_line', 'to_name', 'duration'])

    for line, idxs in line_idxs.items():
        for x, y in zip(idxs, idxs[1:]):
            url = f"https://map.naver.com/p/subway/1000/{x}/{y}/-?c=8.00,0,0,0,dh"
            if not parse_html(url, driver): continue
            duration, name1, name2 = extract_data(driver)
            writer.writerow([x, line, name1, y, line, name2, duration])
            time.sleep(0.5)

driver.quit()


