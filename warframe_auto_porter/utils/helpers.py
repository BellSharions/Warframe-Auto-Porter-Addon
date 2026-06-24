import re

from ..constants import COLOR_SPACE_MAP


def strtobool(val):
    if not isinstance(val, str):
        return val
    if val.lower() in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif ('none') in val.lower() or val.lower() in ('none', '', 'no', 'false'):
        return False
    else:
        return False


def get_color_space(source):
    """Determine color space based on source name"""
    if source in COLOR_SPACE_MAP:
        return COLOR_SPACE_MAP[source]
    source_lower = source.lower()
    for key in COLOR_SPACE_MAP:
        if key.lower() in source_lower:
            return COLOR_SPACE_MAP[key]
    return 'sRGB'


def contains(str1, str2):
    if not isinstance(str1, str) or not isinstance(str2, str):
        return True
    if '=' in str1.lower() or '=' in str2.lower():
        return str1.lower() == str2.lower()
    return str1.lower() in str2.lower()


def containstexture(str1, str2):
    if not isinstance(str1, str) or not isinstance(str2, str):
        return True
    if '=' in str1.lower() or '=' in str2.lower():
        return str1.lower() == str2.lower()
    pattern = re.compile(r'\b' + re.escape(str1.lower()) + r'\b')
    return bool(pattern.search(str2.lower()))
