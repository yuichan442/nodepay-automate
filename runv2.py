import asyncio
import time
import uuid
from datetime import datetime
from curl_cffi import requests
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def log(level, message, color=Fore.WHITE):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{Fore.CYAN}[{timestamp}]{Style.RESET_ALL} {color}[{level}]{Style.RESET_ALL} {message}"
    print(formatted_message)

def show_warning():
    print(Fore.LIGHTYELLOW_EX + """
   _  __        __    ___              ___       __                  __     
  / |/ /__  ___/ /__ / _ \___ ___ __  / _ |__ __/ /____  __ _  ___ _/ /____ 
 /    / _ \/ _  / -_) ___/ _ `/ // / / __ / // / __/ _ \/  ' \/ _ `/ __/ -_)
/_/|_/\___/\_,_/\__/_/   \_,_/\_, / /_/ |_\_,_/\__/\___/_/_/_/\_,_/\__/\__/ 
                             /___/                                          
          Nodepay Autofarmer by IM-Hanzou: github.com/im-hanzou\n""")
    try:
        confirm = input(Fore.LIGHTRED_EX + "By using this tool means you understand the risks. Do it at your own risk! \n" + 
                       Fore.LIGHTYELLOW_EX + "Press Enter to continue or Ctrl+C to cancel... ")
        if confirm.strip() == "":
            print(Fore.LIGHTGREEN_EX + "Continuing...")
        else:
            print(Fore.LIGHTRED_EX + "Exiting...")
            exit()
    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + "\nExiting...")
        exit()

PING_INTERVAL = 60
RETRIES = 60

DOMAIN_API = {
    "SESSION": "http://api.nodepay.ai/api/auth/session",
    "PING": "https://nw.nodepay.org/api/network/ping"
}

CONNECTION_STATES = {
    "CONNECTED": 1,
    "DISCONNECTED": 2,
    "NONE_CONNECTION": 3
}

proxy_browser_ids = {}

def uuidv4():
    return str(uuid.uuid4())
    
def valid_resp(resp):
    if not resp or "code" not in resp or resp["code"] < 0:
        raise ValueError("Invalid response")
    return resp
    
async def render_profile_info(proxy, token):
    global proxy_browser_ids

    try:
        if proxy not in proxy_browser_ids:
            proxy_browser_ids[proxy] = uuidv4()

        np_session_info = load_session_info(proxy)

        if not np_session_info:
            response = await call_api(DOMAIN_API["SESSION"], {}, proxy, token)
            valid_resp(response)
            account_info = response["data"]
            if account_info.get("uid"):
                save_session_info(proxy, account_info)
                await start_ping(proxy, token, account_info)
            else:
                handle_logout(proxy)
        else:
            account_info = np_session_info
            await start_ping(proxy, token, account_info)
    except Exception as e:
        log("ERROR", f"Error in render_profile_info for proxy {proxy}: {e}", Fore.LIGHTRED_EX)
        error_message = str(e)
        if any(phrase in error_message for phrase in [
            "sent 1011 (internal error) keepalive ping timeout; no close frame received",
            "500 Internal Server Error"
        ]):
            log("WARNING", f"Removing error proxy from the list: {proxy}", Fore.LIGHTYELLOW_EX)
            remove_proxy_from_list(proxy)
            return None
        else:
            log("ERROR", f"Connection error: {e}", Fore.LIGHTRED_EX)
            return proxy

async def call_api(url, data, proxy, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Origin": "chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm",
    }

    try:
        response = requests.post(
            url, 
            json=data, 
            headers=headers, 
            proxies={"http": proxy, "https": proxy},
            timeout=30,
            impersonate="chrome110"
        )

        return valid_resp(response.json())
    except Exception as e:
        log("ERROR", f"Error during API call: {e}", Fore.LIGHTRED_EX)
        raise ValueError(f"Failed API call to {url}")

async def start_ping(proxy, token, account_info):
    try:
        while True:
            await ping(proxy, token, account_info)
            await asyncio.sleep(PING_INTERVAL)
    except asyncio.CancelledError:
        log("INFO", f"Ping task for proxy {proxy} was cancelled", Fore.LIGHTBLUE_EX)
    except Exception as e:
        log("ERROR", f"Error in start_ping for proxy {proxy}: {e}", Fore.LIGHTRED_EX)
        
async def get_real_ip(proxy):
    try:
        response = requests.get(
            "https://api64.ipify.org/", 
            proxies={"http": proxy, "https": proxy},
            timeout=10
        )
        return response.text.strip()
    except Exception as e:
        log("ERROR", f"Failed to get real IP via proxy {proxy}: {e}", Fore.LIGHTRED_EX)
        return "N/A"

async def ping(proxy, token, account_info):
    global proxy_browser_ids, RETRIES, CONNECTION_STATES

    current_time = time.time()

    try:
        data = {
            "id": account_info.get("uid"),
            "browser_id": proxy_browser_ids[proxy],
            "timestamp": int(time.time()),
            "version":"2.2.7"
        }

        response = await call_api(DOMAIN_API["PING"], data, proxy, token)
        if response["code"] == 0:
            ip_score = response.get('data', {}).get('ip_score', 'N/A')
            real_ip = await get_real_ip(proxy)
            log("INFO", 
                f"Account: {Fore.LIGHTGREEN_EX}{account_info.get('email', 'N/A')}{Style.RESET_ALL} | " + 
                f"Browser ID: {Fore.LIGHTMAGENTA_EX}{proxy_browser_ids[proxy]}{Style.RESET_ALL} | " +
                f"IP: {Fore.LIGHTYELLOW_EX}{real_ip}{Style.RESET_ALL} | " + 
                f"IP Score: {Fore.LIGHTRED_EX}{ip_score}{Style.RESET_ALL}", 
                Fore.LIGHTCYAN_EX)
            RETRIES = 0
        else:
            handle_ping_fail(proxy, response)
    except Exception as e:
        log("ERROR", f"Ping failed via proxy {proxy}: {e}", Fore.LIGHTRED_EX)
        handle_ping_fail(proxy, None)

def handle_ping_fail(proxy, response):
    global RETRIES

    RETRIES += 1
    if response and response.get("code") == 403:
        handle_logout(proxy)

def handle_logout(proxy):
    global proxy_browser_ids

    if proxy in proxy_browser_ids:
        del proxy_browser_ids[proxy]
    save_status(proxy, None)
    log("WARNING", f"Logged out and cleared session info for proxy {proxy}", Fore.LIGHTYELLOW_EX)

def load_proxies(proxy_file):
    try:
        with open(proxy_file, 'r') as file:
            proxies = file.read().splitlines()
        return proxies
    except Exception as e:
        log("ERROR", f"Failed to load proxies: {e}", Fore.LIGHTRED_EX)
        raise SystemExit("Exiting due to failure in loading proxies")

def save_status(proxy, status):
    pass  

def save_session_info(proxy, data):
    pass

def load_session_info(proxy):
    return {}  

def is_valid_proxy(proxy):
    return True  

def remove_proxy_from_list(proxy):
    pass  

async def main():
    all_proxies = load_proxies('proxies.txt')  
    token = input(Fore.LIGHTYELLOW_EX + "Nodepay Token: ").strip()
    if not token:
        log("ERROR", "Token cannot be empty. Exiting the program.", Fore.LIGHTRED_EX)
        exit()

    while True:
        active_proxies = [
            proxy for proxy in all_proxies if is_valid_proxy(proxy)][:100]
        tasks = {asyncio.create_task(render_profile_info(
            proxy, token)): proxy for proxy in active_proxies}

        done, pending = await asyncio.wait(tasks.keys(), return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            failed_proxy = tasks[task]
            if task.result() is None:
                log("INFO", f"Removing and replacing failed proxy: {failed_proxy}", Fore.LIGHTYELLOW_EX)
                active_proxies.remove(failed_proxy)
                if all_proxies:
                    new_proxy = all_proxies.pop(0)
                    if is_valid_proxy(new_proxy):
                        active_proxies.append(new_proxy)
                        new_task = asyncio.create_task(
                            render_profile_info(new_proxy, token))
                        tasks[new_task] = new_proxy
            tasks.pop(task)

        for proxy in set(active_proxies) - set(tasks.values()):
            new_task = asyncio.create_task(
                render_profile_info(proxy, token))
            tasks[new_task] = proxy
        await asyncio.sleep(3)
    await asyncio.sleep(10)  

if __name__ == '__main__':
    show_warning()
    print(Fore.LIGHTYELLOW_EX + "Alright, we here! Insert your nodepay token that you got from the tutorial.\n")
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print(Fore.LIGHTRED_EX + "Program terminated by user.")
