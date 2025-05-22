from os import getenv
from linesofaction.server.app import app

def main():
    try:
        server_port = int(getenv("SERVER_PORT", 5000))
    except ValueError:
        print("SERVER_PORT must be an integer.")
        raise
    else:
        app.run(port=server_port)

if __name__ == "__main__":
    main()
