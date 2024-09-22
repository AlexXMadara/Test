import requests
import random
import string
import json
import hashlib
from faker import Faker
import time

# Fetch free proxies from a public proxy API
def get_proxies():
    url = "https://www.proxy-list.download/api/v1/get?type=https"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            return proxies
        else:
            print(f'[×] Failed to fetch proxies: {response.status_code}')
            return []
    except Exception as e:
        print(f'[×] Error fetching proxies: {e}')
        return []

# Select a random proxy from the list
def get_random_proxy(proxies):
    if proxies:
        return random.choice(proxies)
    return None

# Function to generate random strings
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# Use temp-mail.gg to get temporary email addresses
def create_temp_mail_gg_account():
    fake = Faker()
    url = "https://api.temp-mail.gg/mailbox"
    headers = {"accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            mailbox_info = response.json()
            email = mailbox_info['email']
            password = fake.password()
            birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)
            first_name = fake.first_name()
            last_name = fake.last_name()
            print(f'[+] Mail account created: {email}')
            return email, password, first_name, last_name, birthday
        else:
            print(f'[×] Email Error : {response.text}')
            return None, None, None, None, None
    except Exception as e:
        print(f'[×] Error : {e}')
        return None, None, None, None, None

# API call function with proxy support
def _call(url, params, proxy=None, post=True):
    headers = {
        'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'
    }
    try:
        if post:
            response = requests.post(url, data=params, headers=headers, proxies=proxy)
        else:
            response = requests.get(url, params=params, headers=headers, proxies=proxy)
        
        return response.json()
    except Exception as e:
        print(f"[×] Error during API call: {e}")
        return {}

# Facebook account registration function
def register_facebook_account(email, password, first_name, last_name, birthday, proxy=None):
    api_key = '882a8490361da98702bf97a021ddc14d'
    secret = '62f8ce9f74b12f84c123cc23437a4a32'
    gender = random.choice(['M', 'F'])
    
    req = {
        'api_key': api_key,
        'attempt_login': True,
        'birthday': birthday.strftime('%Y-%m-%d'),
        'client_country_code': 'EN',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': first_name,
        'format': 'json',
        'gender': gender,
        'lastname': last_name,
        'email': email,
        'locale': 'en_US',
        'method': 'user.register',
        'password': password,
        'reg_instance': generate_random_string(32),
        'return_multiple_errors': True
    }
    
    sorted_req = sorted(req.items(), key=lambda x: x[0])
    sig = ''.join(f'{k}={v}' for k, v in sorted_req)
    ensig = hashlib.md5((sig + secret).encode()).hexdigest()
    req['sig'] = ensig
    api_url = 'https://b-api.facebook.com/method/user.register'
    reg = _call(api_url, req, proxy=proxy)

    # Check for Facebook rate limit error
    if 'error_code' in reg and reg['error_code'] == 368:
        print(f"[×] Rate limit detected. Pausing for 6 hours...")
        time.sleep(6 * 60 * 60)  # Pause for 6 hours
        return False
    
    if 'new_user_id' in reg and 'session_info' in reg:
        id = reg['new_user_id']
        token = reg['session_info']['access_token']
        print(f'''
        ⋘▬▭▬▭▬▭▬﴾𓆩OK𓆪﴿▬▭▬▭▬▭▬⋙
        ﴾𝐕𝐈𝐏﴿ EMAIL : {email}
        ﴾𝐕𝐈𝐏﴿ ID : {id}
        ﴾𝐕𝐈𝐏﴿ PASSWORD : {password}
        ﴾𝐕𝐈𝐏﴿ NAME : {first_name} {last_name}
        ﴾𝐕𝐈𝐏﴿ BIRTHDAY : {birthday}
        ﴾𝐕𝐈𝐏﴿ GENDER : {gender}
        ⋘▬▭▬▭▬▭▬﴾𓆩OK𓆪﴿▬▭▬▭▬▭▬⋙
        ﴾𝐕𝐈𝐏﴿ Token : {token}
        ⋘▬▭▬▭▬▭▬﴾𓆩OK𓆪﴿▬▭▬▭▬▭▬⋙
        ''')
        return True
    else:
        print(f'[×] Registration failed. Response: {reg}')
        return False

# Main script execution
if __name__ == '__main__':
    num_accounts = int(input('[+] How Many Accounts You Want: '))
    successful_accounts = 0
    proxies = get_proxies()  # Fetch proxies

    while successful_accounts < num_accounts:
        email, password, first_name, last_name, birthday = create_temp_mail_gg_account()
        if email and password and first_name and last_name and birthday:
            proxy = get_random_proxy(proxies)
            proxy_dict = {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}'
            } if proxy else None
            print(f'[+] Using proxy: {proxy}')
            
            success = register_facebook_account(email, password, first_name, last_name, birthday, proxy=proxy_dict)
            if success:
                successful_accounts += 1
                print(f'[+] Successfully created {successful_accounts}/{num_accounts} accounts.')
            time.sleep(120)  # wait for 2 minutes between account creation attempts
