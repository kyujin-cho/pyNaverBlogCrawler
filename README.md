# pyNaverBlogCrawler
https://github.com/rupeshk/web2epub 라이브러리를 참조한 파이썬 기반의 네이버 블로그 글 크롤러입니다.

블로그의 모든 글 및 이미지를 ePUB 형태로 저장해줍니다.

사용방법 
파이썬 2 :
  pip install readability-lxml beautifulsoup4 simplejson requests 설치 
  python getArticle2.py 실행
파이썬 3 :
  pip install readability-lxml beautifulsopu4 simplejson requests 설치
  python getArticle.py 실행

Troubleshooting 
  Q: lxml 설치 시 오류가 발생합니다.
  A: 
    Windows:
      http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml 에서 최신 버전의 *win32* whl 파일 다운로드 
      예:(lxml-3.5.0-cp35-none-win32.whl)
      다운로드 받은 파일을 pip install pip install 명령어로 설치
      예:(pip intall lxml-3.5.0-cp35-none-win32.whl)
    
    OS X:
      xcode-select --install 로 Xcode Command Line Tools 설치하여 libxml2 설치 후 다시 시도
  
