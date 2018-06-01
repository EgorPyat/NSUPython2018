import sys
import time
from urllib.parse import urlparse

from requests import get
from bs4 import BeautifulSoup, NavigableString


def check_parentheses(tag):
    text = "".join(text for text in tag.previous_siblings
                   if isinstance(text, NavigableString))
    open_brackets = ('(', '[', '{')
    close_brackets = (')', ']', '}')
    counters = [0, 0, 0]
    for symbol in text:
        try:
            index = open_brackets.index(symbol)
            counters[index] += 1
        except ValueError:
            pass
        try:
            index = close_brackets.index(symbol)
            counters[index] -= 1
            continue
        except ValueError:
            pass
    return all(counter == 0 for counter in counters)


def is_correct_link(tag):
    if tag.name is not 'a':
        return False
    if tag.has_attr('class') and ('new' in tag['class'] or 'image' in tag['class']):
        return False
    if not tag.has_attr('href') or not tag['href'].startswith('/'):
        return False
    return True


def lazy_reader(file_object, predicate):
    data = file_object.find(predicate)
    while data is not None:
        yield data
        data = data.find_next_sibling(predicate)


BAD_PARENTS = [
    'i',
    'sup'
]
BAD_PARENTS = set(BAD_PARENTS)


BAD_PARENTS_CLASSES = [
    'infobox', 'wikidict-box', 'dablink', 'thumb', 'metadata', 'floatright', 'mw-editsection', 'navbox', 'toc', 'hatnote'
]
BAD_PARENTS_CLASSES = set(BAD_PARENTS_CLASSES)


def good_link_parents(tag):
    while tag:
        if tag.name == 'a':
            yield tag.parent
            tag = tag.find_next()
        elif tag in BAD_PARENTS \
                or tag.has_attr('class') and len(set(tag['class']) & BAD_PARENTS_CLASSES) > 0\
                or tag.has_attr('align') and 'right' in tag['align']:
            tag = tag.find_next_sibling() or tag.parent.find_next_sibling()
        else:
            tag = tag.find_next()


def get_first_link(soup):
    paragraph = soup.find('div', attrs={'class': 'mw-parser-output'})
    for parent in good_link_parents(paragraph.find()):
        for next_link in lazy_reader(parent, is_correct_link):
            if check_parentheses(next_link):
                return next_link


if __name__ == "__main__":
    visited = list()
    if len(sys.argv) != 2:
        print('URL of Wikipedia page was expected', file=sys.stderr)
        sys.exit(-1)
    start = sys.argv[1]
    # start = "https://ru.wikipedia.org/wiki/Special:Random"
    # start = "https://ru.wikipedia.org/wiki/Казахстан"
    # start = "https://ru.wikipedia.org/wiki/Сражение_при_Ресаке"
    # start = "https://ru.wikipedia.org/wiki/Головной_убор"
    # start = "https://ru.wikipedia.org/wiki/Административно-территориальное_деление_Вологодской_области#"
    # start = "https://ru.wikipedia.org/wiki/Образ"
    # start = "https://ru.wikipedia.org/wiki/ВМ-Т"
    # start = "https://ru.wikipedia.org/wiki/Форма_государственного_правления"
    # start = "https://en.wikipedia.org/wiki/Jos%C3%A9_Miguel_Agrelot_Coliseum"
    # start = "https://en.wikipedia.org/wiki/Arrondissements_of_France"
    end = [
        "https://en.wikipedia.org/wiki/Philosophy",
        "https://ru.wikipedia.org/wiki/%D0%A4%D0%B8%D0%BB%D0%BE%D1%81%D0%BE%D1%84%D0%B8%D1%8F"]
    parsed = urlparse(start)
    req = get(parsed.scheme + "://" + parsed.netloc + parsed.path)
    while True:
        soup = BeautifulSoup(req.text, 'lxml')
        link = get_first_link(soup)
        next_path = link['href']
        url = parsed.scheme + "://" + parsed.netloc + next_path
        # print(link)
        print(link['title'], url)
        if next_path in visited:
            print("CYCLE")
            break
        if url in end:
            break
        visited.append(next_path)
        req = get(url)
        time.sleep(1)
