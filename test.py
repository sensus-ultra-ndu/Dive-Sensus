import re

string = '0x158f39a3'
r'\d\w\d{7}\w'
regex = re.compile(r'\d\w[a-zA-Z0-9]{8}')
if regex.match(string) is None:
	print('cannot')
else:
    print('ok')
    uigyviycviy