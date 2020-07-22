import requests as req
from bs4 import BeautifulSoup as bs

LIMIT = 20 # 페이지당 출력되는 게시물 수
URL = f'https://kr.indeed.com/jobs?q=Django&limit={LIMIT}' # 페이지 추출을 위한 기본 URL

def get_last_page():    # 페이지 추출 함수
    result = req.get(URL)
    soup = bs(result.text, 'html.parser')
    pagination = soup.find('div', {'class': 'pagination'})
    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]: # 마지막 a링크는 '다음'으로 페이지가 아니므로 삭제
        pages.append(int(link.find('span').string)) # link에 String요소가 하나라면 link.string으로 수정가능
    
    last_page = pages[-1] # 마지막 페이지 추출
    return last_page

def extract_job(html): # 채용정보를 추출하여 doc 형태로 리턴
    title = html.find('h2', {'class': 'title'}).find('a')['title']
    company = html.find('span', {'class': 'company'})
    company_anchor = company.find('a')
    if company_anchor is not None:  # 회사명에 링크가 있는경우 앵커에서 추출, 아닌경우 그대로 추출
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip() # 빈칸제거
    location = html.find('div', {'class': 'recJobLoc'})['data-rc-loc']
    job_id = html['data-jk']

    return {'title': title,
        'company': company,
        'location': location,
        'link': f'https://kr.indeed.com/viewjob?jk={job_id}'
    }

def extract_jobs(last_page): # 추출한 최종페이지를 이용하여 모든 채용 정보를 수집
    jobs = []

    for page in range(last_page):  # 추출한 마지막 페이지를 이용한 범위지정 for loop
        print(f'indeed Scarpping page {page+1}')
        result = req.get(f'{URL}&start={page*LIMIT}')
        soup = bs(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs

def get_jobs():
    last_page = get_last_page() # 최종 페이지 추출
    jobs = extract_jobs(last_page)  # 최종 페이지를 이용한 페이지당 데이터 추출 

    return jobs
