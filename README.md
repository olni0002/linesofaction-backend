# Lines of Action

## Required software
- [Python](https://www.python.org/downloads/) version 3.6 or newer
- [Git](https://git-scm.com/) only for cloning the repo

## Running
Clone this repository and enter the directory
```bash
git clone https://github.com/olni0002/linesofaction-backend.git
cd linesofaction-backend/
```
Create a virtual environment and activate it
```bash
python3 -m venv .venv

# Unix-like bash/zsh
source .venv/bin/active

# Windows command prompt
.venv\Scripts\activate.bat
# Windows powershell
.venv\Scripts\activate.ps1
```
Install project dependencies in the virtual environment
```bash
pip install -r requirements.txt
```
Run the provided python file directly
```bash
python3 linesofaction.py
```
or run the application as a module
```bash
python3 -m linesofaction
```

You have now successfully started the server and need to run the frontend to play the game
```bash
git clone https://github.com/bigcheesespaghett/LinesOfAction.git
```
Setup instructions are found in the projects README
