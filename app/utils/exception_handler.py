from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest

def handle_not_found(item):
    if item is None:
        raise HTTPNotFound(json_body={'status': 'error', 'message': 'data not found'})

def handle_bad_request(is_valid, error):
    if not is_valid:
        raise HTTPBadRequest(json_body={'status': 'error', 'message': error})
