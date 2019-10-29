import db_setting       # 전체 DB
import db_search        # search DB
import db_context       # context DB
import db_percentiy     # percentiy DB
import db_keyword       # keyword DB

import cralwler_setting # 크롤링 세팅
import time             # 시간 라이브러리

while True:
    # 1. AWS-SCamera DB 연결을 한다.
    conn = db_setting.setting()

    # 2. SCamera-search DB (검색어 입력) 초기화를 한다.
    db_search.init(conn)

    # 3. Android에서 검색어가 들어올 때까지 기다린다.
    check = 0
    while(not check):
        check = db_search.find(conn, "0")
        time.sleep(0.1)
    print(check[0][0])

    # 4. SCamera-context DB (내용 DB) 초기화를 한다.
    db_context.init(conn)

    # 5. SCamera-percentiy DB (퍼센트 DB) 초기화를 한다.
    db_percentiy.init(conn)

    # 6. SCamera-KEYWORD (키워드 DB) 초기화를 한다.
    db_keyword.init(conn)

    # 7. 크롤링 초기설정 (cralwler_init) 을 해준다.
    # cralwler_setting.init(conn, check[0][0])
    cralwler_setting.init(conn, check[0][0])

    # 8. SCamera-Search DB 업데이트
    # db_search.update(conn, "LG 코드제로 A9", "1")
    db_search.update(conn, check[0][0], "1")
    conn.close()