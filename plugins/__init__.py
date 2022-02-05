import logging


def set_plugins():
    from plugins import start, language, subscribe, video, post, other_commands
    logging.info('Plugins imported')
