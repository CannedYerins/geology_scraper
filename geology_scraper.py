from bs4 import BeautifulSoup
import requests
import sys
import re
import os


def is_next_anchor(e):
    if e.name != 'a':
        return False
    img_child = e.find('img')
    return img_child is not None and img_child['src'] == '../gifs/next.gif'


def process_text(s):
    s = re.sub('(&nbsp)+', '', s)
    s = re.sub('\n{2,}', '\n', s)
    s = re.sub(r'[^\x00-\x7F]+', '', s)
    return s


def main():
    initial_url = sys.argv[1]
    current_page = initial_url[initial_url.rfind('/') + 1:]
    base_url = initial_url[:initial_url.rfind('/') + 1]
    lecture_name = base_url.split('/')[-2]
    print base_url
    print lecture_name
    page_texts = []

    while True:
        print current_page
        html = requests.get(base_url + current_page,
                            auth=(sys.argv[2], sys.argv[3])).text
        soup = BeautifulSoup(html, 'lxml')
        page_texts.append(process_text(soup.get_text()))
        anchor = soup.find(is_next_anchor)
        next_page = anchor['href']
        # stop condition: the "next button" points to the page we're already
        # on, i.e. the last one
        if next_page == current_page:
            break
        else:
            current_page = next_page

    if not os.path.isdir('lectures'):
        os.mkdir('lectures')
    filename = 'lectures/' + lecture_name + '.txt'
    f = open(filename, 'w')
    f.write(''.join(page_texts))
    print 'Successfully processed lecture and created file at ' + filename


if __name__ == '__main__':
    main()
