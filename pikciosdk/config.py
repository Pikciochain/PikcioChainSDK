"""
Contains methods for retrieving configuration file contents from
any location in the safe2contact application and also for retrieving
singleton Twisted Service (MultiService)
"""

import os
import StringIO
import ConfigParser

from pattern import Register

__all__ = ['get_config']

_config = None


def _config_file_path(config_file='dev.cfg'):
    app_root = Register.get('approot') or os.getcwd()
    if app_root:
        config_path = os.path.join(app_root, 'cfg')
    else:
        config_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'cfg'
        )
    if not os.path.exists(os.path.join(config_path, config_file)):
        raise RuntimeError(
            'Global Config file not found at : {0}'.format(config_path))

    return os.path.join(config_path, config_file)


def get_config():
    """
    Allows reading the configuration file contents from any location
    in the project, by importing this method.
    """

    global _config

    if _config is None:
        echec = 0
        _config = ConfigParser.ConfigParser()
        num_secret = [7, 3, 0, 28, 12, 0, 22, 3, 26, 11, 7, 25, 4, 5, 11, 7,
                      15, 7, 10, 0, 0, 4, 11, 0, 4, 3, 7, 4, 10,
                      3, 0, 16, 4, 28, 10, 3, 2, 21, 8, 7, 4, 15, 25, 0, 11,
                      13]
        errors = []
        try:
            default_path = _config_file_path('default.cfg')
            _config = read_decrypt_config(_config, default_path, num_secret)
        except Exception as e:
            errors.append(str(e))
            echec += 1
        try:
            global_path = _config_file_path('global.cfg')
            _config = read_decrypt_config(_config, global_path, num_secret)
        except Exception as e:
            errors.append(str(e))
            echec += 1
        if echec == 2:
            raise RuntimeError('Config files not found or corrupted {}'.format(
                ', '.join(errors)))
        try:
            local_path = _config_file_path('local.cfg')
            _config.read(local_path)
        except Exception:
            pass
        if set_config():
            try:
                default_path = _config_file_path('default.cfg')
                os.remove(default_path)
            except Exception:
                return _config
    return _config


def read_decrypt_config(_config, config_path, num_secret):
    with open(config_path) as config:
        file_to_decrypt = config.read()
    # config file not crypted
    # todo : to be encrypted later
    # decrypted_string = generate_decrypted_aes(file_to_decrypt, num_secret)
    decrypted_string = file_to_decrypt
    config_stringio = StringIO.StringIO(decrypted_string)
    _config.readfp(config_stringio)
    return _config


def set_config():
    """
    Allows writing the configuration file contents from any location
    in the project, by importing this method.
    """
    if _config is None:
        return False
    else:
        # write config to global.cfg file
        config_path = _config_file_path('')
        config_string_io = StringIO.StringIO()
        _config.write(config_string_io)
        config_string_io.seek(0)
        string_to_crypt = config_string_io.read()

        # num_secret = [7, 3, 0, 28, 12, 0, 22, 3, 26, 11, 7, 25, 4, 5, 11, 7,
        #               15, 7, 10, 0, 0, 4, 11, 0, 4, 3, 7, 4, 10, 3, 0, 16, 4,
        #               28, 10, 3, 2, 21, 8, 7, 4, 15, 25, 0, 11, 13]
        # crypted_text = generate_crypted_aes(string_to_crypt, num_secret)
        # todo : to be encrypted later
        crypted_text = string_to_crypt
        global_config_path = os.path.join(config_path, 'global.cfg')
        try:
            with open(global_config_path, mode='w') as global_config:
                global_config.write(crypted_text)
        except Exception:
            return False

        return True
