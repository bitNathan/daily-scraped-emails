# Daily Wikipedia Scraper
_Automated daily email with Wikipedia's trending articles, news, and this day in history_

## Getting Started

### Prerequisites
- Python 3.8+ 
- A Gmail account ( or other SMTP-compatible email service )
- An email account to receive the digest
- Wikipedia API access token ( wikipedia gives [very easy instructions](https://api.wikimedia.org/wiki/Getting_started_with_Wikimedia_APIs) on how to make a personal key )

### Automate with Cloud Services

_TODO: In progress but once something works I'll put a bit about setup_

### Running Locally

_TODO: Once packaging reaches an alright state I'll have download and setup for that_

#### Installation through Git
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd daily-wikipedia-scraper
   ```

2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root:
   ```env
   SENDER_EMAIL=your-sender@gmail.com
   SENDER_PASSWORD=your-app-password
   RECEIVER_EMAIL=your-receiver@example.com
   WIKI_ACCESS_TOKEN = your-access-token
   ```

#### Usage
_TODO: local automation_

Run the script manually:
```bash
python send.py
```

## Security
No credentials are stored in the codebase, everything is set by the user in the .env file.

**Email Setup Requirements:**
- Use a dedicated Gmail account for sending (not your main account)
- Enable 2-factor authentication and generate an App Password

> **Security Note**  
> Currently the sender email is accessed using an App Password, which is less secure than your standard authentication methods. (This why I recommend you make a seperate email account to send everything from, you can recieve to your standard email alright.) This project won't by fully deployable until Oauth authentication support is added.

## Roadmap

| Status | Feature                    
|--------|-------------------
| ✅    | Initial Wikipedia parsing               
|  X    | Automation with lambda or cron ( auto update via Github Actions )               
|  X    | Pretty emails                           
|  X    | Package into an exe    
|  X    | Expand to other APIs and scraping                
|  X    | Allow users to customize their email in env settings

## Contributing
This is a hobby project, but feel free to:
- Fork to your heart's content
- Submit a PR
- Report any bugs with an issue

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Future Ideas
_These are more or less ranked by how interested I am in completing them but more ideas never hurt_

- scrape other free news sources
- Word clouds from trending articles and news sources
    - Could go very in depth with nlp analysis
- Daily writing prompts
    - Actually, prompts for dnd one shots/dungeons would be really up my alley
- Weather data (likely using location data input into env files)
- Summaries/status of your inbox (would require authentication into main account, requiring oauth2)
- NASA APOD images
- Puzzle games (Wordle, etc.)
