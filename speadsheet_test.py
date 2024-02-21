import pygsheets
import pandas as pd

def setup():
    gc = pygsheets.authorize(service_file='kpu2024-dca0549f3753.json')
    id_test = '129h_iw2er5z5CXF3sN-XVQ1of3bZDv2uqwcCcRSuwaY'

    sh = gc.open_by_key(id_test)
    return sh

def update_spreadsheet():
    try:
        sh = setup()
        wks = sh[1]
        # set the values at cell A12
        formula = '=HYPERLINK("https://www.google.com","Google")'
        wks.update_value('A11', formula)
    except Exception as e:
        print('error update_spreadsheet: ' + str(e))


def main():
    update_spreadsheet()

if __name__ == '__main__':
    main()
