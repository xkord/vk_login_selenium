# VK login with selenium web driver (vk_login_selenium)

Simple script for vk login procedure with selenium web driver

## Usage

Create directory for configuration files:

```sh
mkdir configs
```

Prepare configuration files. Configuration file format:

	LOGIN = 'login'
	PASSWORD = 'password'

You can create few configuration files for logginig into few vk accounts. Configuration file names must ends with '.conf'.

Run:

```python
python vk_login_selenium.py -c congigs
```
