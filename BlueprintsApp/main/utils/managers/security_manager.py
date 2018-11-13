from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from utils import logger_utils
from utils.managers.manager import Manager


class SecurityManager(Manager):

    CIPHER = b"CB*(GH&V09IKdsf4"
    IV = b"0000000000000000"
    __LOGGER = logger_utils.get_logger(__name__)

    @classmethod
    def encode_data(cls, data):
        """Description: method encodes incoming string into AES-128 cipher

        :param data: Data string to save
        :return: Encrypted cypher
        """
        backend = default_backend()
        cipher = Cipher(algorithms.AES(SecurityManager.CIPHER), modes.CBC(SecurityManager.IV), backend=backend)
        encryptor = cipher.encryptor()
        data = data.encode("utf-8")
        # Data padding - add zero bytes to the end of the string
        # to make it length divisible by 16 (AES block)
        while len(data) % 16 != 0:
            data += b"0"
        SecurityManager.__LOGGER.debug("Size: {}".format(len(data)))
        return encryptor.update(data) + encryptor.finalize()

    @classmethod
    def decode_data(cls, e_data):
        backend = default_backend()
        cipher = Cipher(algorithms.AES(SecurityManager.CIPHER), modes.CBC(SecurityManager.IV), backend=backend)
        decryptor = cipher.decryptor()
        data = decryptor.update(e_data) + decryptor.finalize()
        data = data.decode("utf-8")
        data = data[::-1]
        for i in range(0, len(data), 1):
            if data[i] != "0":
                SecurityManager.__LOGGER.debug(data[i])
                data = data[i:]
                break
        return data[::-1]
