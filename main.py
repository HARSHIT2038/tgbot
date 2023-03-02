import json

import urllib.request

import os

import telegram

# Define a function to process the JSON data

def process_data(data):

    messages = []

    for item in data:

        url = item["url"]

        try:

            # Open the URL and retrieve the metadata

            with urllib.request.urlopen(url) as response:

                metadata = response.info()

                filename = os.path.basename(url)

                filesize = int(metadata.get("Content-Length"))

                

                if filesize <= 50*1024*1024:

                    # Send a Telegram message with the metadata

                    message = f"File {filename} with size {filesize} bytes found at {url}."

                    messages.append(message)

                

                else:

                    # Send a "dead" message if the file is too large

                    message = f"File {filename} with size {filesize} bytes at {url} is too large."

                    messages.append(message)

                    

        except Exception as e:

            # Handle any errors that occur while opening the URL

            message = f"Error while processing URL {url}: {e}"

            messages.append(message)

    # Send a list of all messages

    message = "\n".join(messages)

    bot.send_message(chat_id=chat_id, text=message)

# Define a function to handle the /chk command

def chk_command(update, context):

    # Check if the message is a reply to a file

    if update.message.reply_to_message and update.message.reply_to_message.document:

        # Retrieve the uploaded JSON file

        file_id = update.message.reply_to_message.document.file_id

        file = bot.get_file(file_id)

        # Download the file and load the data

        filename = file.file_path.split("/")[-1]

        file.download(filename)

        with open(filename, "r") as infile:

            data = json.load(infile)

        # Process the data

        process_data(data)

        # Delete the downloaded file

        os.remove(filename)

    else:

        # Send an error message if the user did not reply to a file

        message = "Please reply to a JSON file to check its data."

        bot.send_message(chat_id=update.message.chat_id, text=message)

# Connect to the Telegram bot

bot = telegram.Bot(token="5808384079:AAG8mLXrXUO0IXMdVIi6LkqEtxigEUB27Rs")

chat_id = "1177047392"

# Define a handler for the /chk command

chk_handler = telegram.ext.CommandHandler("chk", chk_command)

dispatcher = telegram.ext.Dispatcher(bot, None)

dispatcher.add_handler(chk_handler)

# Start the bot

updater = telegram.ext.Updater(bot=bot, use_context=True)

updater.start_polling()

