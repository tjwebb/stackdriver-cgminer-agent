# stackdriver-cgminer-agent

This is a lightweight logging agent that can be run on embedded miner controllers running cgminer.
Most miner controllers are limited in disk and RAM resources, and do not include the basic tools you'd need to run a secure agent, such as Python, OpenSSL, cron, gcc, and so forth.
This package includes an installer that you can run on a remote machine to install the agent and its dependencies over SSH.

Tested on Antminer S7, S9, and S17.

# Install

You will need a Google Cloud Platform account. Create the project that will store your Stackdriver logs.
Clone this repository this on a machine that can access the miner over the network, e.g. your laptop.
It will connect to the miner IP you specify, and prompt you for additional information about your miner and GCP account info.

## 1. Install the Google Cloud SDK

[Download the Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts) for your platform.
Then, authenticate with the `gcloud` command-line tool and select or create the project you want to use.

```sh
gcloud init
```

In the next step, the installer will create a [Service Account](https://cloud.google.com/iam/docs/service-accounts) so that the miner can authenticate with the Stackdriver API.
In order to set up the necessary credentials for Stackdriver logging, your GCP user will need the following roles/permissions:

- roles/


## 2. Install the agent

This script requires that the following binaries are in your `PATH`:
- `gcloud` (installed in the previous step)
- `go`



```py
git clone git@github.com:tjwebb/stackdriver-cgminer-agent.git
pip install -r requirements.txt

python install.py <miner_ip>
```

# Learn More

  - [Stackdriver Logging How-to](https://cloud.google.com/logging/docs/how-to)

