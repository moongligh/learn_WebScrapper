import requests as req
from bs4 import BeautifulSoup as bs

LIMIT = 20 # 페이지당 출력되는 게시물 수
URL = f'https://stackoverflow.com/jobs?q=Django' # 페이지 추출을 위한 기본 URL

def get_last_page():    # 페이지 추출 함수
    result = req.get(URL)
    soup = bs(result.text, 'html.parser')
    pages = soup.find('div', {'class': 's-pagination'}).find_all('a')
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

def extract_job(html):  # 채용정보를 추출하여 doc 형태로 리턴
    title = html.find('a', {'class': 's-link'})['title']
    company, location = html.find('h3').find_all('span', recursive=False) # unpack value를 이용하기 위해 첫단계 'span'만 수집
    company.get_text(strip=True)
    location.get_text(strip=True).strip('-').strip(' \r').strip('\n')

    # company_location = html.find('h3').get_text(strip=True) # h3태그 안의 모든 text를 가져온다.
    # company = company_location.split('•')[0]    # 가져온 text의 값 중 • 을 기준으로 앞은 회사 뒤는 지역을 할당한다.
    # location = company_location.split('•')[1]

    job_id = html['data-jobid']

    return {'tite': title,
        'company': company,
        'location': location,
        'link': f'https://stackoverflow.com/jobs/{job_id}'
    }

def extract_jobs(last_page):    # 추출한 최종페이지를 이용하여 모든 채용 정보를 수집
    jobs=[]
    for page in range(last_page):   # 추출한 마지막 페이지를 이용한 범위지정 for loop
        print(f'StackOverFlow Scarpping page {page+1}')
        result = req.get(f'{URL}&pg={page+1}')
        soup = bs(result.text, 'html.parser')
        results = soup.find_all('div', {'class': '-job'})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs():
    last_page = get_last_page() # 최종 페이지 추출
    jobs = extract_jobs(last_page)  # 최종 페이지를 이용한 페이지당 데이터 추출 
    return jobs