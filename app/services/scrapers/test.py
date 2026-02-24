import requests
from bs4 import BeautifulSoup

url = "https://weworkremotely.com/categories/remote-back-end-programming-jobs"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("[*] CSS Selector (select/select_one) yöntemi ile test ediliyor...\n")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# DÜZELTME 1: find_all yerine select. Class olduğu için başına nokta (.) koyduk.
jobs = soup.select('li.new-listing-container')

for job in jobs[:2]: 
    # DÜZELTME 2: find yerine select_one. Class'ların başına nokta (.) koyduk.
    title_elem = job.select_one('h3.new-listing__header__title')
    company_elem = job.select_one('p.new-listing__company-name')
    
    # DÜZELTME 3: İşte CSS Selector'ün asıl gücü! Uzun lambda yerine,
    # "href özelliğinde /remote-jobs/ içeren 'a' etiketini bul" komutu (*= içerir demektir)
    link_elem = job.select_one('a[href*="/remote-jobs/"]')

    title = title_elem.text.strip() if title_elem else "Bulunamadı"
    company = company_elem.text.strip() if company_elem else "Bulunamadı"
    link = f"https://weworkremotely.com{link_elem['href']}" if link_elem else "Bulunamadı"

    print(f"🎯 İlan Başlığı : {title}")
    print(f"🏢 Şirket      : {company}")
    print(f"🔗 Link        : {link}")
    
    if link != "Bulunamadı":
        detail_resp = requests.get(link, headers=headers)
        detail_soup = BeautifulSoup(detail_resp.content, 'html.parser')
        
        # DÜZELTME 4: Detay sayfası class'ı için nokta (.)
        desc_div = detail_soup.select_one('div.lis-container__job__content__description')
        if not desc_div: 
            # DÜZELTME 5: Eğer o class yoksa, ID ile ara. ID'ler için diyez (#) kullanılır.
            desc_div = detail_soup.select_one('div#job-listing-show-container')

        desc_text = desc_div.text.strip()[:100] + "..." if desc_div else "Açıklama Div'i Hatalı!"
        print(f"📄 Açıklama Özet: {desc_text}")
        
    print("-" * 50)
    