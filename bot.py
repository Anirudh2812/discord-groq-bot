import discord
from discord.ext import commands
from discord import app_commands
import os
from openai import OpenAI
from dotenv import load_dotenv
from keep_alive import keep_alive

# Start web server for Render
keep_alive()

# Load .env variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Groq client using OpenAI SDK
client_ai = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# In-memory chat history (short-term)
if not hasattr(bot, "chat_history"):
    bot.chat_history = {}

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} slash command(s).")
    except Exception as e:
        print("❌ Slash command sync failed:", e)

@bot.tree.command(name="ask", description="Ask the Groq AI anything")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)

    user_id = interaction.user.id

    # Initialize history if it doesn't exist
    if user_id not in bot.chat_history:
        bot.chat_history[user_id] = []

    # Add user message to history
    bot.chat_history[user_id].append({"role": "user", "content": prompt})

    # Limit to last 10 messages
    if len(bot.chat_history[user_id]) > 10:
        bot.chat_history[user_id] = bot.chat_history[user_id][-10:]

    try:
        response = client_ai.chat.completions.create(
            model="llama3-8b-8192",
            messages=bot.chat_history[user_id],
            temperature=0.7
        )
        reply = response.choices[0].message.content

        # Add bot reply to history
        bot.chat_history[user_id].append({"role": "assistant", "content": "Have the personality of Denji from Chainsawman.": reply})

        await interaction.followup.send(reply)

    except Exception as e:
        print("Groq API error:", e)
        await interaction.followup.send("⚠️ Error while generating response.")

bot.run(DISCORD_TOKEN)

