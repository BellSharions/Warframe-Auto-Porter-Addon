import os


def find_internal_path(path):
    index = path.find("Lotus")
    if index == -1:
        return ""
    extracted = path[index:]

    last_segment = os.path.basename(extracted)
    if last_segment == '':
        return extracted

    if '.' in last_segment:
        parts = last_segment.split('.')
        if len(parts) > 1:
            ext = parts[-1]
            if ext.isalpha() and 1 <= len(ext) <= 5:
                extracted = os.path.dirname(extracted)

    return extracted


def find_internal_texture_path(path):
    index = path.find("Lotus")
    if index == -1:
        return ""
    extracted = path[index:]

    return extracted
