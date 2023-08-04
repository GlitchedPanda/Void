from mitmproxy import options
from mitmproxy.tools import dump

from util.Logger import logger
from mitm.addons.EA import EaAddon
from setup.ProxyUtil import enable_proxy

async def start_proxy(host, port):
    opts = options.Options(listen_host=host, listen_port=port)

    master = dump.DumpMaster(
        opts,
        with_termlog=False,
        with_dumper=False,
    )
    master.addons.add(EaAddon())

    logger.info('Successfully initialized mitmproxy')

    enable_proxy(port)
    
    await master.run()
    return master