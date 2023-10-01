**Deprecated:** This code is irrelevant since Vondelgym moved to a new booking system.

This tool can be used to automatically attempt to book classes at Vondelgym that you subscribed to to receive notifications when a spot comes available.
The tool will read your notifications from the profile page, then read the schedule to find a matching class and book it when there's a spot available.

The package code can be used to interact with the Vondelgym web application. It uses Beautifulsoup to parse the web app HTML and extracts the relevant information from it.

## Usage
Install the tool
```bash
pip install .
```

Set your Vondelgym password as an environment variable
```bash
export VONDELGYM_PASSWORD=[your-password-here]
```

Run the tool
```bash
vondelgym-booker [your-email-here] 
```

## Limitations
Currently only Crossfit classes at Vondelgym Oost can be booked using the tool.

## How I use it

### Recurring job
Running this tool only once is not very useful.
That's why I run it as a [systemd service](https://www.freedesktop.org/software/systemd/man/systemd.service.html) on my Ubuntu machine to run the tool every so 20 seconds. 
This will ensure I booked the spot when it becomes available before someone else takes it.

There is a vondelgym.service at `/etc/systemd/system/vondelgym.service` looking as follows:
```ini
[Unit]
Description=Book Vondelgym classes
[Service]
ExecStart=vondelgym-booker [your-email-here]
```

There is an accompanying vondelgym.timer at `/etc/systemd/system/vondelgym.timer`
```ini
[Unit]
Description=Try to book Vondelgym classes every 20 seconds
[Timer]
OnBootSec=10
OnUnitActiveSec=20
AccuracySec=1s
[Install]
WantedBy=timers.target
```

My password is configured in an environment file at `/etc/systemd/system/vondelgym.service.d/myenv.conf`:
```ini
[Service]
Environment="VONDELGYM_PASSWORD=[your-password-here]"
```

### Azure function
#### Prerequisites
- [azure-functions-core-tools-4](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Clinux%2Ccsharp%2Cportal%2Cbash#v2)
- [azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)

#### Run locally
Be sure to set VONDELGYM_PASSWORD and VONDELGYM_EMAIL as environment variables either in your shell or in Values in `local.settings.json`.

```bash
func start
```

#### Deploy function app
Login
```bash
az login
```

Create resource group
```bash
az group create --name vondelgymbooking-rg --location "West Europe"
```

Create storage account
```bash
az storage account create --name vondelgymstorage --sku Standard_LRS
```

Create function app
```bash
az functionapp create --consumption-plan-location westeurope --runtime python --runtime-version 3.8 --functions-version 4 --name vondelgym-booker --os-type linux --storage-account vondelgymstorage
```

Install local package and Azure function app requirements locally
```bash
pip install --target .python_packages/lib/site-packages -r requirements.txt  .
```

Publish this project as a function to the app
```bash
func azure functionapp publish vondelgym-booker --no-build
```

## Update deployment
```bash
az functionapp update --name vondelgym-booker  --resource-group vondelgymbooking-rg
```