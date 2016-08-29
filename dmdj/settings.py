from dmdj import SERVICE


def get_url(model, version):
    return '{0}schemata/{1}/{2}?format=json'.format(SERVICE, model, version)
