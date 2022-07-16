import cordium


class Bot(cordium.Bot):
    # token = "TOKEN" # token can also be passed here

    async def on_ready(self):
        print("Connected to the gateway.")


bot = Bot()  # intents are all off by default
bot.start("TOKEN")
