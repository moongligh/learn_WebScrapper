from indeed import extract_indeed_pages, extract_indeed_jobs

last_indeed_pages = extract_indeed_pages() # 최종 페이지 추출
indeed_jobs = extract_indeed_jobs(last_indeed_pages)  # 최종 페이지를 이용한 request문 작성

print(indeed_jobs) # indeed에 올라온 구직내용 출력