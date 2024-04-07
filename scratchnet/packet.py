from scratchnet.logger import Logger
from profanity import profanity
from os.path import abspath, dirname, join


class Packet:
    # Static variable to store character list
    CHARACTER_LIST: list[str]

    @staticmethod
    def init():
        """
        Initializes the character list from the character_list.txt file.
        """
        base_dir = abspath(dirname(__file__))
        with open(abspath(join(base_dir, './character_list.txt'))) as file:
            Packet.CHARACTER_LIST = [line.rstrip('\n') for line in file]
        Packet.CHARACTER_LIST.append(' ')

    def __init__(self, packet_data=None):
        """
        Constructor for Packet class.

        Args:
            packet_data (str, optional): Packet data to initialize the object with.
        """
        self.__encoded_idx = 0
        self.__encoded_string = packet_data or ''

    def write_number(self, num: int):
        """
        Writes a number to the encoded string.

        Args:
            num (int): Number to be written.
        """
        val = round(num)
        val_str = str(val)
        final = f'0{abs(val)}' if val < 0 else val_str
        length = len(final) + 1
        self.__encoded_string += f'{length}{final}'

    def write_string(self, string: str):
        """
        Writes a string to the encoded string.

        Args:
            string (str): String to be written.
        """
        if profanity.contains_profanity(string):
            Logger.warn('Tried to write a string with profanity, replacing it.')
            string = 'SERVER ERROR: your message contained profanity!'
        encoded = ''.join(str(Packet.CHARACTER_LIST.index(char) + 10) for char in string)
        self.__encoded_string += f'{encoded}00'

    def read_number(self):
        """
        Reads a number from the encoded string.

        Returns:
            int: The read number.
        """
        val_str = ''
        length = int(self.__encoded_string[self.__encoded_idx])
        for _ in range(length):
            self.__encoded_idx += 1
            val_str += self.__encoded_string[self.__encoded_idx]
        self.__encoded_idx += 1
        int_val = int(val_str[1:])
        return -int_val if val_str[0] == '0' else int_val

    def read_string(self):
        """
        Reads a string from the encoded string.

        Returns:
            str: The read string.
        """
        string = ''
        while self.__encoded_string[self.__encoded_idx:self.__encoded_idx+2] != '00':
            code = int(self.__encoded_string[self.__encoded_idx:self.__encoded_idx+2]) - 10
            string += Packet.CHARACTER_LIST[code]
            self.__encoded_idx += 2
        self.__encoded_idx += 2
        return string

    def read_struct(self, struct: list[str]) -> list[int | str] | None:
        """
        Reads a packet with types provided by a struct.

        Example:
            PLAYER_PACKET_STRUCT = ['string', 'int', 'int']


        Args:
            struct (list[str]): Type structure.
        """
        output: list[int | str] = []
        for struct_type in struct:
            lower = struct_type.lower()
            if lower == 'string':
                output.append(self.read_string())
            elif lower == 'int':
                output.append(self.read_number())
            else:
                Logger.err(f'Cannot read struct with invalid type "{lower}".')
                return None

        return output

    def set_idx(self, idx: int):
        """
        Sets the index for reading from the encoded string.

        Args:
            idx (int): Index to set.
        """
        self.__encoded_idx = idx

    def form_packet(self, encoded_string: str):
        """
        Forms a packet from the given encoded string.

        Args:
            encoded_string (str): Encoded string to form the packet from.
        """
        self.__encoded_string = encoded_string
        self.__encoded_idx = 0

    def get_raw_data(self):
        """
        Returns the raw encoded data.

        Returns:
            str: The raw encoded data.
        """
        return self.__encoded_string
