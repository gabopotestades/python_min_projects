from html.parser import HTMLParser

#Override function for comment and data
class MyHTMLParser(HTMLParser):
    
    def handle_data(self, data):
        if data == '\n': return
        print('>>> Data', data, sep = '\n')
    
    def handle_comment(self, data):
        if len(data.split('\n')) > 1:
            print('>>> Multi-line Comment')
        else:
            print('>>> Single-line Comment')

        if data.strip():
            print(data)

#Format string input issues in given data
html_string = ''
for i in range(int(input())):
    html_string += input().rstrip()+'\n'

#Parse data
parser = MyHTMLParser()
parser.feed(html_string)
