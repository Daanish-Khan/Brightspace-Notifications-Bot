import discord

class helper:

    def __init__(self):
        self.message = []
        self.timeout_flag = False

    def get_message(self):
        return self.message

    def get_timeout_flag(self):
        return self.timeout_flag

    def set_timeout_flag(self, flag):
        self.timeout_flag = flag

    def embed_builder(self, key, desc, body, time):

        if "announcements" in desc.lower():
            type = "Announcement"
            title = "\N{CHEERING MEGAPHONE} Announcement for " + key + " \N{CHEERING MEGAPHONE}"
            color = discord.Color.teal()
        elif "assignments" in desc.lower():
            type = "Assignment"
            title = "\N{ALARM CLOCK} Assignment is due soon for " + key + " \N{ALARM CLOCK}"
            color = discord.Color.red()
        elif "quizzes" in desc.lower():
            type = "Quiz"
            title = "\N{ALARM CLOCK} Quiz is due soon for " + key + " \N{ALARM CLOCK}"
            color = discord.Color.orange()

        embed = discord.Embed(title=title, type="rich", color=color)

        embed.add_field(name=desc, value=body, inline=False)
        embed.set_author(name=key)
        embed.set_footer(text="Notification received at " + time)

        return embed
