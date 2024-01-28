from urllib.parse import urlparse, parse_qs


def parse_url(url):
    """
    Parses the given URL and returns structured information.
    """
    parsed_url = urlparse(url)

    path_steps = parsed_url.path.strip('/').split('/') if parsed_url.path else []
    query_params = parse_qs(parsed_url.query)

    response_data = {
        'protocol': parsed_url.scheme or "Not specified",
        'domain': parsed_url.netloc or "Not specified",
        'path_steps': path_steps,
        'query_params': query_params,
        'fragment': parsed_url.fragment or "Not specified"
    }
    return response_data
