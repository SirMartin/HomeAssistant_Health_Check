import time
import requests
import os


def health_check_home_assistant_external(url, key, timeout):
    print("Checking External URL Home Assistant")
    try:
        response = requests.get(f'{url}/api/',
                                headers={'Authorization': key},
                                timeout=timeout)
        return response.status_code == 200
    except Exception as ex:
        print("HA External error.")
        print(getattr(ex, 'message', repr(ex)))
        return False


def health_check_home_assistant_internal(url, key, timeout):
    try:
        print("Checking Internal URL Home Assistant")
        response = requests.get(f'{url}/api/',
                                headers={'Authorization': key},
                                verify=False,
                                timeout=timeout)
        return response.status_code == 200
    except Exception as e:
        print("HA Internal error.")
        print(getattr(e, 'message', repr(e)))
        return False


def proxmox_vm_start(url, key, nodes_path):
    try:
        print("Starting Home Assistant")
        response = requests.post(f'{url}/api2/json/{nodes_path}/start',
                                 headers={'Authorization': key},
                                 verify=False)
        return response.status_code == 200
    except Exception as ex:
        print("Start VM error.")
        print(getattr(ex, 'message', repr(ex)))
        return False


def proxmox_vm_stop(url, key, nodes_path):
    try:
        print("Stopping Home Assistant")
        response = requests.post(f'{url}/api2/json/{nodes_path}/stop',
                                 headers={'Authorization': key},
                                 verify=False)
        return response.status_code == 200
    except Exception as ex:
        print("Stop VM error.")
        print(getattr(ex, 'message', repr(ex)))
        return False


def send_message_to_telegram(url, chat_id, msg):
    if url is None or chat_id is None:
        return
    try:
        print(f"Sending {msg} to Telegram.")
        print(f'https://api.telegram.org/{url}/sendMessage')
        requests.post(f'https://api.telegram.org/{url}/sendMessage',
                      data={'chat_id': chat_id, 'text': msg})
    except Exception as e:
        print(f"Telegram error with msg: {msg}")
        print(getattr(e, 'message', repr(e)))


def run():
    # Load environment variables.
    ha_url_internal = os.environ["HA_URL_INTERNAL"]
    ha_url_external = os.environ["HA_URL_EXTERNAL"]
    ha_key = os.environ["HA_KEY"]
    proxmox_url = os.environ["PROXMOX_URL"]
    proxmox_key = os.environ["PROXMOX_KEY"]
    proxmox_vm_path = os.environ["PROXMOX_VM_PATH"]
    telegram_url = os.environ.get("TELEGRAM_URL", None)
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID", None)
    retry_count = int(os.environ.get("RETRY_COUNT", 3))
    sleep_time = int(os.environ.get("SLEEP_TIME_SECONDS", 60))
    timeout_ha = int(os.environ.get("TIMEOUT_HA_SECONDS", 30))

    retries_attempted = 0

    while True:
        if not health_check_home_assistant_external(ha_url_external, ha_key, timeout_ha):
            ha_alive = health_check_home_assistant_internal(
                ha_url_internal, ha_key, timeout_ha)

            if not ha_alive:
                retries_attempted += 1

                if retries_attempted > retry_count:
                    # Stop and start the VM
                    retries_attempted = 0
                    send_message_to_telegram(telegram_url, telegram_chat_id, "Stopping Home Assistant's VM")
                    proxmox_vm_stop(proxmox_url, proxmox_key, proxmox_vm_path)
                    time.sleep(15)
                    send_message_to_telegram(telegram_url, telegram_chat_id, "Starting Home Assistant's VM")
                    proxmox_vm_start(
                        url=proxmox_url, key=proxmox_key, nodes_path=proxmox_vm_path)
                    send_message_to_telegram(telegram_url, telegram_chat_id, "Home Assistant's VM working again!")

        # Sleep the process for 60 seconds.
        time.sleep(sleep_time)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print("Main error.")
        print(getattr(e, 'message', repr(e)))
