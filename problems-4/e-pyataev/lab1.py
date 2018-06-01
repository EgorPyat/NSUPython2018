import time
import urllib
import bs4
import requests
import re
import sys

def remove_parentheses(text):
    sharp_brackets = 0
    parentheses = 0
    st = -1
    fi = -1
    count = 0
    remove = []
    for ch in text:
        if ch == '<':
            sharp_brackets += 1
        if ch == '>':
            sharp_brackets -= 1
        if ch == '(':
            parentheses += 1
            if(sharp_brackets == 0 and st == -1):
                st = count
        if ch == ')':
            parentheses -= 1
            if(st != 0 and parentheses == 0):
                fi = count
                remove.append(text[st:fi+1])
                st = -1
                fi = -1
        count += 1
    for el in remove:
        text = text.replace(el,'')

    return text

def find_link(search_history, lang):
    response = requests.get(search_history[-1])
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    founded_link = None
    find = False
    for content_div in soup.find_all('div', attrs={'class':'mw-parser-output'}):
        for element in content_div.find_all("p", recursive=False):
            element = remove_parentheses(str(element))
            element = bs4.BeautifulSoup(element, "html.parser").find('p')
            for link in element.find_all("a", recursive=False):
                classes = link.get('class') if link.get('class') is not None else []
                if link.get('href') is None or 'new' in classes:
                    continue
                founded_link = 'https://' + lang + '.wikipedia.org' + link.get('href')
                find = True
                break
            if find:
                break
        if not founded_link:
            return

    return founded_link

def crawl(search_history, target_url):
    if search_history[-1] in target_url:
        print("Reached the destination!")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("cycle!")
        return False
    else:
        return True

if __name__ == "__main__":
    if(len(sys.argv) == 2):
        try:
            target_url = ("https://en.wikipedia.org/wiki/Philosophy", "https://ru.wikipedia.org/wiki/%D0%A4%D0%B8%D0%BB%D0%BE%D1%81%D0%BE%D1%84%D0%B8%D1%8F")
            start_url = sys.argv[1]
            lang = re.search('://(\w+).', start_url).group(1)
            links_chain = [start_url]

            while crawl(links_chain, target_url):
                print(urllib.parse.unquote(links_chain[-1]))
                link = find_link(links_chain, lang)
                if not link:
                    print("No link was found!")
                    break

                links_chain.append(link)
                time.sleep(2)
        except Exception as e:
            print(e)
