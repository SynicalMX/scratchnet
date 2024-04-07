from colorama import Fore


class Logger:
	@staticmethod
	def info(msg):
		print(f'{Fore.BLUE}[scratchnet] {Fore.WHITE}{msg}')

	@staticmethod
	def warn(msg):
		print(f'{Fore.YELLOW}[warning] {msg}')

	@staticmethod
	def err(msg):
		print(f'{Fore.RED}[error] {msg}')
