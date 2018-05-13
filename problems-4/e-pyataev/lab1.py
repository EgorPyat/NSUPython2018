import time
import urllib
import bs4
import requests

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

def find_link(search_history):
    response = requests.get(search_history[-1])
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    founded_link = None
    find = False
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")
    for element in content_div.find_all("p", recursive=False):
        element = remove_parentheses(str(element))
        element = bs4.BeautifulSoup(element, "html.parser").find('p', recursive=False)
        for link in element.find_all("a", recursive=False):
            founded_link = urllib.parse.urljoin('https://en.wikipedia.org/', link.get('href'))
            if founded_link in search_history: continue
            find = True
            break
        if find:
            break
    if not founded_link:
        return

    return founded_link

def crawl(search_history, target_url):
    if search_history[-1] == target_url:
        print("Reached the destination!")
        return False
    else:
        return True

if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/Special:Random"
    target_url = "https://en.wikipedia.org/wiki/Philosophy"
    links_chain = [start_url]

    try:
        while crawl(links_chain, target_url):
            print(links_chain[-1])

            link = find_link(links_chain)
            if not link:
                print("No link was found!")
                break

            links_chain.append(link)
            time.sleep(2)
    except KeyboardInterrupt:
        pass
