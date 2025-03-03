from .config import NocoSettings

noco_settings = NocoSettings()

def init_noco_settings(settings):
    '''init noco_settings from the main app'''
    global noco_settings # pylint: disable=W0602

    if settings is None:
        return

    for key, value in settings.model_dump().items():
        if hasattr(noco_settings, key):
            setattr(noco_settings, key, value)
