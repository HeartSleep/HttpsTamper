from mitmproxy import http
import urllib,re,hashlib
from pprint import pprint
'''
requst ref
https://github.com/mitmproxy/mitmproxy/blob/3cd37652709292cffa1bc733134cef5483489341/mitmproxy/http.py
'''

def request(flow: http.HTTPFlow) -> None:


    if 'xxx.com' in flow.request.host:
        if "POST"== flow.request.method:
            hl = hashlib.md5()
            if flow.request.urlencoded_form:
                # If there's already a form, one can just add items to the dict:
                a = ""
                for k in flow.request.urlencoded_form.keys():
                    a = a + "&" + k + "=" + flow.request.urlencoded_form[k]
                a = a.strip('&')
                # a = urllib.unquote(a)
                a = re.sub('&sign=\w+', "", a)
                arr = a.split("&")
                arr = sorted(arr)
                # print s
                s = "&".join(arr)
                s = s + 'xxxx_SALT_AKJfoiwer394Jeiow4u309'
                print(s)
                hl.update(s.encode(encoding='utf-8'))
                print(hl.hexdigest())

                low.request.urlencoded_form['sign']=hl.hexdigest()
        if "GET" ==flow.request.method:
            hl = hashlib.md5()
            a = ""
            for k in flow.request.query.keys():
                a = a + "&" + k + "=" + flow.request.query[k]
            a = a.strip('&')
            # a = urllib.unquote(a)
            a = re.sub('&sign=\w+', "", a)
            arr = a.split("&")
            arr = sorted(arr)
            # print s
            s = "&".join(arr)
            s = s + 'xxx_SALT_AKJfoiwer394Jeiow4u309'
            print(s)
            hl.update(s.encode(encoding='utf-8'))
            print(hl.hexdigest())
            flow.request.query["sign"] = hl.hexdigest()



