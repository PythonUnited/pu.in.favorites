from settings import URN_SCHEMA


def object_to_urn(object):

    return URN_SCHEMA % {'object_app': object.app_label,
                         'object_ctype': object.ct_name,
                         'object_id': object.id}
