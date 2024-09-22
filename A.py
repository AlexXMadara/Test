import time
import random
import string
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker

# Function to generate random strings
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# Function to scrape temporary email from temp-mail.gg
def get_temp_mail():
    # Set up Selenium and ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU for headless performance
    options.add_argument('--no-sandbox')
    
    # Create a new instance of ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Visit the temp-mail.gg mailbox page
        driver.get("https://temp-mail.gg/mailbox")
        
        # Wait for the email address to be generated and displayed
        time.sleep(5)  # Adjust the sleep time if needed for page load
        
        # Locate the generated email address
        email_element = driver.find_element(By.XPATH, '//*[@id="email"]')
        email_address = email_element.get_attribute('value')
        
        print(f"[+] Temporary email generated: {email_address}")
        return email_address
    except Exception as e:
        print(f"[×] Error while fetching temp mail: {e}")
        return None
    finally:
        # Close the browser
        driver.quit()

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
        # Fetch temp mail from temp-mail.gg
        email = get_temp_mail()
        if email:
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
            
            time.sleep(120)  # wait for 2 minutes between account creation attempts
