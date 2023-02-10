import csv
from bs4 import BeautifulSoup
from selenium import webdriver
   
def get_url(search_term):
    """Generate a url from search_term"""
    template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ','+')

    """Add term query to url"""
    url = template.format(search_term)

    '''Getting the next page''' 
    """Add page query to placehoder"""
    url +='&page={}'
    return url

'''Generalize the patter'''
def extract_record(item):
    """Extract and return data from a sigle record"""
    atag = item.h2.a
    name = atag.text
    print(name)
    url = "https://www.amazon.in/"+atag.get('href')
    print(url)
    try:
        price_parent = item.find('span','a-price')
        price = price_parent.find('span','a-offscreen').text
        print(price)
    except AttributeError:
        return
    try:        
        rating = item.i.text
        print(rating)
    except AttributeError:
        rating = ""
       
    try:
        review = item.find('span',{'class':'a-size-base s-underline-text'})
        review_count = review.text
        print(review_count)
    except:
        review_count = ""
    image = item.find('img',{'class':'s-image'}).get('src')
    print(image)

    result = (name,url, price,rating,review_count,image)
    return result   

def main(search_term):
    """Run main program routine"""
    #Startup the webdriver
    driver = webdriver.Chrome("F:\Web Scraping\Golabal\chromedriver.exe")
    records = []
    url = get_url(search_term)
    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source,'html.parser')
        results = soup.find_all('div', {'data-component-type':'s-search-result'})
        print(len(results))

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()  
    # Save data in CSV file
    with open('results1.csv','w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name','url', 'price','rating','review_count','image'])
        writer.writerows(records)


main('HP Laptop')