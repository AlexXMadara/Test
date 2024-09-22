import requests
import random
import string
import hashlib
import time
from faker import Faker

# Your ZylaLabs Temp Email Service API Key
API_ACCESS_KEY = "Bearer 5375|xYI3xBIADR1BW03ndXAQnrFDqcd0MIRgavIIVYXh"

# Function to generate random strings (for reg_instance and password)
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# Function to generate temporary email using ZylaLabs Temp Email API
def get_temp_mail():
    url = "https://zylalabs.com/api/5076/temp+email+service+api/6455/generate+temp+email"
    headers = {
        'Authorization': API_ACCESS_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            email_info = response.json()
            email_address = email_info['email']
            token = email_info['token']
            print(f"[+] Temporary email generated: {email_address}")
            return email_address, token
        else:
            print(f"[×] Error fetching temp mail: {response.status_code} - {response.text}")
            return None, None
    except Exception as e:
        print(f"[×] Error: {e}")
        return None, None

# Function to verify the inbox for new emails using ZylaLabs Temp Email API
def verify_inbox(email, token):
    url = f"https://zylalabs.com/api/5076/temp+email+service+api/6453/verify+inbox?email={email}&token={token}"
    headers = {
        'Authorization': API_ACCESS_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"[+] Inbox verified for {email}")
            return response.json()
        else:
            print(f"[×] Error verifying inbox: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"[×] Error: {e}")

# API call function for Facebook registration
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
        time.sleep(11)  # Pause for 11 seconds
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

    fake = Faker()

    while successful_accounts < num_accounts:
        # Fetch temp mail and token from ZylaLabs Temp Email API
        email, token = get_temp_mail()
        if email and token:
            # Generate random user details
            password = fake.password()
            first_name = fake.first_name()
            last_name = fake.last_name()
            birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)

            # Attempt to register a Facebook account
            success = register_facebook_account(email, password, first_name, last_name, birthday)
            if success:
                successful_accounts += 1
                print(f'[+] Successfully created {successful_accounts}/{num_accounts} accounts.')
            
            # Verify the inbox for confirmation emails
            inbox_data = verify_inbox(email, token)
            if inbox_data:
                print(f"[+] Inbox data for {email}: {inbox_data}")
            
            time.sleep(120)  # wait for 2 minutes between account creation attempts
