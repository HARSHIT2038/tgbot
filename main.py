import json
import urllib.request
import os
import telegram

# Define a function to process the JSON data
def process_data(data):
    dead_urls = []
    small_files = []
    for item in data:
        url = item["url"]
        try:
            # Open the URL and retrieve the metadata
            with urllib.request.urlopen(url) as response:
                metadata = response.info()
                filesize = int(metadata.get("Content-Length"))
                if filesize < 50000000:
                    # Add the URL to the list of small files
                    filename = os.path.basename(url)
                    small_files.append(f"{filename} ({filesize} bytes)")
        except Exception as e:
            # Handle any errors that occur while opening the URL
            message = f"Error while processing URL {url}: {e}"
            dead_urls.append(url)

    # Send a Telegram message with the list of small files
    if len(small_files) > 0:
        message = "The following files are less than 50 MB in size:\n\n"
        message += "\n".join(small_files)
        bot.send_message(chat_id=chat_id, text=message)

    # Send a "dead" message for any URLs that could not be opened
    if len(dead_urls) > 0:
        message = "The following URLs could not be opened:\n\n"
        message += "\n".join(dead_urls)
        bot.send_message(chat_id=chat_id, text=message)

# Connect to the Telegram bot
bot = telegram.Bot(token="1539441986:AAGRX7gKpccRlpEYAgoxF043czJSoU8WJdw")
chat_id = "1177047392"

# Define a function to handle the /chk command
def chk_command(update, context):
    # Get the message and reply to it
    message = update.message.reply_to_message
    if not message:
        bot.send_message(chat_id=chat_id, text="Please reply to a message containing a JSON file.")
        return
    # Retrieve the uploaded JSON file
    file = message.document.file_id
    filename = message.document.file_name
    file = bot.get_file(file)

    # Download the file and load the data
    file.download(filename)
    with open(filename, "r") as infile:
        data = json.load(infile)

    # Process the data
    process_data(data)

    # Delete the downloaded file
    os.remove(filename)

# Add a handler for the /chk command
updater = telegram.ext.Updater("your_bot_token")
updater.dispatcher.add_handler(telegram.ext.CommandHandler("chk", chk_command))

# Start the bot
updater.start_polling()
