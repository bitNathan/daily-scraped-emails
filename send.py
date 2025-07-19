import smtplib 
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from bleach import clean
from bleach.css_sanitizer import CSSSanitizer
from dotenv import load_dotenv

def log_into_email(email_addr:str, password:str):
    # TODO catch errors, actually impliment error handling everywhere, not just here
    gmail_server= "smtp.gmail.com"
    gmail_port= 587

    server = smtplib.SMTP(gmail_server, gmail_port, timeout=5)

    server.ehlo()
    server.starttls()

    server.login(email_addr, password)
    return server

def bleach_html(html):
    allowed_tags = ['p','span','a','img','strong','em','table',
        'tr','td','tbody','thead','th', 'h1','h2']
    allowed_attrs = {
        '*': ['style'],
        'a': ['href', 'title'],
        'img': ['src','alt','width','height'],
    }
    css_sanitizer = CSSSanitizer(allowed_css_properties=["color", "font-weight"])
    cleaned= clean(html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True,
        css_sanitizer=css_sanitizer)
    
    return cleaned

def build_msg(data):
    # TODO make look... not like this
    date = datetime.datetime.now()
    year_date = date.strftime("%Y-%j")

    # TODO dates seem to come before or after text?
    # gets 5 at most days
    on_this_day_data = ""
    for i in range(min(5, len(data['onthisday']))):
        event_year = str(data['onthisday'][i]['year']).zfill(4)
        event_date = datetime.datetime.strptime(event_year, "%Y").strftime("%Y")
        
        # use br.join to seperate each entry with a newline (but in html)
        on_this_day_data += "<br>" + "<br>".join({
            event_date,
            bleach_html(data['onthisday'][i]['text'])
            # TODO get links for each article included as a result
        })

    # TODO order halfway backwards? maybe MIME handles odd later down function
    tfa_data = "<br>".join({
        bleach_html(data['tfa']['titles']['display']),
        bleach_html(data['tfa']['content_urls']['desktop']['page']),
        bleach_html(data['tfa']['extract_html'])
    })

    msg = MIMEMultipart()
    msg['Subject'] = "Auto Wikipedia Bot " + year_date
    
    msg.attach(MIMEText("<h2>Featured Article</h2>", "html"))
    msg.attach(MIMEText(tfa_data, "html"))

    msg.attach(MIMEText("<h2>On This Day</h2>", "html"))
    msg.attach(MIMEText(on_this_day_data, "html"))

    return msg

def get_wiki_data():
    date = datetime.datetime.now()
    year, month, day = date.strftime('%Y'), date.strftime('%m'), date.strftime('%d')
    base_url = 'https://api.wikimedia.org/feed/v1/wikipedia/en/'

    featured_url = base_url + 'featured/' + f"{year}/{month}/{day}"
    onthisday_url = base_url + 'onthisday/events/' + f"{month}/{day}"
    # TODO news is stored under featured, seperate from tfa
    # TODO mostread also under featured
    # TODO work on daily image and article thumbnails too
    # TODO according to wikipedias terms article text should always be accompanied by link... so do that
    
    headers = {
    'Authorization': 'Bearer ' + os.getenv("WIKI_ACCESS_TOKEN"),
    'User-Agent': f'AUTO-WIKI-BOT ({os.getenv("CONTACT_EMAIL")})'
    }

    featured_response = requests.get(featured_url, headers=headers).json()
    on_this_day_response = requests.get(onthisday_url, headers=headers).json()

    return {**featured_response, **on_this_day_response}

if __name__ == "__main__":
    load_dotenv() 
    from_email = (os.getenv("EMAIL_ADDRESS"))
    password = (os.getenv("EMAIL_PASSWORD"))
    target_email = os.getenv("TARGET_ADDRESS")

    data = get_wiki_data()
    msg = build_msg(data)

    server = log_into_email(from_email, password)
    server.sendmail(from_email, target_email, msg.as_string())
    server.quit()
