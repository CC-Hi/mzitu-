import urllib.request
import re
import time
import urllib.parse
import os
import gzip

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

def get_img(html,headers):
    p = r'<img src="([^"]+.jpg)"'
    imglist = re.findall(p,html)
    for each in imglist:
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
if __name__=='__main__':
    m_name_search=input('输入要搜索的妹子（输入‘1’到首页）：')
    if m_name_search == '1':
        o_url = 'http://www.mzitu.com/'
    else:
        m_search = urllib.parse.quote(m_name_search)
        o_url = 'http://www.mzitu.com/search/'+m_search
    urllist=get_url(o_url)
    a_cont=0
    exist_dir_search =os.path.isdir(m_name_search)
    if not exist_dir_search:
        os.mkdir(m_name_search)
    os.chdir(m_name_search)
    download_time = input('输入要下的专辑数：')
    while not download_time.isnumeric():
        download_time = input('请输入数字：')
    download_time = int(download_time)
    download_time_counter = 1  #下载的专辑数计数
    for url in urllist:
        print(url)
        html_new_dir=open_url(url)
        new_dir_name = re.findall('<title>(.+?)</title>',html_new_dir)[0]
        dir_exist = os.path.isdir(new_dir_name)
        if dir_exist:
            continue
        os.mkdir(new_dir_name)
        os.chdir(new_dir_name)
        for i in range(1,100):
            url_new = url+'/'+str(i)
            print(url_new)
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
            a_cont += 1
            print(a_cont)
            time.sleep(0.1)
        os.chdir('..')
        if download_time_counter >= download_time:
            break
        download_time_counter +=1
        time.sleep(0.2)
