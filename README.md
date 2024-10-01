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

Once the agent is running, it will listen for commands and execute them on your Linux machine. Examples of usage include installing packages, debugging system issues, and more.

Example usages:

![image](https://github.com/user-attachments/assets/7cb68a2b-65e3-4eff-b449-ce43fd7419cb)

![image](https://github.com/user-attachments/assets/6b31d2bc-3674-48c2-92c4-ce1b5481bab8)

![image](https://github.com/user-attachments/assets/3cd4650a-3ccc-498c-bfd9-d6a05784c599)

## License

This project is licensed under the GNU General Public License - see the `LICENSE` file for details.
