# TwitchPlaysTomodachiV2

A self-contained python script that send InputRedirection commands to a Nintendo 3DS with Lumas3DS installed.

Build for TwitchPlaysTomodachi, but can be used for any other game and purpose.

Make sure to `pip install` all of the dependencies in `dependencies.txt` and run the script with `python3 tpt.py <ip>`

You'll also need to create a `.env` file with the following variables:

```
TWITCH_CHAT_HOST=irc.chat.twitch.tv
TWITCH_CHAT_PORT=6667
TWITCH_BOT_USERNAME=<twitch bot username>
TWITCH_BOT_OAUTH=<twitch bot oauth token>
TWITCH_CHAT_CHANNEL=<twitch channel username of the chat you want to watch>
DISCORD_WEBHOOK=<discord webhook url>
PRIVATE_WEBHOOK=<discord webhook url>
```

The discord webhooks are used for the `!mods` command and for sending errors (to the private webhook)