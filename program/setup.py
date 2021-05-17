from setuptools import setup

setup(
    name='Suitcase-RPi',
    version='1',
    packages=['nmea_data', 'sophusUtil'],
    url='',
    license='me',
    author='sophus',
    author_email='Sophus@fredborg.no',
    description='parser for NMEA sensors and zmq sender'
)

    """Ethernet transmitter.

    Sends data to the API from the suitcase.
    """
        """publishes a zmq message with the "commands" payload name. :param
        message: message to be published :return: None
        """initilaizes the server, with setting the zmq socket, and adding the
        storage box :param ip: :param storage_box: :param frequncy:

        Args:
            ip:
            storage_box:
            frequncy:
        """

        Args:
            message:
        """
        """send commands over ZMQ :return:"""
        """send sensor data over ZMQ :return:"""
        """gets and sends data from the storage box, tries to reconect if
        it'sclosed :return:
        """