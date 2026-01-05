import os
import requests
from extract_authtoken import extract_authtoken
from send_notification import send_promotion_notification, send_error_notification

from dotenv import load_dotenv

load_dotenv()

def create_session(auth_token):
    cookie_raw = f'authtoken={auth_token}'
    headers = {
        'Cookie': cookie_raw
    }
    session = requests.Session()
    session.headers.update(headers)
    return session

def get_promotions(session):
    url = 'https://www.lidl.cz/prm/api/v1/CZ/promotionslist?language=cs-CZ'
    r = session.get(url)
    data = r.json()
    all_promotions = []
    for section in data['sections']:
        all_promotions.extend(section['promotions'])
    return all_promotions

def activate_promotion(session, promotion_id):
    """
    Activates a promotion.
    Returns True if the promotion was activated successfully, False if the promotion was already activated.
    """
    url = f'https://www.lidl.cz/prm/api/v1/CZ/promotions/{promotion_id}/activation?language=cs-CZ'
    r = session.post(url)
    print(r.status_code)
    return r.status_code == 202

def main():
    try:
        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')

        auth_token = extract_authtoken(email, password)
        print('Using auth token: ', auth_token)

        session = create_session(auth_token)
        promotions = get_promotions(session)
        print('Total promotions:', len(promotions))

        n_activated = 0
        for promotion in promotions:
            if activate_promotion(session, promotion['id']):
                n_activated += 1
                print('Activated promotion:', promotion['description'])
        print('Activated', n_activated, 'promotions')

        send_promotion_notification(n_activated)
    except Exception as e:
        print('Error:', e)
        send_error_notification(str(e))

if __name__ == "__main__":
    main()
