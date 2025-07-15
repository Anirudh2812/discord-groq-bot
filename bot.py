from keep_alive import keep_alive
keep_alive()
import discord
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Fix: Initialize OpenAI client for Groq
client_ai = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# ✅ Discord bot setup
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
            # ✅ Using latest supported Groq model
            response = client_ai.chat.completions.create(
                model="llama3-8b-8192",  # You can try "llama3-70b-8192" too
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            reply = response.choices[0].message.content
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send("⚠️ Error: Could not get a response.")
            print("Groq API error:", e)

# ✅ Start bot
bot.run(DISCORD_TOKEN)

