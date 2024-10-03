# About the project
This basic agent, powered by OpenAI's GPT-4o model, is designed to assist with installation and debugging tasks on Linux machines by executing bash commands directly. USE AT YOUR OWN RISK, this program essentially has free reign over your linux machine, this is obviously a huge security risk and I heavily recommend making backups of your system on a separate device.

## Prerequisites

- Linux (Only tested on Debian 12)
- Python 3.8+
- OpenAI API Key

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/liammcmillen/gpt-4o-agent.git
   cd gpt-4o-agent
   ```

2. **Set up a virtual environment (optional):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install the dependencies:**

   ```bash
   pip3 install -r requirements.txt
   ```
4. **Configure the API Key:**

   Add your OpenAI API key as an environment variable by appending it to your `.bashrc` or `.zshrc` file:

   ```bash
   echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
   source ~/.bashrc

   # Or for Zsh users:
   echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```
5. **Run the Agent:**

   ```bash
   python3 gpt4oagent.py
   ```
## Usage

Once the agent is running, it will listen for input and respond accordingly including executing commands on your Linux machine. Examples of usage include installing packages, debugging system issues, and more.

Example usages:

![image](https://github.com/user-attachments/assets/7dca173e-2287-4e66-8d0b-d093f14dd486)

![image](https://github.com/user-attachments/assets/aa18dbfc-e7ca-42a1-b23d-e704540113d6)

![image](https://github.com/user-attachments/assets/51096386-1383-4725-b970-ec490664254e)

## License

This project is licensed under the GNU General Public License - see the `LICENSE` file for details.
