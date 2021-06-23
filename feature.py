import subprocess
import regex
import tldextract    
from tldextract import extract
import ssl
import socket
import bs4
import urllib.request
import whois
import datetime
from googlesearch import search
from subprocess import Popen, PIPE
from dateutil.relativedelta import relativedelta
import favicon
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd
from threading import Thread

# ok
def url_having_ip(url):
    import string
    index = url.find("://")
    split_url = url[index+3:]
    # print(split_url)
    index = split_url.find("/")
    split_url = split_url[:index]
    # print(split_url)
    split_url = split_url.replace(".", "")
    # print(split_url)
    counter_hex = 0
    for i in split_url:
        if i in string.hexdigits:
            counter_hex +=1

    total_len = len(split_url)
    having_IP_Address = -1
    if counter_hex >= total_len:
        having_IP_Address = 1

    return having_IP_Address

# ok
def url_length(url):
    length=len(url)
    if(length<54):
        return -1
    elif(54<=length<=75):
        return 0
    else:
        return 1

# ok
def get_complete_URL(shortened_url):
    command_stdout = subprocess.Popen(['curl', shortened_url], stdout=PIPE).communicate()[0]
    output = command_stdout.decode('utf-8')
    href_index = output.find("href=")
    if href_index == -1:
        href_index = output.find("HREF=")
    splitted_ = output[href_index:].split('"')
    expanded_url = splitted_[1]
    return expanded_url

# ok
def check_for_shortened_url(url):
    famous_short_urls = ["bit.ly", "tinyurl.com", "goo.gl",
                        "rebrand.ly", "t.co", "youtu.be",
                        "ow.ly", "w.wiki", "is.gd"]

    domain_of_url = url.split("://")[1]
    domain_of_url = domain_of_url.split("/")[0]
    status = 1
    if domain_of_url in famous_short_urls:
        status = -1

    complete_url = None
    if status == -1:
        complete_url = get_complete_URL(url)

    return status*(-1)

# ok
def having_at_symbol(url):
    symbol=regex.findall(r'@',url)
    if(len(symbol)==0):
        return -1
    else:
        return 1 

# ok
def doubleSlash(url):
    index = url.find("://")
    split_url = url[index+3:]
    label = 1
    index = split_url.find("//")
    if index!=-1:
        label = -1
    return label*(-1)

# ok
def prefix_Suffix(url):
    index = url.find("://")
    split_url = url[index+3:]
    # print(split_url)
    index = split_url.find("/")
    split_url = split_url[:index]
    # print(split_url)
    label = 1
    index = split_url.find("-")
    # print(index)
    if index!=-1:
        label = -1
    
    return label*(-1)

# ok
def sub_Dom(url):
    SubDom, Dom, Suffix = extract(url)
    if(SubDom.count('.')==0):
        return -1
    elif(SubDom.count('.')==1):
        return 0
    else:
        return 1

# ok  
def SSLfinal_State(url):
    try:    
        if(regex.search('https',url)):
            usehttps = 1
        else:
            usehttps = 0
        SubDom, Dom, Suffix = extract(url)
        host_name = Dom + "." + Suffix
        context = ssl.create_default_context()
        sct = context.wrap_socket(socket.socket(), server_hostname = host_name)
        sct.connect((host_name, 443))
        certificate = sct.getpeercert()
        issuer = dict(x[0] for x in certificate['issuer'])
        certificate_Auth = str(issuer['commonName'])
        certificate_Auth = certificate_Auth.split()
        if(certificate_Auth[0] == "Network" or certificate_Auth == "Deutsche"):
            certificate_Auth = certificate_Auth[0] + " " + certificate_Auth[1]
        else:
            certificate_Auth = certificate_Auth[0] 
            
        trusted_Auth = ['Comodo','Symantec','GoDaddy','GlobalSign','DigiCert','StartCom','Entrust','Verizon','Trustwave','Unizeto','Buypass','QuoVadis','Deutsche Telekom','Network Solutions','SwissSign','IdenTrust','Secom','TWCA','GeoTrust','Thawte','Doster','VeriSign']        

        startingDate = str(certificate['notBefore'])
        endingDate = str(certificate['notAfter'])
        startingYear = int(startingDate.split()[3])
        endingYear = int(endingDate.split()[3])
        Age_of_certificate = endingYear-startingYear
        
        if((usehttps==1) and (certificate_Auth in trusted_Auth) and (Age_of_certificate>=1) ):
            return -1 
        
        elif((usehttps==1) and (certificate_Auth not in trusted_Auth)):
            return 0 
        else:
            return 1 
                
    except Exception as e:
        return 1

# ok
def Dom_registration(url):
    try:
        extract_res = tldextract.extract(url)
        ul = extract_res.domain + "." + extract_res.suffix
        
        wres = whois.whois(url)
        # print(wres)
        f = wres["creation_date"][0]
        s = wres["expiration_date"][0]
        if(s>f+relativedelta(months=+12)):
            return -1
        else:
            return 1
    except:
        return 1

# ok
def has_favicon(url):
    try:
        extract_res = tldextract.extract(url)
        url_ref = extract_res.domain

        favs = favicon.get(url)
        # print(favs)
        match = 0
        for favi in favs:
            url2 = favi.url
            extract_res = tldextract.extract(url2)
            url_ref2 = extract_res.domain

            if url_ref in url_ref2:
                match += 1

        if match >= len(favs)/2:
            return -1
        return 1
    except:
        return 0

def port(url):
    # Implement
    return 0

# ok
def https_token(url):
    SubDom, Dom, Suffix = extract(url)
    host =SubDom +'.' + Dom + '.' + Suffix 
    if(host.count('https')): 
        return 1
    else:
        return -1

# ok
def request_url(url):
    try:
        SubDom, Dom, Suffix = extract(url)
        websiteDom = Dom
        
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'lxml')
        imgs = soup.findAll('img', src=True)
        total = len(imgs)
        
        linked_to_same = 0
        avg =0
        for image in imgs:
            SubDom, Dom, Suffix = extract(image['src'])
            imageDom = Dom
            if(websiteDom==imageDom or imageDom==''):
                linked_to_same = linked_to_same + 1
        vids = soup.findAll('video', src=True)
        total = total + len(vids)
        
        for video in vids:
            SubDom, Dom, Suffix = extract(video['src'])
            vidDom = Dom
            if(websiteDom==vidDom or vidDom==''):
                linked_to_same = linked_to_same + 1
                
        linked_outside = total-linked_to_same
        if(total!=0):
            avg = linked_outside/total
            
        if(avg<0.22):
            return -1
        elif(0.22<=avg<=0.61):
            return 0
        else:
            return 1
    except:
        return 0

# ok
def email_submit(url):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    # Check if no form tag
    form_opt = str(soup.form)
    idx = form_opt.find("mail()")
    if idx == -1:
        idx = form_opt.find("mailto:")

    if idx == -1:
        return -1
    return 1

# ok
def sfh(u):
    programhtml = requests.get(u).text
    s = BeautifulSoup(programhtml,"lxml")
    try:
        f = str(s.form)
        ac = f.find("action")
        if(ac!=-1):
            i1 = f[ac:].find(">")
            u1 = f[ac+8:i1-1]
            if(u1=="" or u1=="about:blank"):
                return 1
            erl = tldextract.extract(u)
            upage = erl.domain
            erl2 = tldextract.extract(u1)
            usfh = erl2.domain
            if upage in usfh:
                return -1
            return 0
        else:
            # Check this point
            return -1
    except:
        # Check this point
        return 1

# ok
def url_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

# ok
def check_URL_of_anchor(url):
    extract_res = tldextract.extract(url)
    url_ref = extract_res.domain
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    a_tags = soup.find_all('a')

    if len(a_tags) == 0:
        return -1

    invalid = ['#', '#content', '#skip', 'JavaScript::void(0)']
    bad_count = 0
    for t in a_tags:
        link = t['href']

        if link in invalid:
            bad_count += 1

        if url_validator(link):
            extract_res = tldextract.extract(link)
            url_ref2 = extract_res.domain

            if url_ref not in url_ref2:
                bad_count += 1

    bad_count /= len(a_tags)

    if bad_count < 0.31:
        return -1
    elif bad_count <= 0.67:
        return 0
    return 1

# ok
def get_pagerank(url):
    pageRankApi = 'c0wg4sscg80coo04kg488448gsggc8k4w4csk0sc'
    extract_res = tldextract.extract(url)
    url_ref = extract_res.domain + "." + extract_res.suffix
    headers = {'API-OPR': pageRankApi}
    domain = url_ref
    req_url = 'https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D=' + domain
    request = requests.get(req_url, headers=headers)
    result = request.json()
    # print(result)
    value = result['response'][0]['page_rank_decimal']
    # print(value)
    if type(value) == str:
        value = 0

    if value < 2:
        return 1
    return -1


def stat_report(url):
    return 0

# ok
def check_web_traffic(url):
    extract_res = tldextract.extract(url)
    url_ref = extract_res.domain + "." + extract_res.suffix
    html_content = requests.get("https://www.alexa.com/siteinfo/" + url_ref).text
    soup = BeautifulSoup(html_content, "lxml")
    value = str(soup.find('div', {'class': "rankmini-rank"}))[42:].split("\n")[0].replace(",", "")

    if not value.isdigit():
        return 1

    value = int(value)
    if value < 100000:
        return -1
    return 0

# ok
def check_dns_record(url):
    extract_res = tldextract.extract(url)
    url_ref = extract_res.domain + "." + extract_res.suffix
    try:
        whois_res = whois.whois(url)
        return -1
    except:
        return 1

# ok
def check_iframe(url):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    if str(soup.iframe).lower().find("frameborder") == -1:
        return -1
    return 1

def get_port(url):
    return 0

def link_in_tag(url):
    return 0

def abnormal_url(url):
    return 0

def check_redirect(url):
    return 0

def on_mouseover(url):
    return 0

def on_RightClick(url):
    return 0

def popUpWidnow(url):
    return 0

def get_age_of_domain(url):
    return 0

def check_google_index(url):
    return 0

def check_links_to_page(url):
    return 0

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def get_all_features(url):
    having_IP_Address_th = ThreadWithReturnValue(target=url_having_ip, args=(url,))         
    URL_Length_th = ThreadWithReturnValue(target=url_length, args=(url,))
    Shortining_Service_th = ThreadWithReturnValue(target=check_for_shortened_url, args=(url,))
    having_At_Symbol_th = ThreadWithReturnValue(target=having_at_symbol, args=(url,))         
    double_slash_redirecting_th = ThreadWithReturnValue(target=doubleSlash, args=(url,))
    Prefix_Suffix_th = ThreadWithReturnValue(target=prefix_Suffix, args=(url,))              
    having_Sub_Domain_th = ThreadWithReturnValue(target=sub_Dom, args=(url,))         
    SSLfinal_State_th = ThreadWithReturnValue(target=SSLfinal_State, args=(url,))             
    Domain_registeration_length_th = ThreadWithReturnValue(target=Dom_registration, args=(url,))
    Favicon_th = ThreadWithReturnValue(target=has_favicon, args=(url,))                    
    port_th =  ThreadWithReturnValue(target=get_port, args=(url,))                      
    HTTPS_token_th =  ThreadWithReturnValue(target=https_token, args=(url,))               
    Request_URL_th = ThreadWithReturnValue(target=request_url, args=(url,))             
    URL_of_Anchor_th = ThreadWithReturnValue(target=check_URL_of_anchor, args=(url,))            
    Links_in_tags_th = ThreadWithReturnValue(target=link_in_tag, args=(url,))              
    SFH_th = ThreadWithReturnValue(target=sfh, args=(url,))                        
    Submitting_to_email_th = ThreadWithReturnValue(target=email_submit, args=(url,))       
    Abnormal_URL_th = ThreadWithReturnValue(target=abnormal_url, args=(url,))               
    Redirect_th = ThreadWithReturnValue(target=check_redirect, args=(url,))                  
    on_mouseover_th = ThreadWithReturnValue(target=on_mouseover, args=(url,))               
    RightClick_th = ThreadWithReturnValue(target=on_RightClick, args=(url,))                  
    popUpWidnow_th = ThreadWithReturnValue(target=popUpWidnow, args=(url,))                
    Iframe_th = ThreadWithReturnValue(target=check_iframe, args=(url,))                     
    age_of_domain_th = ThreadWithReturnValue(target=get_age_of_domain, args=(url,))
    DNSRecord_th = ThreadWithReturnValue(target=check_dns_record, args=(url,))                  
    web_traffic_th = ThreadWithReturnValue(target=check_web_traffic, args=(url,))                 
    Page_Rank_th = ThreadWithReturnValue(target=get_pagerank, args=(url,))                 
    Google_Index_th = ThreadWithReturnValue(target=check_web_traffic, args=(url,))              
    Links_pointing_to_page_th = ThreadWithReturnValue(target=check_links_to_page, args=(url,))     
    Statistical_report_th = ThreadWithReturnValue(target=stat_report, args=(url,))

    having_IP_Address_th.start()         
    URL_Length_th.start()
    Shortining_Service_th.start()
    having_At_Symbol_th.start()        
    double_slash_redirecting_th.start()
    Prefix_Suffix_th.start()              
    having_Sub_Domain_th.start()        
    SSLfinal_State_th.start()            
    Domain_registeration_length_th.start()
    Favicon_th.start()                    
    port_th.start()                      
    HTTPS_token_th.start()               
    Request_URL_th.start()            
    URL_of_Anchor_th.start()           
    Links_in_tags_th.start()              
    SFH_th.start()                      
    Submitting_to_email_th.start()      
    Abnormal_URL_th.start()               
    Redirect_th.start()                 
    on_mouseover_th.start()              
    RightClick_th.start()                
    popUpWidnow_th.start()              
    Iframe_th.start()                    
    age_of_domain_th.start()
    DNSRecord_th.start()               
    web_traffic_th.start()              
    Page_Rank_th.start()                
    Google_Index_th.start()              
    Links_pointing_to_page_th.start()     
    Statistical_report_th.start()

    data = {
            'having_IP_Address' : having_IP_Address_th.join(),         
            'URL_Length' : URL_Length_th.join(), 
            'Shortining_Service' : Shortining_Service_th.join(),                
            'having_At_Symbol' : having_At_Symbol_th.join(),         
            'double_slash_redirecting' : double_slash_redirecting_th.join(),
            'Prefix_Suffix' : Prefix_Suffix_th.join(),              
            'having_Sub_Domain' : having_Sub_Domain_th.join(),         
            'SSLfinal_State' : SSLfinal_State_th.join(),             
            'Domain_registeration_length' : Domain_registeration_length_th.join(),
            'Favicon' : Favicon_th.join(),                    
            'port' :  port_th.join(),                      
            'HTTPS_token' :  HTTPS_token_th.join(),               
            'Request_URL' : Request_URL_th.join(),             
            'URL_of_Anchor' : URL_of_Anchor_th.join(),            
            'Links_in_tags' : Links_in_tags_th.join(),              
            'SFH' : SFH_th.join(),                        
            'Submitting_to_email' : Submitting_to_email_th.join(),       
            'Abnormal_URL' : Abnormal_URL_th.join(),               
            'Redirect' : Redirect_th.join(),                  
            'on_mouseover' : on_mouseover_th.join(),               
            'RightClick' : RightClick_th.join(),                  
            'popUpWidnow' : popUpWidnow_th.join(),                
            'Iframe' : Iframe_th.join(),                      
            'age_of_domain' : age_of_domain_th.join(),
            'DNSRecord' : DNSRecord_th.join(),                  
            'web_traffic' : web_traffic_th.join(),                 
            'Page_Rank' : Page_Rank_th.join(),                 
            'Google_Index' : Google_Index_th.join(),              
            'Links_pointing_to_page' : Links_pointing_to_page_th.join(),     
            'Statistical_report' : Statistical_report_th.join()                
    }
    
    df = pd.DataFrame(data,index = [0])
    return df
