\# Telegram Asset Price Bot



A production-ready Telegram bot built with Python that retrieves cryptocurrency and precious-metal prices from external APIs and publishes formatted price reports in Telegram.



The bot supports manual commands in private chats and channels, as well as automatic daily price updates using a scheduler.



\## Features



\- Retrieve Bitcoin, Ethereum and Tether prices

\- Retrieve gold and silver prices

\- `/start` command in private chat

\- `/prices` command in private chat

\- `/prices` command inside a Telegram channel

\- Automatic daily price publication

\- Configurable timezone and posting time

\- HTML-formatted Telegram messages

\- Async API requests and Telegram handlers

\- API and publishing error handling

\- Automated tests with Pytest

\- Code quality checks with Ruff

\- Docker and Docker Compose support



\## Supported Assets



| Asset | Symbol | Data Source |

|---|---:|---|

| Bitcoin | BTC | CoinGecko |

| Ethereum | ETH | CoinGecko |

| Tether | USDT | CoinGecko |

| Gold | XAU | MetalpriceAPI |

| Silver | XAG | MetalpriceAPI |



\## Technologies



\- Python 3.12

\- python-telegram-bot

\- Async/Await

\- CoinGecko API

\- MetalpriceAPI

\- Pytest

\- pytest-asyncio

\- Ruff

\- Docker

\- Docker Compose

\- Git and GitHub



\## Project Structure



```text

telegram-asset-price-bot/

├── bot/

│   ├── \_\_init\_\_.py

│   ├── config.py

│   ├── main.py

│   ├── message\_formatter.py

│   ├── price\_service.py

│   └── scheduler.py

├── tests/

│   ├── \_\_init\_\_.py

│   ├── test\_main.py

│   ├── test\_message\_formatter.py

│   ├── test\_price\_service.py

│   └── test\_scheduler.py

├── .dockerignore

├── .env

├── .env.example

├── .gitignore

├── Dockerfile

├── docker-compose.yml

├── README.md

└── requirements.txt

```



\## Environment Variables



Create a `.env` file in the project root:



```dotenv

TELEGRAM\_BOT\_TOKEN=your\_telegram\_bot\_token

TELEGRAM\_CHANNEL\_ID=@your\_channel\_username



COINGECKO\_API\_KEY=your\_coingecko\_api\_key

METALPRICE\_API\_KEY=your\_metalprice\_api\_key



TIMEZONE=Asia/Tehran

DAILY\_POST\_TIME=09:00

REQUEST\_TIMEOUT=15

```



\### Variable Description



| Variable | Description |

|---|---|

| `TELEGRAM\_BOT\_TOKEN` | Token received from Telegram BotFather |

| `TELEGRAM\_CHANNEL\_ID` | Channel username or Telegram channel ID |

| `COINGECKO\_API\_KEY` | CoinGecko Demo API key |

| `METALPRICE\_API\_KEY` | MetalpriceAPI key |

| `TIMEZONE` | Timezone used by the scheduler |

| `DAILY\_POST\_TIME` | Daily publication time in `HH:MM` format |

| `REQUEST\_TIMEOUT` | API request timeout in seconds |



> Never commit your real `.env` file, Telegram token or API keys to GitHub.



\## Local Installation



Clone the repository:



```bash

git clone https://github.com/milad5108/telegram-asset-price-bot.git

cd telegram-asset-price-bot

```



Create a virtual environment:



\### Windows PowerShell



```powershell

python -m venv .venv

.venv\\Scripts\\Activate.ps1

```



\### Linux or macOS



```bash

python3 -m venv .venv

source .venv/bin/activate

```



Install the dependencies:



```bash

pip install -r requirements.txt

```



Create the environment file:



\### Windows PowerShell



```powershell

Copy-Item .env.example .env

```



\### Linux or macOS



```bash

cp .env.example .env

```



Add your Telegram and API credentials to `.env`.



\## Run Locally



```bash

python -m bot.main

```



After startup, test these commands:



```text

/start

/prices

```



\## Run with Docker



Build the Docker image:



```bash

docker build -t telegram-asset-price-bot:latest .

```



Run the container in foreground mode:



```bash

docker run --rm \\

&#x20; --name telegram-asset-price-bot \\

&#x20; --env-file .env \\

&#x20; telegram-asset-price-bot:latest

```



Run the container in detached mode:



```bash

docker run -d \\

&#x20; --name telegram-asset-price-bot \\

&#x20; --env-file .env \\

&#x20; --restart unless-stopped \\

&#x20; telegram-asset-price-bot:latest

```



View container logs:



```bash

docker logs -f telegram-asset-price-bot

```



Stop and remove the detached container:



```bash

docker stop telegram-asset-price-bot

docker rm telegram-asset-price-bot

```



\## Run with Docker Compose



Build and run in foreground mode:



```bash

docker compose up --build

```



Run in detached mode:



```bash

docker compose up -d --build

```



Check the service status:



```bash

docker compose ps

```



View logs:



```bash

docker compose logs -f

```



Stop and remove the Compose services:



```bash

docker compose down

```



\## Tests



Run all automated tests:



```bash

pytest

```



The project currently includes tests for:



\- Telegram command handlers

\- Price service

\- Message formatting

\- Scheduler behavior



\## Code Quality



Check the project with Ruff:



```bash

ruff check .

```



Check that Python files compile correctly:



```bash

python -m compileall bot tests

```



Run all project checks:



```bash

python -m compileall bot tests

ruff check .

pytest

```



\## Scheduler



The bot uses a configurable daily scheduler.



Example configuration:



```dotenv

TIMEZONE=Asia/Tehran

DAILY\_POST\_TIME=09:00

```



With this configuration, the bot publishes a new price report every day at `09:00` using the `Asia/Tehran` timezone.



\## Telegram Setup



1\. Create a Telegram bot using BotFather.

2\. Copy the bot token into `TELEGRAM\_BOT\_TOKEN`.

3\. Add the bot to your Telegram channel.

4\. Promote the bot to administrator.

5\. Give it permission to post messages.

6\. Set the channel username or ID in `TELEGRAM\_CHANNEL\_ID`.



\## Security



The following files and values must never be committed:



\- `.env`

\- Telegram bot token

\- CoinGecko API key

\- MetalpriceAPI key

\- URLs containing secret tokens

\- Logs containing sensitive data

\- Virtual environment files

\- Python cache files



Before pushing changes, verify that `.env` is ignored:



```bash

git check-ignore -v .env

```



You can also inspect tracked files:



```bash

git ls-files

```



\## Roadmap



\- \[x] Telegram bot commands

\- \[x] Cryptocurrency price retrieval

\- \[x] Gold and silver price retrieval

\- \[x] Channel command support

\- \[x] Daily scheduler

\- \[x] Automated tests

\- \[x] Ruff code-quality checks

\- \[x] Docker support

\- \[x] Docker Compose support

\- \[ ] GitHub Actions CI

\- \[ ] CI status badge

\- \[ ] Screenshots and demo

\- \[ ] Version `v1.0.0` release

\- \[ ] Ubuntu deployment documentation



\## Author



Developed by \[milad5108](https://github.com/milad5108)



\## License



This project is intended for educational and portfolio purposes.



A formal open-source license can be added in a future release.