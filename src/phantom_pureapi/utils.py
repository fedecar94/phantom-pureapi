def get_auth_token_from_headers(headers):
    for header, header_content in headers:
        if header == b"authorization":
            return header_content
    return None


def get_content_type_from_headers(headers):
    accept_list = list()
    for header, header_content in headers:
        if header == b"accept":
            accept_list = header_content.split(b",")

    for content_type in accept_list:
        if content_type in [b"text/html", b"application/json", b"application/msgpack"]:
            return content_type.decode()
    else:
        return "application/json"
