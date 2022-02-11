import requests
import lxml.html as html
import os
import datetime


#Constant links
HOME_URL='https://www.jornada.com.mx'
XPATH_LINK_TO_ARTICLE= '//h2[@class="title-default"]/a/@href'
XPATH_TITLE = '//h2[@class="title title-default"]/text()'
XPATH_SUMMARY = '//*[@id="content_nitf"]/p[1]/text()'
XPATH_CONTENT='//*[@id="content_nitf"]/p[not(@class)]/text()'


def parse_notice(link,today):
    try:
        response=requests.get(link)
        if response.status_code==200:
            notice=response.content.decode('utf-8')
            parsed=html.fromstring(notice)

            try:
                title= parsed.xpath(XPATH_TITLE)[0]
                title=title.replace('\"','')
                summary= parsed.xpath(XPATH_SUMMARY)[0]
                content= parsed.xpath(XPATH_CONTENT)[1:]
            except IndexError:
                return
                
            if content[0]!="":    
                with open(f'{today}/{title}.txt','w',encoding='utf-8') as f:
                    f.write(title)
                    f.write('\n\n')
                    f.write(summary)
                    f.write('\n\n')
                    for p in content:
                        f.write(p)
                        f.write('\n')
                    f.write('fuente: ')
                    f.write(link)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    #try-except in case of error
    try:
        #get the home page
        response= requests.get(HOME_URL)
        #if request is ok
        if response.status_code==200:
            #decode utf-8 response and parse it
            home=response.content.decode('utf-8')
            parsed=html.fromstring(home)
            links_to_notices=parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)
            today= datetime.date.today().strftime('%d %m %Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_notices:
                concat_link=HOME_URL+link
                parse_notice(concat_link,today)

        else:
            #if request is not ok
            raise ValueError(f'Error: {response.status_code}')

    #If there's an error, print it
    except ValueError as ve:
        print(ve)

def run():
    parse_home()
    pass

if __name__ == '__main__':
    run()



