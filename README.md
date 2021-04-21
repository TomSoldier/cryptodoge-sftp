# cryptodoge-sftp

## How to start the modules

From the **root folder** of the project, use the following commands in command line or PowerShell:

**The starting order should be as follows:**

`python -m src.network.network`

`python -m src.server.server`

`python -m src.client.client`

**NOTES:**

Without modules the relative imports in the folder structure can not be handled.
**\_\_init\_\_.py** files used to handle modules. They can be empty.
