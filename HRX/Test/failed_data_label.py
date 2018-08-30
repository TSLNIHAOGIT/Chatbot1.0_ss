import re
file=open('UnittestTextReport.txt')
for each in file:
    if each.startswith('FAIL:'):
        # print('each',each)
        pattern=re.search('index=(\d{0,})',each)
        print('index',pattern.group(1))

    if each.startswith('AssertionError:'):
        # print('each',each)
        pattern=re.search(r'(\d.*\d)',each)
        print('label',pattern.group(1))