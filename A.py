import requests
import random
import string
import json
import hashlib
from faker import Faker
import time

# Function to generate random strings
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# Use temp-mailfree.com to get a temporary email
def create_temp_mailfree_account():
    fake = Faker()
    
    url = "https://api.temp-mailfree.com/request/mail/id"  # Endpoint to generate an email
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            email_info = response.json()
            email = email_info['email']
            password = fake.password()
            birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)
            first_name = fake.first_name()
            last_name = fake.last_name()
            print(f'[+] Mail account created: {email}')
            return email, password, first_name, last_name, birthday
        else:
            print(f'[×] Error creating email: {response.text}')
            return None, None, None, None, None
    except Exception as e:
        print(f'[×] Error: {e}')
        return None, None, None, None, None

# Check incoming mail after account creation
def check_incoming_mail(email):
    url = f"https://api.temp-mailfree.com/request/mail/{email}/"
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            mails = response.json()
            if mails:
                print(f"[+] Incoming mail for {email}: {mails}")
            else:
                print(f"[×] No new mail for {email}")
        else:
            print(f"[×] Error checking mail: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[×] Error: {e}")

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
        print(f"[×] Rate limit detected. Pausing for 11 seconds...")
        time.sleep(11)  # Pause for 11 seconds instead of 6 hours
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

    while successful_accounts < num_accounts:
        email, password, first_name, last_name, birthday = create_temp_mailfree_account()
        if email and password and first_name and last_name and birthday:
            success = register_facebook_account(email, password, first_name, last_name, birthday)
            if success:
                successful_accounts += 1
                print(f'[+] Successfully created {successful_accounts}/{num_accounts} accounts.')
            
            # Check for incoming mail after account creation
            check_incoming_mail(email)
            
            time.sleep(120)  # wait for 2 minutes between account creation attempts
