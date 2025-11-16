AI Assistant + Terminal:
A Python project with a PyQt5 GUI that combines an AI assistant (powered by OpenAI) and a terminal emulator.
----------------------------------------------------------------------------------------------
my_project/
├── qtpyTerminal.py      # Terminal widget
├── shell.py             # Main AI + Terminal code
├── requirements.txt     # Python dependencies
├── .env                 # Example environment variables (safe to share)
└── README.md            # Project documentation
---------------------------------------------------------------------------------------------
Installation:
git clone https://github.com/MeNna-Say/MyProject.git
cd MyProject
-----------------------------------------------------------------------------------------------
Create a virtual environment:
python -m venv venv
-----------------------------------------------------------------------------------------------
Activate the environment in ubuntu:
source venv/bin/activate
-----------------------------------------------------------------------------------------------
Running the Project:
python shell.py
------------------------------------------------
Notes:
each user should create their own virtual environment.
Handle terminal commands carefully, avoid destructive commands unless necessary.
The .env file is sensitive; keep your API key secret.
----------------------
