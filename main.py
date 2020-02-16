from kutana import Kutana, load_plugins
from kutana.backends import Telegram
import dotenv

env = dotenv.dotenv_values()

# Create application
app = Kutana()

# Add manager to application
app.add_backend(Telegram(env["TELEGRAM_TOKEN"], proxy="http://127.0.0.1:8118"))

# Load and register plugins
app.add_plugins(load_plugins("plugins/"))

if __name__ == "__main__":
    # Run application
    app.run()
