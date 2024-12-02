# Nodepay Automate with Proxies | Bypass Version!
## Information: Old version is not working anymore, Please use ``runv2.py`` instead! Multi accounts feature for v2 script is coming soon!
Automate farming Nodepay Network using proxies. ~Please use the bypass version. I found Nodepay's real IP host to make farming easier without being blocked by Cloudflare protection.~ 

Old version is not working anymore, Please use ``runv2.py`` instead!
- ~This bot support multiple accounts. Run ```run-multi-bypass.py```~
- ~Place multiple tokens in ```tokens.txt```~
### Tools and components required
1. Nodepay Account | Register: [https://app.nodepay.ai/register](https://app.nodepay.ai/register?ref=ZUCBuJaIoBXLE6J)
2. Proxies Static Residental | [FREE 10 PREMIUM PROXIES](https://www.webshare.io/?referral_code=p7k7whpdu2jg) | Good Premium Proxies (paid): [922proxy](https://www.922proxy.com/register?inviter_code=d03d4fed), [proxy-cheap](https://app.proxy-cheap.com/r/JysUiH), [infatica](https://dashboard.infatica.io/aff.php?aff=544)
3. VPS (OPTIONAL) and Python3
# Setup Tutorial
- Open [Nodepay](https://app.nodepay.ai/register?ref=ZUCBuJaIoBXLE6J) and login to dashboard
- Press F12 or CTRL + SHIFT + I
- Select Console
- At the console, type ```allow pasting``` and press enter
![0001](https://github.com/im-hanzou/getgrass_bot/blob/main/pasting.JPG)
- Then type ``localStorage.getItem('np_token')`` and press enter
![0002](https://github.com/im-hanzou/getgrass_bot/blob/main/nodepaytoken.png)
- The text that appears is your nodepay token and copy the text
### Component installation
- Install Python For Windows: [Python](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe)
- For Unix:
```bash
apt install python3 python3-pip -y
```
- Installing requirements: 
```bash
python -m pip install -r requirements.txt
```
### Run the Bot
- Replace the proxies example in ```proxies.txt``` to your own proxies, please use only 10 proxies with proxies http only.
#### Run command
- Run for original server - version 2:
```bash
python runv2.py
```
>Press Enter then insert your nodepay token
- ~Run for original server~:
```bash
python run.py
```
>~Press Enter then insert your nodepay token~ Not working anymore, please use ``runv2.py``
- ~Run for bypass server~:
>~Use this script if you getting errors like ```Error during API call: 403 Client Error: Forbidden for url```~. Not working anymore, please use ``runv2.py``
```bash
python run-bypass.py
```
>~Press Enter then insert your nodepay token~ Not working anymore, please use ``runv2.py``
- ~Run for multi bypassed server~:
```bash
python run-multi-bypass.py
```
>Not working anymore, please use ``runv2.py``
# Operating status
If the following log appears, it means it is running successfully.
```bash
[2024-12-02 14:54:54] [INFO] Account: user@email.com | Browser ID: xxxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx | IP: 127.0.0.1 | IP Score: 99
[2024-12-02 14:54:58] [INFO] Account: user@email.com | Browser ID: xxxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx | IP: 127.0.0.1 | IP Score: 86
[2024-12-02 14:54:59] [INFO] Account: user@email.com | Browser ID: xxxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx | IP: 127.0.0.1 | IP Score: 92
[2024-12-02 14:55:02] [INFO] Account: user@email.com | Browser ID: xxxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx | IP: 127.0.0.1 | IP Score: 81
[2024-12-02 14:55:11] [INFO] Account: user@email.com | Browser ID: xxxxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx | IP: 127.0.0.1 | IP Score: 82
```
# Notes
- Run this bot, and it will update your referrer code to my invite code if you don't have one.
- One account only can connect with 10 Proxies.
- Feel free to enjoy and recode or create new bots using the Nodepay API with direct IP that I found.
- You can just run this bot at your own risk, I'm not responsible for any loss or damage caused by this bot. This bot is for educational purposes only.
