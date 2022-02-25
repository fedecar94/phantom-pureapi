

def parse_headers(headers):
    accept_list = list()
    language_list = list()
    for header, header_content in headers:
        if header == b'accept':
            accept_list = header_content.split(b',')

    return accept_list, language_list
