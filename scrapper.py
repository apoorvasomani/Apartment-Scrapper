import sys
import urllib2
import xlsxwriter

from bs4 import BeautifulSoup


def get_page(url):
    """
    Get the page using the url

    """
    page = ''

    try:
        page = urllib2.urlopen(url)
        return page
    except urllib2.URLError as e:
        print 'Exception occurred -', e.read()

    return page

def search_elements(page, element, **query_attrs):
    """
    Search for the given element which satisfy the query attributes

    """
    soup = BeautifulSoup(page, 'html.parser')

    # Search the element
    elements = soup.find_all(element, attrs=query_attrs)

    return elements

def find_element(parent_element, element, strip_text=True, **query_attrs):
    """
    Search for an element inside an already parsed element

    """
    element = parent_element.find(element, attrs=query_attrs)

    if not element:
        return None

    element = element.text.encode('utf-8')

    if strip_text:
        element = element.strip()

    return element

def get_apartments_and_write_to_excel(page):

    workbook = xlsxwriter.Workbook('mumbai_apartments.xlsx')
    worksheet = workbook.add_worksheet()

    # Set width of columns
    worksheet.set_column('B:B', 100)
    worksheet.set_column('C:C', 10)

    # Define formatting styles
    bold = workbook.add_format({'bold': True})

    # Add titles for column
    worksheet.write(1, 1, 'Apartment Description', bold)
    worksheet.write(1, 2, 'Price', bold)

    row = 2

    apartments = search_elements(page, 'p', **{'class': 'result-info'})
    for apartment in apartments:
        title = find_element(apartment, 'a', **{'class': 'result-title'})
        price = find_element(apartment, 'span', **{'class': 'result-price'})

        if title:
            worksheet.write(row, 1, title.title().decode('utf-8'))

        if price:
            worksheet.write(row, 2, price.decode('utf-8'))

        row += 1

    workbook.close()

if __name__ == '__main__':

    url = sys.argv[1]

    page = get_page(url)
    _ = get_apartments_and_write_to_excel(page)

