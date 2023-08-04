import asyncio
from mitm.MitmHandler import start_proxy

from colorama import Fore

from util.Logger import logger

from setup.CertUtil import *
from setup.ProxyUtil import disable_proxy
from setup.Config import config

VERSION = '1.0.0'
TITLE = f'''{Fore.MAGENTA} _   _  _____  _____ ______ 
| | | ||  _  ||_   _||  _  \\
| | | || | | |  | |  | | | |
| | | || | | |  | |  | | | |
\\ \\_/ /\\ \\_/ / _| |_ | |/ / 
 \\___/  \\___/  \\___/ |___/  
                   {Fore.BLUE}v{Fore.LIGHTMAGENTA_EX + VERSION}
                            '''

if __name__ == '__main__':
    try:
        os.system('cls')
        print(TITLE)

        if not is_cert_installed():
            install_cert()  
        
        asyncio.run(start_proxy('127.0.0.1', config.port))  

        if config.delete_cert_on_exit:
            delete_cert()

        asyncio.get_running_loop    

        logger.info('Succesfully exited')        
        disable_proxy()
    except KeyboardInterrupt:
        logger.warning('Keyboard Interrupted') 
        disable_proxy()   
    except BaseException as e:
        logger.exception(e)
        disable_proxy()
