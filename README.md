# About the project
This basic agent, powered by OpenAI's GPT-4o model, is designed to assist with installation and debugging tasks on Linux machines by executing bash commands directly. USE AT YOUR OWN RISK, this program essentially has free reign over your linux machine, this is obviously a huge security risk and I heavily recommend making backups of your system on a separate device and/or first experimenting with it on a VM

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
   streamlit run gpt4oagent.py
   ```
## Usage

Once the agent is running, it will listen for commands and execute them on your Linux machine. Examples of usage include installing packages, debugging system issues, and more.

Example usages:

![image](https://github.com/user-attachments/assets/1252755a-944f-40ba-9983-90412cbc9a16)

![image](https://github.com/user-attachments/assets/d4949990-9f6c-4519-a4a5-e023d802e806)

![image](https://github.com/user-attachments/assets/8e42cd8c-4f14-4652-a1fd-6a25fe910361)

![image](https://github.com/user-attachments/assets/16fcde7b-89dc-435d-b9ab-d0e5c24c7572)

## License

This project is licensed under the GNU General Public License - see the `LICENSE` file for details.
