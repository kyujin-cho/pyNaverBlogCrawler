# -*- coding: utf-8 -*-

import requests
import urllib.parse
import simplejson as json
import re
import os
import zipfile
import urllib.request
import os.path
import mimetypes
import time
import urllib.parse
import cgi
import time
from readability.readability import Document
from bs4 import BeautifulSoup, Tag
from multiprocessing import Process, Pipe, Queue


class MyZipFile(zipfile.ZipFile):
    def writestr(self, name, s, compress=zipfile.ZIP_DEFLATED):
        zipinfo = zipfile.ZipInfo(name, time.localtime(time.time())[:6])
        zipinfo.compress_type = compress
        zipfile.ZipFile.writestr(self, zipinfo, s)


def dlimg(path, str):
    str.put(urllib.request.urlopen(path).read())
    return


def getimg(path1, path2):
    if __name__ == '__main__':
        qstr1 = Queue()
        qstr2 = Queue()
        p1 = Process(target=dlimg, args=(path1, qstr1))
        p2 = Process(target=dlimg, args=(path2, qstr2))

        p1.start()
        p2.start()

        p1.join()
        p2.join()

        img1 = qstr1.get()
        img2 = qstr2.get()
        return [img1, img2]


def getURL(post, bID):
    postNo = list()
    count = 30
    page = int(int(post) / 30) + 1
    for i in range(1, page + 1):
        print("Try")
        print(i)
        params = urllib.parse.urlencode({'blogId': bID, 'currentPage': i, 'countPerPage': 30})
        URL = "http://blog.naver.com/PostTitleListAsync.nhn?%s" % params
        rawJson = requests.get(URL).text
        rawJson = re.sub(r"\"pagingHtml\":.*\",", "", rawJson)
        parsedJson = json.loads(rawJson)
        if i == page:
            count = post % 30
        for j in range(count):
            print(j)
            print(parsedJson["postList"][j]["logNo"])
            postNo.append(parsedJson["postList"][j]["logNo"])
    postNo.reverse()
    print(len(postNo))
    return postNo


def buildEpub(bookTitle, bookAuthor, bookPublisher, blogURL, count, postNo):
    # parser = build_command_line()
    # (options, args) = parser.parse_args()
    cover = None
    # nos = len(args)
    requestnum = 0
    cpath = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='
    ctype = 'image/gif'
    # if cover is not None:
    #    cpath = 'images/cover' + os.path.splitext(os.path.abspath(cover))[1]
    #    ctype = mimetypes.guess_type(os.path.basename(os.path.abspath(cover)))[0]

    epub = MyZipFile('{:s} - {:s}.epub'.format(bookAuthor, bookTitle), 'w', zipfile.ZIP_DEFLATED)
    # Metadata about the book
    info = dict(title=bookTitle,
                author=bookAuthor,
                rights='Copyright respective page authors',
                publisher=bookPublisher,
                ISBN='978-1449921880',
                subject='Blogs',
                description='Articles extracted from blogs for archive purposes',
                date=time.strftime('%Y-%m-%d'),
                front_cover=cpath,
                front_cover_type=ctype
                )

    # The first file must be named "mimetype"
    epub.writestr("mimetype", "application/epub+zip", zipfile.ZIP_STORED)
    # We need an index file, that lists all other HTML files
    # This index file itself is referenced in the META_INF/container.xml file
    epub.writestr("META-INF/container.xml", '''<container version="1.0"
		xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
		<rootfiles>
			<rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
		</rootfiles>
		</container>''')

    # The index file is another XML file, living per convention
    # in OEBPS/content.opf
    index_tpl = '''<package version="2.0"
		xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid">
		<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
		<dc:title>%(title)s</dc:title>
		<dc:creator>%(author)s</dc:creator>
		<dc:language>en</dc:language>
		<dc:rights>%(rights)s</dc:rights>
		<dc:publisher>%(publisher)s</dc:publisher>
		<dc:subject>%(subject)s</dc:subject>
		<dc:description>%(description)s</dc:description>
		<dc:date>%(date)s</dc:date>
		<dc:identifier id="bookid">%(ISBN)s</dc:identifier>
		<meta name="cover" content="cover-image" />
		</metadata>
		<manifest>
		  <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
		  <item id="cover" href="cover.html" media-type="application/xhtml+xml"/>
		  <item id="cover-image" href="%(front_cover)s" media-type="%(front_cover_type)s"/>
		  <item id="css" href="stylesheet.css" media-type="text/css"/>
			%(manifest)s
		</manifest>
		<spine toc="ncx">
			<itemref idref="cover" linear="no"/>
			%(spine)s
		</spine>
		<guide>
			<reference href="cover.html" type="cover" title="Cover"/>
		</guide>
		</package>'''

    toc_tpl = '''<?xml version='1.0' encoding='utf-8'?>
		<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
				 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
		<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
		<head>
		<meta name="dtb:uid" content="%(ISBN)s"/>
		<meta name="dtb:depth" content="1"/>
		<meta name="dtb:totalPageCount" content="0"/>
		<meta name="dtb:maxPageNumber" content="0"/>
	  </head>
	  <docTitle>
		<text>%(title)s</text>
	  </docTitle>
	  <navMap>
		<navPoint id="navpoint-1" playOrder="1"> <navLabel> <text>Cover</text> </navLabel> <content src="cover.html"/> </navPoint>
		%(toc)s
	  </navMap>
	</ncx>'''

    cover_tpl = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<title>Cover</title>
		<style type="text/css"> img { max-width: 100%%; } </style>
		</head>
		<body>
		<h1>%(title)s</h1>
		<div id="cover-image">
		<img src="%(front_cover)s" alt="Cover image"/>
		</div>
		</body>
		</html>'''

    stylesheet_tpl = '''
		p, body {
			font-weight: normal;
			font-style: normal;
			font-variant: normal;
			font-size: 1em;
			line-height: 2.0;
			text-align: left;
			margin: 0 0 1em 0;
			orphans: 2;
			widows: 2;
		}
		h1{
			color: blue;
		}
		h2 {
			margin: 5px;
		}
	'''

    manifest = ""
    spine = ""
    toc = ""

    epub.writestr('OEBPS/cover.html', cover_tpl % info)
    # if cover is not None:
    #    epub.write(os.path.abspath(cover),'OEBPS/images/cover'+os.path.splitext(cover)[1],zipfile.ZIP_DEFLATED)

    for i in range(count):
        url = blogURL
        url += '/'
        url += str(postNo[i])
        print("Reading url no. {:s} of {:s} --> {:s} ".format(str(i + 1), str(count), url))
        html = urllib.request.urlopen(url).read()
        readable_article = Document(html).summary().encode('utf-8')
        readable_title = Document(html).short_title()

        manifest += '<item id="article_{}" href="article_{}.html" media-type="application/xhtml+xml"/>\n'.format(i + 1,
                                                                                                                 i + 1)
        spine += '<itemref idref="article_{}" />\n'.format(i + 1)
        toc += '<navPoint id="navpoint-{}" playOrder="{}"> <navLabel> <text>{}</text> </navLabel> <content src="article_{}.html"/> </navPoint>'.format(
                i + 2, i + 2, cgi.escape(readable_title), i + 1)

        soup = BeautifulSoup(readable_article)
        # Add xml namespace
        soup.html["xmlns"] = "http://www.w3.org/1999/xhtml"
        # Insert header
        body = soup.html.body
        h1 = soup.new_tag("h1", **{'class': "title"})
        h1.insert(0, cgi.escape(readable_title))
        body.insert(0, h1)
        # Add stylesheet path
        head = soup.find('head')
        if head is None:
            head = soup.new_tag("head")
            soup.html.insert(0, head)
        link = soup.new_tag('link', type="text/css", rel='stylesheet', href='stylesheet.css')
        head.insert(0, link)
        article_title = soup.new_tag("title")
        article_title.insert(0, cgi.escape(readable_title))
        head.insert(1, article_title)

        # Download images
        for j, image in enumerate(soup.findAll('img')):
            try:
                # Convert relative urls to absolute urls
                imgabspath = [urllib.parse.urljoin(url, image["src"]),
                              urllib.parse.urljoin(url, image["src"])]
                # Remove query strings from url
                imgpath = [urllib.parse.urlunsplit(urllib.parse.urlsplit(imgabspath[0])[:3] + ('', '',)),
                           urllib.parse.urlunsplit(urllib.parse.urlsplit(imgabspath[1])[:3] + ('', '',))]
                print("Downloading image: {:s} {:s}".format(str(j + 1), imgpath[0]))
                print("Downloading image: {:s} {:s}".format(str(j + 2), imgpath[1]))
                imgfile = [os.path.basename(imgpath[0]),
                           os.path.basename(imgpath[1])]
                filename = [
                    'article_{:s}_image_{:s}{:s}'.format(str(i + 1), str(j + 1), os.path.splitext(imgfile[0])[1]),
                    'article_{:s}_image_{:s}{:s}'.format(str(i + 1), str(j + 2), os.path.splitext(imgfile[1])[1])]
                if imgpath[0].lower().startswith("http") and imgpath[1].lower().startswith("http"):
                    img = getimg(imgabspath[0], imgabspath[1])
                    epub.writestr('OEBPS/images/' + filename[0], img[0])
                    epub.writestr('OEBPS/images/' + filename[1], img[1])

                    image['src'] = 'images/' + filename[0]
                    manifest += '<item id="article_{:s}_image_{:s}" href="images/{:s}" media-type="{:s}"/>\n'.format(
                            str(i + 1), str(j + 1), filename[0], str(mimetypes.guess_type(filename[0])[0]))
                    manifest += '<item id="article_{:s}_image_{:s}" href="images/{:s}" media-type="{:s}"/>\n'.format(
                            str(i + 1), str(j + 2), filename[1], str(mimetypes.guess_type(filename[1])[0]))
                j += 1
            except urllib.error.HTTPError as e:
                print(e)
        epub.writestr('OEBPS/article_{:s}.html'.format(str(i + 1)), str(soup))
    info['manifest'] = manifest
    info['spine'] = spine
    info['toc'] = toc

    # Finally, write the index and toc
    epub.writestr('OEBPS/stylesheet.css', stylesheet_tpl)
    epub.writestr('OEBPS/Content.opf', index_tpl % info)
    epub.writestr('OEBPS/toc.ncx', toc_tpl % info)


postCount = input("Total post count : ")
blogID = str(input("Blog ID : "))
title = str(input("Book Title (default: Blog ID) : "))
postAuthor = str(input("Author of those articles(default: Blog ID) : "))
postPublisher = str(input("Your name : "))
if postCount == '' and blogID == '':
    postCount = 381
    blogID = 'santa_croce'
if title == '':
    title = blogID
if postAuthor == '':
    postAuthor = blogID
if postPublisher == '':
    exit()
postCount = int(postCount)
postNo = getURL(postCount, blogID)

'''
if not os.path.exists(ID) :
	os.makedirs(ID)
'''

URL = 'http://m.blog.naver.com/{:s}'.format(blogID)
buildEpub(title, postAuthor, postPublisher, URL, postCount, postNo)
