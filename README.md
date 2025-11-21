AI Assistant + Terminal:
A Python project with a PyQt5 GUI that combines an AI assistant (powered by OpenAI) and a terminal emulator.
----------------------------------------------------------------------------------------------
shellos/
├── main.py
├── .env
├── core/
│   ├── shell.py
│   ├── parser.py
│   └── commands.py
├── filesystem/
│   ├── fs.py
│   └── storage.py
├── scheduler/
│   ├── task_manager.py
│   └── jobs.py
├── memory/
│   ├── context.py
│   └── session.py
├── ai/
│   ├── assistant.py
│   └── chat_engine.py   
├── utils/
│   ├── config.py
│   ├── helpers.py
│   └── error_handling.py
├── logs/
│   ├── app.log
│   └── shell.log        
└── tests/
    ├── test_shell.py
    ├── test_fs.py
    ├── test_scheduler.py 

---------------------------------------------------------------------------------------------
Installation:
git clone https://github.com/MennaXI/Chatbot-Shell-OS
cd chatbot_project
-----------------------------------------------------------------------------------------------
Create a virtual environment:
python -m venv venv
-----------------------------------------------------------------------------------------------
Activate the environment in ubuntu:
source venv/bin/activate
-----------------------------------------------------------------------------------------------
Running the Project:
python main.py
------------------------------------------------
Notes:
each user should create their own virtual environment.
Handle terminal commands carefully, avoid destructive commands unless necessary.
The .env file is sensitive; keep your API key secret.
----------------------
