import os
from pathlib import Path

from kutana import Kutana, load_plugins
from kutana.backends import Telegram
import dotenv

env = dotenv.dotenv_values() if Path(".env").exists() else os.environ

# Create application
app = Kutana()

# Add manager to application
app.add_backend(Telegram(env.get("TELEGRAM_TOKEN"), proxy=env.get("PROXY")))

# Load and register plugins
app.add_plugins(load_plugins("plugins/"))

if __name__ == "__main__":
    # Run application
    app.run()
