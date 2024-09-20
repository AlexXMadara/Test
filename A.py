def register_facebook_account(email, password, first_name, last_name, birthday):
    api_key = '882a8490361da98702bf97a021ddc14d'
    secret = '62f8ce9f74b12f84c123cc23437a4a32'
    gender = random.choice(['M', 'F'])
    req = {'api_key': api_key, 'attempt_login': True, 'birthday': birthday.strftime('%Y-%m-%d'),
           'client_country_code': 'EN', 'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
           'fb_api_req_friendly_name': 'registerAccount', 'firstname': first_name, 'format': 'json', 'gender': gender,
           'lastname': last_name, 'email': email, 'locale': 'en_US', 'method': 'user.register', 'password': password,
           'reg_instance': generate_random_string(32), 'return_multiple_errors': True}
    sorted_req = sorted(req.items(), key=lambda x: x[0])
    sig = ''.join(f'{k}={v}' for k, v in sorted_req)
    ensig = hashlib.md5((sig + secret).encode()).hexdigest()
    req['sig'] = ensig
    api_url = 'https://b-api.facebook.com/method/user.register'
    reg = _call(api_url, req)
    
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
        ﴾𝐕𝐈𝐏﴿GENDER : {gender}
        ⋘▬▭▬▭▬▭▬﴾𓆩OK𓆪﴿▬▭▬▭▬▭▬⋙
        ﴾𝐕𝐈𝐏﴿ Token : {token}
        ⋘▬▭▬▭▬▭▬﴾𓆩OK𓆪﴿▬▭▬▭▬▭▬⋙''')
    else:
        print(f'[×] Registration failed. Response: {reg}')
