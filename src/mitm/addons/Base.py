import re

from mitmproxy.http import HTTPFlow

from urllib.parse import urlparse

class BaseAddon():

	@staticmethod
	def request(flow: HTTPFlow):
		pass

	@staticmethod
	def response(flow: HTTPFlow):
		pass

	@staticmethod
	def block_telemetry(flow: HTTPFlow):
		pass

	@staticmethod
	def host_and_path_match(flow: HTTPFlow, host: str, path: str):
		req_host = flow.request.pretty_host
		req_path = urlparse(flow.request.url).path

		return re.match(host, req_host) and re.match(path, req_path)
