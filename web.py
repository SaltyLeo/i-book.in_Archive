# -*- coding: utf-8 -*-
import re
import time
import uuid
from flask import Flask
from flask import render_template
from flask import request
from flask import abort
import urllib.request
from flask import url_for
from elasticsearch import Elasticsearch
from flask_bootstrap import Bootstrap
es = Elasticsearch()
app=Flask(__name__,static_url_path='')
bootstrap=Bootstrap(app)
app.secret_key = '!!!A0Zr98j/3yX R~XHH!jmN]LWX/,?RT!!'

def get_cf_ip(reh):
    cri = re.findall(r'Cf-Connecting-Ip: (.*?) ',str(reh))
    return cri

def getipfss(d):
    try:
        res = es.search(index="es", body={"query":{"match":{'ids':'%s'%d}}})      
        raw_data = res['hits']['hits'][0]
        getipfs = raw_data['_source']['link']
        return getipfs
    except:
        return False   

def getlink(pn,num,str):
    try:
        res = es.search(index="es", body={"query":{"multi_match":{'query':'%s'%str,'fields':['name','author','isbn']}},"from":pn,"size":20})
        raw_data = res['hits']['hits'][int(num)]
        getlink = raw_data['_source']['link']
        return getlink
    except:
        return False    

def getbookinfo(pn,num,str):
    try:
        res = es.search(index="es", body={"query":{"multi_match":{'query':'%s'%str,'fields':['name','author','isbn']}},"from":pn,"size":20})
        raw_data = res['hits']['hits'][int(num)]
        book_name = raw_data['_source']['name']
        book_author = raw_data['_source']['author']
        if book_author == 'None':
            book_author = ''
        book_intor = raw_data['_source']['intor']
        if book_intor == 'None':
            book_intor = ''
        book_isbn = raw_data['_source']['isbn']
        if book_isbn == 'None':
            book_isbn = ''
        book_press = raw_data['_source']['press']
        if book_press == 'None':
            book_press = ''
        book_douban = raw_data['_source']['douban']
        if book_douban == 'None':
            book_douban = ''
        book_tags = raw_data['_source']['tags']
        if book_tags == 'None':
            book_tags = ''
        book_img = raw_data['_source']['img']
        book_link = raw_data['_source']['link']
        book_type = raw_data['_source']['type']
        book_type = book_type.replace('《','<img class="dim" src="/type/').replace('》','.svg"  height="20" > ')
        book_size = raw_data['_source']['size']
        book_size = format(float(int(book_size))/float(1000000),'.2f') 
        link = "%s&p=%s&n=%s"%(str,pn,num)
        bookinfos = book_name,book_author,book_intor,book_isbn,book_press,book_douban,book_tags,book_img,link,book_type,book_size
        return bookinfos
    except:
        return False

def essbook(pn,str):
    try:
        page_li = []
        res = es.search(index="es", body={"query":{"multi_match":{'query':'%s'%str,'fields':['name','author','isbn']}},"from":pn,"size":20})
        search_max = len(res['hits']['hits'])
        if search_max == 0:
            return False
        else:
            for i in range(0,search_max):
                raw_data = res['hits']['hits'][i]
                book_name = raw_data['_source']['name']
                book_author = raw_data['_source']['author']
                if book_author == 'None':
                    book_author = ''
                else:
                    book_author = '-%s'%book_author
                book_intor = raw_data['_source']['intor']
                if book_intor == 'None':
                    book_intor = 'None'
                else:
                    book_intor = book_intor[0:70]
                book_isbn = raw_data['_source']['isbn']
                book_press = raw_data['_source']['press']
                book_douban = raw_data['_source']['douban']
                book_tags = raw_data['_source']['tags']
                book_img = raw_data['_source']['img']
                book_type = raw_data['_source']['type']
                book_type = book_type.replace('《','<img class="dim" src="/type/').replace('》','.svg"  height="14" > ')
                book_size = raw_data['_source']['size']
                book_size = format(float(int(book_size))/float(1000000),'.2f')      
                link = "%s&p=%s&n=%s"%(str,pn,i)
                single_info = book_name,book_author,book_size,link,book_type
                page_li.append(single_info)
            return page_li
    except:
        return False

def guessbook(str1):
    
    res = es.search(index="es", body={"query":{"match":{'intor':'的'}},"sort": {"_script": {"script": "Math.random()","type": "number",}}})
    ##app.logger.info(res)
    raw_data = res['hits']['hits'][0]
    book_name = raw_data['_source']['name']
    book_author = raw_data['_source']['author']
    if book_author == 'None':
        book_author = ''
    book_intor = raw_data['_source']['intor']
    book_isbn = raw_data['_source']['isbn']
    book_press = raw_data['_source']['press']
    book_douban = raw_data['_source']['douban']
    book_tags = raw_data['_source']['tags']
    book_img = raw_data['_source']['img']
    #book_link = raw_data['_source']['link']
    link = raw_data['_source']['ids']
    book_type = raw_data['_source']['type']
    book_type = book_type.replace('《','<img class="dim" src="/type/').replace('》','.svg"  height="20" > ')
    book_size = raw_data['_source']['size']
    book_size = format(float(int(book_size))/float(1000000),'.2f') 
    #link = "%s&p=%s&n=%s"%(str,pn,num)
    bookinfos = book_name,book_author,book_intor,book_isbn,book_press,book_douban,book_tags,book_img,link,book_type,book_size
    return bookinfos


@app.route('/ads.txt')
def ads():
    return render_template('ads.txt')

@app.route('/sitemap/<num>')
def sitemap(num):
    return render_template('/sitemap/%s'%num)


@app.route('/')
def index():
    cfip = request.headers.get("Cf-Connecting-Ip")
    return render_template("index.html",ip = cfip)

@app.route('/about')
def about():
    cfip = request.headers.get("Cf-Connecting-Ip")
    return render_template('about.html',ip = cfip)

@app.route('/help')
def help():
    cfip = request.headers.get("Cf-Connecting-Ip")
    return render_template('help.html',ip = cfip)

@app.route('/donate')
def donate():
    cfip = request.headers.get("Cf-Connecting-Ip")
    return render_template('donate.html',ip = cfip)
    
@app.route('/dmca')
def dmca():
    cfip = request.headers.get("Cf-Connecting-Ip")
    return render_template('dmca.html',ip = cfip)

@app.route('/guess')
def guess():
    cfip = request.headers.get("Cf-Connecting-Ip")
    try:
        if request.method=='GET':
            bookinfos = guessbook(0)
            return render_template('guess.html',bookinfos = bookinfos,ip = cfip)
        else:
            errors = '无效的链接！'
            return render_template("info.html" ,errors = errors,ip = cfip)
    except:
        errors = '无效的链接！'
        return render_template("info.html" ,errors = errors,ip = cfip)

@app.route('/ipfsd')
def get3():
    cfip = request.headers.get("Cf-Connecting-Ip")
    try:
        if request.method=='GET':
            d=request.args.get('d')
            #app.logger.info(d)  
            getlinks = getipfss(d)
            #app.logger.info(getlinks)  
            l=request.args.get('l')
            if getlinks == False:
                errors = '无效的链接！Invalid link!'
                return render_template("info.html" ,errors = errors,ip = cfip)
            else:
                if l == 'zh':
                    return render_template("jump.html",getlinks = getlinks,ip = cfip)
                elif l == 'en':
                    return render_template("jump.html",getlinks = getlinks,ip = cfip,l = l)
                else:
                    errors = '无效的链接！Invalid link!'
                    return render_template("info.html" ,errors = errors,ip = cfip)
    except:
        errors = '无效的链接！Invalid link!'
        return render_template("info.html" ,errors = errors,ip = cfip)

@app.route('/ipfs')
def get2():
    cfip = request.headers.get("Cf-Connecting-Ip")
    try:
        if request.method=='GET':
            s=request.args.get('s')
            p=request.args.get('p')
            n=request.args.get('n')
            l=request.args.get('l')
            getlinks = getlink(p,n,s)
            if getlinks == False:
                errors = '无效的链接！Invalid link!'
                return render_template("info.html" ,errors = errors,ip = cfip)
            else:
                if l == 'zh':
                    return render_template("jump.html",getlinks = getlinks,ip = cfip)
                elif l == 'en':
                    return render_template("jump.html",getlinks = getlinks,ip = cfip,l = l)
                else:
                    errors = '无效的链接！Invalid link!'
                    return render_template("info.html" ,errors = errors,ip = cfip)
    except:         
        errors = '无效的链接！Invalid link!'
        return render_template("info.html" ,errors = errors,ip = cfip)

@app.route('/det')
def info():
    cfip = request.headers.get("Cf-Connecting-Ip")
    try:
        if request.method=='GET':
            s=request.args.get('s')
            p=request.args.get('p')
            n=request.args.get('n')
            bookinfos = getbookinfo(p,n,s)
            app.logger.info(bookinfos) 
            if bookinfos == False:
                errors = '无效的链接！2'
                return render_template("info.html",bookinfos = bookinfos,errors = errors,ip = cfip)
            else:
                return render_template("info.html",bookinfos = bookinfos,ip = cfip)
    except:
        errors = '无效的链接！1'
        return render_template("info.html",bookinfos = bookinfos,errors = errors,ip = cfip)

@app.route('/find')
def search():
    cfip = request.headers.get("Cf-Connecting-Ip")
    if request.method=='GET':
        try:
            q=request.args.get('q')
            try:
                p=int(request.args.get('p'))
                if p == 1:
                    prp = 1
                    pnn = 2
                    p = 0
                    dis = ['disable','']
                    nclicks = ['button','submit']
                elif p == 2:
                    prp = 1
                    pnn = 3
                    p = 20
                    dis = ['','']
                    nclicks = ['submit','submit']
                elif p == 3:
                    prp = 2
                    pnn = 0
                    p = 40
                    dis = ['','disable']
                    nclicks = ['submit','button']
                elif p > 3:
                    prp = 0
                    pnn = 0
                    p = 0
                    dis = ['disable','disable']
                    nclicks = ['button','button']
                    return render_template("result.html",q = q,prp = prp,dis = 'disable',pnn = pnn,nclicks = nclicks,errors = '由于性能限制，目前仅提供三页结果，如没找到你想要的书，那就是这里没有啦。',ip = cfip)
                else:
                    prp = 0
                    pnn = 0
                    p = 0
                    dis = ['disable','disable']
                    nclicks = ['button','button']
                    return render_template("result.html",q = q,prp = prp,dis = 'disable',pnn = pnn,nclicks = nclicks,errors = '你的输入有误！',ip = cfip)
            except:
                prp = 1
                pnn = 2
                p = 0
                dis = ['disable','']
                nclicks = ['button','submit']
            if q:
                page_li = essbook(p,q)
                if page_li == False:
                    return render_template("result.html",q = q,prp = prp,dis = 'disable',pnn = pnn,nclicks = nclicks,errors = '没找到与 %s 相关的结果'%q,ip = cfip)
                return render_template("result.html",q = q,prp = prp,dis = dis,pnn = pnn,nclicks = nclicks,page_li = page_li,ip = cfip)
            else:
                prp = 0
                pnn = 0
                p = 0
                dis = ['disable','disable']
                nclicks = ['button','button']
                return render_template("result.html",q = q,prp = prp,dis = 'disable',pnn = pnn,nclicks = nclicks,errors = '你的输入有误！',ip = cfip)
        except:
            prp = 0
            pnn = 0
            p = 0
            dis = ['disable','disable']
            nclicks = ['button','button']
            return render_template("result.html",q = q,prp = prp,dis = 'disable',pnn = pnn,nclicks = nclicks,errors = '你的输入有误！',ip = cfip)
    else:
        prp = 0
        pnn = 0
        p = 0
        dis = ['disable','disable']
        nclicks = ['button','button']
        return render_template("result.html",q = q,prp = prp,dis = 'disable',pnn = pnn,nclicks = nclicks,errors = '你的输入有误！',ip = cfip)

@app.errorhandler(404)
def hello(error):
    cfip = request.headers.get("Cf-Connecting-Ip")
    prp = 0
    pnn = 0
    p = 0
    dis = ['disable','disable']
    nclicks = ['button','button']
    return render_template("result.html",prp = prp,dis = 'disable',pnn = pnn,nclicks = nclicks,errors = 'error！',ip = cfip)
if __name__=="__main__":
    app.run(host="0.0.0.0", port=7743,debug=True) #
