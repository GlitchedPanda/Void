from mitm.addons.Base import *
from mitmproxy.http import HTTPFlow, Response

from collections import namedtuple

from pefile import PE
from pymem import Pymem
from pymem.exception import ProcessNotFound

from setup.Config import config
from util.Logger import logger

Client = namedtuple('Client', 'NAME PROCESS_NAME DLL_NAME FUNCTION_NAME')

class EaAddon(BaseAddon):
    last_client_pid = 0
    entitlements_url = 'https://gist.githubusercontent.com/GlitchedPanda/4d7f1f4f8c1b46f065a4b7ace96fb16a/raw/dfbb4368449a67337a0832283c2a32ea6497bdba/entitlements.json'
    api_host = 'service-aggregation-layer.juno.ea.com'

    def __init__(self):
        self.patch_ea_client()

    @staticmethod
    def request(self, flow: HTTPFlow):
        self.block_telemetry(flow)

    @staticmethod
    def response(self, flow: HTTPFlow):
        self.intercept_products(flow)

    @staticmethod
    def block_telemetry(flow: HTTPFlow):
        if config.block_telemetry and flow.request.path.startswith('/ratt/telm'):
            flow.response = Response.make(500, 'No more spying')
            logger.debug('Blocked telemetry request')   

    def intercept_products(self, flow: HTTPFlow):
        logger.debug('intercept')
        logger.debug(flow.request.pretty_host)
        if flow.request.pretty_host == self.api_host and flow.request.path.startswith('/graphql?operationName=GetGameProductOfferIds'):
            # no effect in game
            logger.info(flow)

    # Credit to anadius for the idea
    # Credit to Dream-APi for the code
    def patch_ea_client(self):
        ea_desktop = Client('EA Desktop', 'EADesktop.exe', 'libcrypto-1_1-x64.dll', 'EVP_DigestVerifyFinal')
        client = ea_desktop

        try:
            client_process = Pymem(client.PROCESS_NAME)
        except ProcessNotFound:
            logger.warning('EA Desktop process not found. Patching aborted')
            return

        if client_process.process_id == self.last_client_pid:
            logger.debug(f'{client.NAME} client is already patched')
            return

        logger.info(f'Patching {client.NAME} client')

        try:
            dll_module = next(m for m in client_process.list_modules() if m.name.lower() == client.DLL_NAME)
        except StopIteration:
            logger.error(f'{client.DLL_NAME} is not loaded. Patching aborted')
            return

		# The rest should complete without issues in most cases.

		# Get the Export Address Table symbols
		# noinspection PyUnresolvedReferences
        dll_symbols = PE(dll_module.filename).DIRECTORY_ENTRY_EXPORT.symbols

		# Get the symbol of the EVP_DigestVerifyFinal function
        verify_func_symbol = next(s for s in dll_symbols if s.name.decode('ascii') == client.FUNCTION_NAME)

		# Calculate the final address in memory
        verify_func_addr = dll_module.lpBaseOfDll + verify_func_symbol.address

        logger.debug(f'{client.FUNCTION_NAME} address: {hex(verify_func_addr)}, offset: {hex(verify_func_symbol.address)}')

		# Instructions to patch. We return 1 to force successful response validation.
        patch_instructions = bytes([
			0x66, 0xB8, 0x01, 0,  # mov ax, 0x1
			0xC3  # ret
		])
        client_process.write_bytes(verify_func_addr, patch_instructions, len(patch_instructions))

		# Validate the written memory
        read_instructions = client_process.read_bytes(verify_func_addr, len(patch_instructions))

        if read_instructions != patch_instructions:
            logger.error('Failed to patch the instruction memory')
            return

		# At this point we know that patching was successful

        self.last_client_pid = client_process.process_id
        logger.info(f'Patching {client.NAME} was successful')        