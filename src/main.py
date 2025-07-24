import smtplib 
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from bleach import clean
from bleach.css_sanitizer import CSSSanitizer
from dotenv import load_dotenv
import xkcd_scrape as xkcd

# TODO break all this into seperate files and reorganize wikipedia data extraction
# TODO add card formatting so different sources appear on different cards

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
        'tr','td','tbody','thead','th', 'h1','h2','h3','div','br','small']
    allowed_attrs = {
        '*': ['style'],
        'a': ['href', 'title'],
        'img': ['src','alt','width','height'],
        'div': ['style'],
    }
    css_sanitizer = CSSSanitizer(allowed_css_properties=["color", "font-weight", "margin-left", "margin-top", "margin-bottom", "text-align", "font-style", "font-size"])
    cleaned= clean(html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True,
        css_sanitizer=css_sanitizer)
    
    return cleaned

def get_on_this_day_data(data):
    # gets 5 at most events
    # TODO replace "3" with env const global (and other occourances)
    on_this_day_html = ""
    for i in range(min(3, len(data['onthisday']))):
        event_year = str(data['onthisday'][i]['year']).zfill(4)
        
        # Main event description
        event_text = bleach_html(data['onthisday'][i]['text'])
        
        # get links and display title for supporting articles
        related_articles = data['onthisday'][i]['pages']
        articles_html = ""
        for article in related_articles:
            article_title = bleach_html(article['titles']['display'])
            article_url = article['content_urls']['desktop']['page']
            article_extract = bleach_html(article['extract_html'])
            
            articles_html += f"""
                <div style="margin-left: 20px; margin-top: 10px;">
                    <strong><a href="{article_url}">{article_title}</a></strong><br>
                    {article_extract}
                </div>
            """

        # Format each event with proper structure
        on_this_day_html += f"""
            <div style="margin-bottom: 20px;">
                <strong>{event_year}:</strong> {event_text}
                {articles_html}
            </div>
        """

    return on_this_day_html

def get_tfa_data(data):
    title = bleach_html(data['tfa']['titles']['display'])
    url = data['tfa']['content_urls']['desktop']['page']
    extract = bleach_html(data['tfa']['extract_html'])
    
    tfa_html = f"""
        <div>
            <strong><a href="{url}">{title}</a></strong><br>
            {extract}
        </div>
    """
    return tfa_html

def get_mostread_data(data):
    # sort articles by rank to ensure proper ordering
    articles = sorted(
        data['mostread']['articles'],
        key=lambda x: x.get('rank', float('inf'))
    )
    
    mostread_html = ""
    for i, article in enumerate(articles[:3]):
        title = bleach_html(article['titles']['display'])
        url = article['content_urls']['desktop']['page']
        extract = bleach_html(article['extract_html'])
        
        mostread_html += f"""
            <div style="margin-bottom: 15px;">
                <strong>{i + 1}. <a href="{url}">{title}</a></strong><br>
                {extract}
            </div>
        """
    
    return mostread_html

def get_image_data(data):
    thumbnail_url = data['image']['thumbnail']['source']
    description_html = data['image']['description']['html']
    artist_name = data['image']['artist']['text']
    attribution_url = data['image']['file_page']
    license_name = data['image']['license']['type']
    license_url = data['image']['license']['url']
    
    # Format the image with alt text and description (no alt text because description included regardless)
    # TODO image style data style="max-width:100%;height:auto;margin-bottom:10px;
    image_html = f'''
        <div>
            <img src="{thumbnail_url}"><br><br>
            <div style="font-style: italic; margin-bottom: 10px;">{bleach_html(description_html)}</div>
        </div>
    '''

    # Format the credit info
    credit_html = f'''
        <div style="font-size: smaller; color: #666;">
            Image by {bleach_html(artist_name)} 
            (<a href="{attribution_url}">source</a>), 
            licensed under <a href="{license_url}">{license_name}</a>
        </div>
    '''

    return image_html, credit_html

def build_msg(data, xkcd_data):
    date = datetime.datetime.now()
    year_date = date.strftime("%Y-%j")

    # extract/format data from "data"
    image_data, image_credit_data = get_image_data(data)
    tfa_data = get_tfa_data(data)
    on_this_day_data = get_on_this_day_data(data)
    most_read_data = get_mostread_data(data)
    xkcd_image, xkcd_title = xkcd.format_xkcd_data(xkcd_data)
    # TODO read from env css file and apply to here
    # Build email
    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
                h1 {{ color: #0645ad; border-bottom: 2px solid #0645ad; }}
                h2 {{ color: #0645ad; margin-top: 30px; }}
                a {{ color: #0645ad; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                .section {{ margin-bottom: 30px; }}
                .image-section {{ text-align: center; margin-bottom: 30px; }}
            </style>
        </head>
        <body>
            <h1>Daily Digest - {year_date}</h1>
            
            <h2>XKCD comic: {xkcd_title}</h2>
            <div class="image-section section">
                {xkcd_image}
            </div>
            
            <h2>Wikipedia Data</h2>
            <h3>Picture of the Day</h3>
            <div class="image-section section">
                {image_data}
                {image_credit_data}
            </div>

            <div class="section">\
                <h3>Most Read Articles</h3>
                {most_read_data}
            </div>
            
            <div class="section">
                <h3>Featured Article</h3>
                {tfa_data}
            </div>

            <div class="section">
                <h3>On This Day</h3>
                {on_this_day_data}
            </div>

            
        </body>
    </html>
    """

    # build message as a single HTML email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Daily Wikipedia Digest " + year_date
    
    # Attach the HTML content
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    return msg

def get_wiki_data():
    date = datetime.datetime.now()
    year, month, day = date.strftime('%Y'), date.strftime('%m'), date.strftime('%d')
    base_url = 'https://api.wikimedia.org/feed/v1/wikipedia/en/'

    featured_url = base_url + 'featured/' + f"{year}/{month}/{day}"
    onthisday_url = base_url + 'onthisday/events/' + f"{month}/{day}"
    
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
    xkcd_data = xkcd.get_xkcd_data()
    msg = build_msg(data, xkcd_data)

    server = log_into_email(from_email, password)
    server.sendmail(from_email, target_email, msg.as_string())
    server.quit()
