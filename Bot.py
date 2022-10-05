import nextcord
from nextcord.ext import commands
import dotenv
import os
from extensions.pm2_list import pm2list
from extensions.pm2_logs import pm2logger


dotenv.load_dotenv()
TESTING_GUILD_ID = os.environ['TESTING_GUILD_ID']  # Replace with your guild ID

bot = commands.Bot()
options = {}
with open("programs.txt") as f:
    lines = f.read().splitlines()

for line in lines:
    options[line.replace('_', ' ')] = line
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(description="Clear Messages", guild_ids=[TESTING_GUILD_ID])
async def clear(interaction: nextcord.Interaction):
    await interaction.channel.purge()



@bot.slash_command(description="PM2 List", guild_ids=[TESTING_GUILD_ID])
async def pm2ls(interaction: nextcord.Interaction):
    await interaction.send("*************Printing Process Info*************")
    for items in pm2list():
        pid, name, restarts, status, cpu, memory, time_obj, pmid = items
        embed = nextcord.Embed(title=name, description=f"PM2 Process ID: {pmid}", color=0x00000)
        embed.add_field(name="pid", value=pid, inline=False)
        embed.add_field(name="Restarts", value=restarts, inline=False)
        embed.add_field(name="Status", value=status, inline=False)
        embed.add_field(name="Cpu", value=cpu, inline=False)
        embed.add_field(name="Memory", value=memory, inline=False)
        embed.add_field(name="Time Started", value=time_obj, inline=False)
        embed.set_footer(text=f"Requested by {str(interaction.user)}")
        await interaction.send(embed=embed)


@bot.slash_command(description="PM2 Logs", guild_ids=[TESTING_GUILD_ID])
async def pm2logs(
    interaction: nextcord.Interaction,
    process: str = nextcord.SlashOption(
        name="process",
        choices=options,
    ),
):
    logs = pm2logger(process)
    await interaction.response.send_message(f"```{logs}```")


dotenv.load_dotenv()

bot.run(os.environ['BOT_TOKEN'])
