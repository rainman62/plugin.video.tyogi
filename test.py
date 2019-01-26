import re

data = ''
with open ("hello.txt", "r") as myfile:
    data=myfile.read()

inputHTML = str(data)
inputHTML = inputHTML[inputHTML.find('id=archive'):]
returnValue = {}
# returnValue.append({'link': link, 'title': title, 'image': image})

counter = 0

def getCount():
    return counter
def incrementCount():
    global counter
    counter = counter + 1
returnValueArray = []


from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a' and len(attrs)>1 and attrs[0][0]== 'href' and attrs[1][0]=='title':
            print "Encountered a start tag:", tag, " attribute :", attrs
            if returnValue.get(attrs[1][1]) is None:
                returnValue[attrs[1][1]] = getCount()
                incrementCount()
                returnValueArray.append({})
            returnValueArray[returnValue[attrs[1][1]]]['link'] = attrs[0][1]
            returnValueArray[returnValue[attrs[1][1]]]['title'] = attrs[1][1]
        elif tag == 'img' and len(attrs)>1 and attrs[0][0]== 'src' and attrs[1][0]=='alt':
            print "Encountered a start tag:", tag, " attribute :", attrs
            returnValueArray[returnValue[attrs[1][1]]]['image'] = attrs[0][1]

parser = MyHTMLParser()
parser.feed(inputHTML)

print returnValueArray
