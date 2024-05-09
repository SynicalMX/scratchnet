import sys
import types
import signal
import scratchconnect
import asyncio
from scratchconnect.CloudConnection import CloudConnection
from requests.exceptions import JSONDecodeError
from scratchconnect.Project import Project
from scratchnet.packet import Packet
from scratchnet.logger import Logger
from colorama import Fore
from ssl import SSLEOFError


def sigint(a, b):
	Logger.info(f'Quitting scratchnet...')
	sys.exit(0)


class Server:
	def __init__(self, project_id: int, methods, cloud_name='SCRATCHNET', server_key='$(server)'):
		self.project_id = project_id
		self.methods = methods
		self.cloud_name = cloud_name
		self.server_key = server_key
		self.status = 'stopped'
		self.cloud = ''
		self.old_cloud = ''
		self.user: scratchconnect.ScratchConnect | None = None
		self.project: Project | None = None
		self.variables: CloudConnection | None = None

		signal.signal(signal.SIGINT, sigint)

	def login(self, username: str, password: str):
		Logger.info(f'Attempting to login to {Fore.YELLOW}{username}{Fore.WHITE}...')
		self.user = scratchconnect.ScratchConnect(username, password)
		self.project = self.user.connect_project(self.project_id, access_unshared=True)
		self.variables = self.project.connect_cloud_variables()
		if self.user is not None:
			Logger.info(f'{Fore.GREEN}Logged into {Fore.YELLOW}{username}{Fore.GREEN} successfully!')

	def start(self, username: str, password: str):
		self.status = 'starting'
		Logger.info('Starting server...')
		self.login(username, password)
		Packet.init()
		self.status = 'running'
		self.__main()

	def send_packet(self, packet: Packet) -> bool:
		return self.variables.set_cloud_variable(self.cloud_name, packet.get_raw_data())

	def __main(self):
		while self.status == 'running':
			try:
				self.cloud = self.variables.get_cloud_variable_value(self.cloud_name, limit=5)[0]
			except JSONDecodeError:
				continue
			except SSLEOFError:
				continue

			if self.old_cloud == self.cloud:
				continue

			self.old_cloud = self.cloud

			try:
				packet = Packet(self.cloud)
				owner = packet.read_string()
				method_name = packet.read_string()
			except:
				Logger.err(f'Failed to read packet header.')
				continue

			if owner != self.server_key:
				try:
					method = getattr(self.methods, method_name)
					if isinstance(method, types.FunctionType):
						Logger.info(f'{owner} requested method "{method_name}"')
						response: Packet | None = method(self, owner, packet)
						if response is not None:
							try:
								self.send_packet(response)
							except:
								Logger.err(f'{owner} requested method "{method_name}", but the server failed to send the packet, queueing it again.')
								try:
									success = self.queue_packet(0.1, response)
									if not success:
										Logger.err(f'{owner} requested method "{method_name}", but the server failed to send the packet again.')
										continue
								except:
									Logger.err(f'{owner} requested method "{method_name}", but the server failed to send the packet again.')
									continue
					else:
						Logger.err(f'Server cannot call a method that\'s not a function.... (-_- )')

				except AttributeError:
					Logger.warn(f'{owner} requested invalid method "{method_name}".')
					continue

	async def queue_packet(self, timeout: float, packet: Packet) -> bool:
		await asyncio.sleep(timeout)
		return self.send_packet(packet)
