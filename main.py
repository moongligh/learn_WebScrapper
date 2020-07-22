from indeed import get_jobs as get_indeed_jobs
from so import get_jobs as get_so_jobs
from save import save_to_csv

indeed_jobs = get_indeed_jobs()
so_jobs = get_so_jobs()

jobs = so_jobs + indeed_jobs # 두 사이트의 구직정보를 병합
save_to_csv(jobs) # 병합한 데이터를 csv파일로 저장하기

# print(indeed_jobs) # indeed에 올라온 구직내용 출력
# print(so_jobs) # StackOver Flow에 올라온 구직내용 출력