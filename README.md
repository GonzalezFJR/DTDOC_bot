# DTDOC_bot
Telegram bot to help DT DOC shifters

### Packages

You need to install the following executable (can be installed using `conda install -c conda-forge`)

    tesseract-orc

To run the telegram bot server you need the following python packages, that can be installed with pip:

    python-opencv
    pytesseract
    telepot

### Run the code

Modify the `run.py` script to instroduce the correct ID of the telegram bot. Ask Xuan if you don't know the ID.

Run the bot with:

    python run.py

### Configure Telegram

Just open the telegram app, search for the bot called `DTDOC_bot` and start the bot. Write `add me` in order to star receiving notifications.

### Check slice test links

In order to let the bot automatically check the slice test links, you need to drop the output file into a local .txt file (by default `log.txt`). In order to do that, start a ssh sesstion with

    ssh user@lxplus.cern.ch | tee log.txt

and follow all the instructions until running the `tail -f` command. Use a `screen` session to keep it running. 
