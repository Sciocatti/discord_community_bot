# discord_community_bot
A Discord bot made to enhance remote working in small ways.

## Getting started ( as of 2022/03/27 )
1. Clone this repo and cd into it.
2. Install a virtual environment
```bash
# Create virtual environment
python3 -m venv venv
# Activate virtual environment (Ubuntu)
source venv/bin/activate
```
3. Install the needed requirements
```bash
# ! Make sure you are inside the venv.
pip install -r requirements.txt
```
4. Create and link the bot to your server, following [this link](https://realpython.com/how-to-make-a-discord-bot-python/). It is a bit dated, so the code may be different, but the Discord part is solid.
5. Create a file `secret.env` in the root directory of this repo. It must have the following shape, but substitute your own values.
```
DISCORD_TOKEN={{replace this with your token}}
```
6. Run the entrypoint
```bash
venv/bin/python3 main.py
```

> You can find the output in the file `output.log`.

## Contributing
1. Pull the latest main code
```bash
git checkout master
git pull
```
2. Create a dev branch with a suitable name
```bash
git checkout -b feature/increased_joke_json_jokes
```
3. Make changes, commit them and push them. MAKE SURE NOT TO COMMIT SECRETS!
```bash
git add .
git commit -m "Added 20 new jokes"
git push
```
4. Create a PR and wait for the maintainer to merge it in/give feedback.

> This code can run for multiple servers. Please do not break it for others to better your own :)