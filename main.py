import requests
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from twilio.rest import Client
from bs4 import BeautifulSoup


def main():
    url =  'https://kashdout.com/vip-package'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    cities = ['Orlando', 'Daytona', 'Sanford', 'Cocoa']
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('\n---- checking for new cities ------')
    print(time_stamp)
    print('\n')


    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response.status_code)
        print('Request failed!')
        exit()

    # parse page content
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    entries = soup.find_all('tr', class_='border-accent')
    published_cities = soup.find_all('span')

    found_vip = {}

    for city in cities:
        print('Checking ' + city)

        for published_city in published_cities:
            if city in published_city.text:
            # print(city + ' is a match!')
                found_vip[city] = True

    print('Found cities:')
    print(found_vip)


    if len(found_vip) > 0:
        send_text(found_vip)
        send_email(found_vip)
    else:
        # nothing was found, so check if we are at the top of the hour, and if so, send a message
        print('No VIP packages found!')
        if at_top_of_hour():
            send_email(None)



def send_email(found_vip_cities):
    print('Sending email...')
    
    
    # Email account credentials
    username = os.environ.get('EMAILUSER')
    password = os.environ.get('EMAILPASS')  

    # construct the email message
    if found_vip_cities is None:
        msg_content = "No VIP packages found."
        subject_content = 'Just letting you know nothing new has been posted, but the script is still running.'
    else:
        msg_content = "I think the Kash'd Out VIP package is posted for the following cities:\n\n"
        msg_content += '\n'.join(found_vip_cities.keys())
        subject_content = 'KashdOut VIP Package Posted'

    # Create the email message
    msg = EmailMessage()
    msg.set_content(msg_content)
    msg['Subject'] = subject_content
    msg['From'] = username
    msg['To'] = os.environ.get('EMAILTO')

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(username, password)
        smtp.send_message(msg)
        print("Email sent successfully!")


def send_text(found_vip_cities):
    print('Sending text message...')
    
    account_sid = os.environ.get('TWILSID')
    auth_token = os.environ.get('TWILTOKEN')

    from_number = os.environ.get('TWILFROM')
    to_number = os.environ.get('TWILTO')

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body='TEST: Looks like VIP is posted!?',
            from_ =from_number,
            to=to_number
        )

    print(message.sid)


def at_top_of_hour():
    # Get the current time
    now = datetime.now()
    
    # Calculate the number of minutes to the next hour
    minutes_to_hour = 60 - now.minute
    print(minutes_to_hour)

    # Check if the current time is within 1 minutes of the next hour
    if (minutes_to_hour < 2) or (minutes_to_hour == 59):
        return True
    return False

main()


print('---- DONE ------')

