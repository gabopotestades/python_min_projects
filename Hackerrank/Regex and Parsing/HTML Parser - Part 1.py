from html.parser import HTMLParser

#Override HTML Parser function to print tags and their attributes
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('Start :', tag)
        for attr in attrs:
            print('->', attr[0], '>', attr[1])

    def handle_endtag(self, tag):
        print('End   :', tag)

    def handle_startendtag(self, tag, attrs):
        print('Empty :', tag)
        for attr in attrs:
            print('->', attr[0], '>', attr[1])

    def handle_comment(self, data):
        pass

parser = MyHTMLParser()

#For n in inputs, parse the string
for _ in range(int(input())):
    parser.feed(input())
