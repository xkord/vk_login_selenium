import argparse
import logging
import os
from settings import read_settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command

__version__ = "0.0.1.dev0"
logger = logging.getLogger(__name__)
DEFAULT_CONFIGS_NAME = "configs"

def parse_arguments():
    parser = argparse.ArgumentParser(
        description = 'VK login with selenium web driver',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-V', '--verbose', action = 'store_const',
                        const = logging.DEBUG, dest = 'verbosity',
                        help = 'Make a lot of noise')

    parser.add_argument('-v', '--version', action = 'version',
                        version = __version__,
                        help = 'Print version number and exit')

    parser.add_argument('-c', '--configs', dest = 'configs', default = DEFAULT_CONFIGS_NAME, 
                        help = 'Directory with files contains login and password. Default'
                        'value is {0}'.format(DEFAULT_CONFIGS_NAME))

    return parser.parse_args()

def vk_login_selenium(browser, settings):
    #browser.set_page_load_timeout(30)
    #browser.implicitly_wait(30);
    browser.get('https://www.vk.com')
    
    email = browser.find_element_by_id('index_email')
    email.click()
    email.clear()
    email.send_keys(settings['LOGIN'])

    password = browser.find_element_by_id('index_pass')
    password.click()
    password.clear()
    password.send_keys(settings['PASSWORD'])

    login = browser.find_element_by_id('index_login_button')
    login.click()

def main():
    args = parse_arguments()

    logger.addHandler(logging.StreamHandler())

    if (args.verbosity):
        logger.setLevel(args.verbosity)
    else:
        logger.setLevel(logging.INFO)

    logger.debug('vk_promo version: %s', __version__)

    if args.configs is not None and os.path.isdir(args.configs):
        configs_dir = args.configs
        for root, subFolders, files in os.walk(configs_dir):
            for file in files:
                if file.endswith(".conf"):
                    settings = read_settings(os.path.join(root, file))
                    browser = webdriver.Firefox()
                    vk_login_selenium(browser, settings)

if __name__ == "__main__":
    main()