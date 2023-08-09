# Discord Manga Update Bot

This is a Discord bot that keeps track of the latest chapter releases for your favorite manga. The bot will automatically scrape updates from fanfox.net and send you a notification message on Discord whenever a new chapter is released for any manga in your reading list.

## Features
- Add and manage a reading list of manga titles
- Receive updates when new chapters are released for manga on your reading list
- Remove manga titles from your reading list
- Delete your entire reading list

## Setup
### Prerequisites
- Python 3.7 or higher
- MongoDB account
- Discord account
- fanfox.net account (optional)

### Installation
1. Clone this repository to your local machine
2. Install the required dependencies by running `pip install -r requirements.txt`
3. Create a `.env` file in the root directory of the project with the following variables:
```
DISCORD_TOKEN = your_discord_bot_token_here
CONNECTION_URL = your_mongodb_connection_url_here
```
4. Run `python main.py` to start the bot

## Usage
Once the bot is up and running, you can interact with it using the following commands:

- `?list`: displays your current reading list
- `?list_add <manga_title1>/<manga_title2>/...`: adds one or more manga titles to your reading list
- `?list_remove <manga_title1>/<manga_title2>/...`: removes one or more manga titles from your reading list
- `?delete_list`: deletes your entire reading list
- `?updates`: checks for new chapter updates for manga on your reading list
  
## Contributing
Contributions to this project are welcome! Feel free to submit bug reports, feature requests, or pull requests on GitHub.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
