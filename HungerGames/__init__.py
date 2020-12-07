from .hungrybot import HungryBot

def setup(bot):
    bot.add_cog(HungryBot(bot))