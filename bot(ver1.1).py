import discord
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Create OpenAI client (Groq-compatible)
client_ai = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🤖 Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!ask"):
        prompt = message.content[5:].strip()

        if not prompt:
            await message.channel.send("📝 Please enter a prompt after `!ask`")
            return

        try:
            response = client_ai.chat.completions.create(
                model="mixtral-8x7b-32768",
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

client.run(DISCORD_TOKEN)

