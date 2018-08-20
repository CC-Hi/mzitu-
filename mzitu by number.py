import urllib.request
import re
import time
import urllib.parse
import os
import gzip
import threading

def open_url(url,headers=None):
    if headers==None:
        headers={'User-Agent':'Mozilla/5.0 (Windows\
NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Geck\
o) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5221.\
400 QQBrowser/10.0.1125.400',  'Accept-Encoding':' gzip, deflate','Referer':'http://www.mzitu.com/'}
    req=urllib.request.Request(url,headers=headers)
    page = urllib.request.urlopen(req)
    if page.info().get('Content-Encoding')=='gzip':
        f = gzip.GzipFile(fileobj=page)
        html = f.read().decode('utf-8')
    #elif page.info().get('Content-Encoding')=='None':
    else:
        html = page.read().decode('utf-8')
    return html

def get_url(url):
    html = open_url(url)
    urllist = re.findall('<li><a href="([^"]+)"',html)
    return urllist

def dl_img(each,headers):
    print(each+'\n')
    filename = each.split('/')[-1]
    req=urllib.request.Request(each,headers=headers)
    try_c=0
    while try_c<3:
        try:
            page = urllib.request.urlopen(req,timeout=5)
            html = page.read()#.decode('utf-8')
            with open(filename,'wb') as f:
                f.write(html)
                f.close()
            try_c=3
        except:
            try_c=try_c+1
            print('重试\n')
def get_img(html,headers):
    p = r'<img src="([^"]+.jpg)"'
    imglist = re.findall(p,html)
    t=[]
    for each in imglist:
        a=threading.Thread(target=dl_img,args=(each,headers))
        a.start()
        t.append(a)
if __name__=='__main__':
    
    while 1:
        url=input('输入专辑号:')
        url='http://www.mzitu.com/'+url
        html_new_dir=open_url(url)
        new_dir_name = re.findall('<title>(.+?)</title>',html_new_dir)[0]
        dir_exist = os.path.isdir(new_dir_name)
        if dir_exist:
            continue
        os.mkdir(new_dir_name)
        os.chdir(new_dir_name)
        thread_c0=threading.active_count()
        for i in range(1,100):
            url_new = url+'/'+str(i)
            #print(url_new)
            headers={'User-Agent':'Mozilla/5.0 (Windows\
NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Geck\
o) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5221.\
400 QQBrowser/10.0.1125.400',  'Accept-Encoding':' gzip, deflate','Referer':url_new}
            a= open_url(url_new,headers=headers)
            if i <= 1:#此处用于找最后一页
                new_href = re.findall(r'><span>(\d+?)</span></a>',a)
                l_new_href=len(new_href)#临时变量
                for ll_new_href in range(l_new_href):
                    new_href[ll_new_href]=int(new_href[ll_new_href])
                max_page=max(new_href)
            if i>max_page:
                break
            get_img(a,headers)
            time.sleep(0.1)
        thread_c1=threading.active_count()
        while(thread_c1-thread_c0 != 0):
            time.sleep(1)
            thread_c1=threading.active_count()
            print('初始线程数：'+str(thread_c0))
            print('当前线程数：'+str(thread_c1))
        os.chdir('..')
        time.sleep(0.2)
