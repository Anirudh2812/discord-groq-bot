import discord
import os
from openai import OpenAI
from dotenv import load_dotenv
from keep_alive import keep_alive  # ✅ Your Flask web server

# Start fake web server so Render stays happy
keep_alive()  # ✅ Must run before bot.run()

# Load .env vars (if running locally)
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up Groq client
client_ai = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("!ask"):
        prompt = message.content[5:].strip()
        if not prompt:
            await message.channel.send("📝 Please enter a prompt after `!ask`")
            return
        try:
            response = client_ai.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            reply = response.choices[0].message.content
            await message.channel.send(reply)
        except Exception as e:
            print("Error:", e)
            await message.channel.send("⚠️ Sorry, I couldn't process that.")

# ✅ Run the Discord bot
bot.run(DISCORD_TOKEN)

