# HOME ASSISTANT HEALTH CHECKER

This is a really easy project to check the health of my **Home Assistant** installation on **Proxmox**.

It just checks periodically if the **Home Assistant** instance is up, and if not _stops_ and _starts_ again the _VM_ in **Proxmox**.

## Configuration (Environment Variables)

In order to work the program properly you need to set up some environment variables, to configure the access to **Home Assistant**, **Proxmox** and **Telegram** to notify you.

### For Home Assistant:
* **HA_URL_INTERNAL** (mandatory) The internal url in your network for the Home Assistant Installation.
> for example: https://192.168.1.111:8123
* **HA_URL_EXTERNAL**
> for example: https://myHomeAssistant.myDomain.com
* **HA_KEY** The key to have access to the Home Assistant API. For more info check [here](https://developers.home-assistant.io/docs/api/rest/).

### For Proxmox:
* **PROXMOX_URL** The URL of your Proxmox installation.
* > for example: https://192.168.1.111:8006
* **PROXMOX_KEY** The PVEAPIToken to use the proxmox API. More info [here](https://pve.proxmox.com/wiki/Proxmox_VE_API).
* **PROXMOX_VM_PATH** The path to the specific container or VM that hosts your Home Assistant installation.
* > for example: nodes/{your_node_name}/qemu/{your_vm/ct_id}/status

### For Telegram:
For more information check [here](https://core.telegram.org/bots/api).
* **TELEGRAM_URL** The part of the URL that contains the bot information and the key. Format _{botId}:{key}_
> for example: bot123456:ABC************************
* **TELEGRAM_CHAT_ID** The ID of the chat that you want to send the messages to.
> for example: 12345678

## Makefile

Inside the Makefile you have some commands:

> ```make run``` It runs the container, it needs a .env file with the environment variables.

> ```make shell``` It runs the container interactively, it needs a .env file with the environment variables.