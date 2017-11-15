![Alt text](/img/icon.png?raw=true "Falcon Sandbox API Icon")

# VxWebService Python API Connector
The Falcon Sandbox Python API Connector (e.g. for https://www.hybrid-analysis.com/).

## Requirements

- [Python](http://www.python.org) >= 3.4.0
- [python-requests module](http://docs.python-requests.org/en/master/)
- [python-colorama module](http://pypi.python.org/pypi/colorama)

> To install some of the required python modules, please use the `pip` module manager
> Using Debian/Ubuntu OS, this can be done by calling `sudo apt-get install python3-pip`. It will then be available via `pip3`
> Using Windows, this can be done automatically when installing `python` (proper checkbox on the installer has to be checked). It should be available via `pip` 

Usage
---

### Define configuration file

Copy the `config_tpl.py` and name it `config.py`.

The configuration file specifies a triplet of api key/secret and server:

- api_key
- api_secret
- server - full url of the WebService e.g. `https://www.hybrid-analysis.com`

Please fill them with the appropriate data. You can generate a public (restricted) API key by following these instructions:
https://www.hybrid-analysis.com/apikeys/info

If you have the full version of Falcon Sandbox, create any kind of API key in the admin area:
https://www.hybrid-analysis.com/apikeys

### Install python requests module if you're using python < 3.5 [python-requests](http://docs.python-requests.org/en/master/).

Debian/Ubuntu OS:

    sudo apt-get install python3-requests
    
or
    
    pip3 install requests
    
Windows:

    pip install requests

### Install python colorama module, [python-colorama module](http://pypi.python.org/pypi/colorama).

Debian/Ubuntu OS:
    
    pip3 install colorama
    
Windows:

    pip install colorama

### Run the connector. Use 'help' or '-h' (on any API endpoint) to get to know about the various endpoint options. Use '-v' for a more verbose output.

> Depending on your API Key privileges, you will see different options.
> Few actions connected with system state and file submit, are only available while using premium API Key.
> If you are interested in obtaining one, please contact with our [support](https://www.payload-security.com/contact).

    python3 vxapi.py -h
    
After choosing the `action_name`
    
    python3 vxapi.py action_name -h
    
### Use 'verbose' mode to get more wordy output

    python3 vxapi.py action_name -v

![Alt text](/img/cli_example.png?raw=true "Falcon Sandbox API CLI Example Output")

### Notes

> Most Linux OSes have two versions of `python` installed. 
> To ensure that the program will work correctly, please use `python3`.
> In Windows after having installed `python`, please add the parent folder to `PATH` environment variable. Now use `python` to callout the script.

### License

Licensed  GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007
see https://github.com/PayloadSecurity/VxAPI/blob/master/LICENSE.md

Copyright (C) 2017 Hybrid Analysis GmbH
