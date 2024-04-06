from colorama import Fore


def info(msg):
	print(f'{Fore.BLUE}[scratchnet] {Fore.WHITE}{msg}')


def warn(msg):
	print(f'{Fore.YELLOW}[warning] {msg}')


def err(msg):
	print(f'{Fore.RED}[error] {msg}')
