from dotenv import load_dotenv
load_dotenv(override=True)
from pathlib import Path
import os

print(os.getenv("APP_HOME"))
print(Path(Path(__file__).parent.parent, os.getenv("APP_HOME")))