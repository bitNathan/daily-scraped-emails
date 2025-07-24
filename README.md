# Daily Wikipedia Scraper
_Automated daily email with Wikipedia's trending articles, news, and this day in history_

## Quick Start

1. **Clone:** `git clone https://github.com/bitNathan/daily-scraped-emails.git`
2. **Setup:** Create virtual environment and install dependencies
3. **Configure:** Copy `.env.example` to `.env` and add your email/API credentials  
4. **Test:** Run `python main.py` to send your first email
5. **Automate:** Set up cron (Linux/Mac)

## Getting Started

### Prerequisites
- Python 3.8+ ([Download here](https://www.python.org/downloads/))
- A Gmail account for sending emails (I recommend creating a dedicated one)
   - Other email providers could work and may be supported later in development.
- An email account to receive the daily digest
- Wikipedia API access token ([Get one free here](https://api.wikimedia.org/wiki/Getting_started_with_Wikimedia_APIs))


## Installation

### Step 1: Clone and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bitNathan/daily-scraped-emails.git
   cd daily-scraped-emails
   ```

2. **Create a virtual environment:**
   
   **On Linux/Mac:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root directory. You can copy the example file and edit it:

```bash
cp .env.example .env
```

Then edit `.env` with your details:

```env
# Email Configuration
SENDER_EMAIL=your-sender@gmail.com
SENDER_PASSWORD=your-gmail-app-password
RECEIVER_EMAIL=your-receiver@example.com

# Wikipedia API
WIKI_ACCESS_TOKEN=your-wikipedia-access-token
```

**How to get your Gmail App Password:**
1. Go to your Google Account settings
2. Enable 2-Factor Authentication if not already enabled
3. Go to Security → 2-Step Verification → App passwords
4. Generate a new app password for "Mail"
5. Use this 16-character password (not your regular Gmail password)

**How to get Wikipedia Access Token:**
1. Visit [Wikimedia API Getting Started](https://api.wikimedia.org/wiki/Getting_started_with_Wikimedia_APIs)
2. Click "Get API access" 
3. Create a personal API key (free, takes 2 minutes)
4. Copy the access token to your `.env` file

### Step 3: Test the Setup

Test that everything works before setting up automation:

```bash
python main.py
```

You should receive an email within a few minutes.

## Automation

### Cron (linux/mac)

1. **Test the shell script:**
   ```bash
   chmod +x send.sh
   ./send.sh /absolute/path/to/your/project
   ```

2. **Set up daily automation:**
   ```bash
   crontab -e
   ```
> TIP
>
> Use the `pwd` command on linux systems to get the absolute path to the current directory

3. **Add this line for daily emails at 5 AM:**
   ```cron
   0 5 * * * </absolute/path/to/your/project>/scripts/send.sh /absolute/path/to/your/project
   ```

   **Other timing examples:**
   - `0 8 * * *` - Daily at 8 AM
   - `0 9 * * 1-5` - Weekdays at 9 AM
   - `0 6 * * 0` - Sundays at 6 AM
   
   Use [crontab.guru](https://crontab.guru/) to customize timing.

### Manual Testing

Run manually anytime:
```bash
# Linux/Mac
./send.sh /absolute/path/to/project
```

## Security
No credentials are stored in the codebase, everything is set by the user in the .env file.

**Email Setup Requirements:**
- Use a dedicated Gmail account for sending (not your main account)
- Enable 2-factor authentication and generate an App Password

> **Security Note**  
> Currently the sender email is accessed using an App Password, which is less secure than your standard authentication methods. (This why I recommend you make a seperate email account to send everything from, you can recieve to your standard email alright.) This project won't by fully deployable until Oauth authentication support is added.

## Project Status

| Status | Feature           
|--------|------------------
|✅| Wikipedia content scraping | Daily trending articles and "On This Day"
|✅| Email automation | Automated sending via cron/Task Scheduler
|✅| Better email formatting with html and css
| | Easy setup and automation (for windows, Mac, or Linux) through documentation and scripts
| | Multiple news sources
| | Customizable content, let users choose what to include, ordering, and css styling
| | Optional OAuth email authentication rather than app passwords

## Contributing
This is a hobby project, but feel free to:
- Fork to your heart's content
- Submit a PR
- Report any bugs with an issue

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Future Ideas
_These are more or less ranked by how interested I am in completing them but more ideas never hurt_

- Word clouds from trending articles and news sources
    - Could go very in depth with nlp analysis
- Daily writing prompts
    - Actually, prompts for dnd one shots/dungeons would be really up my alley
- Weather data (likely using location data input into env files)
- NASA APOD images
- Puzzle games (Wordle, etc.)
