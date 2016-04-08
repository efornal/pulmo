
def are_all_empty_params( params ):
    for key,value in params.iteritems():
        if value:
            return False
    return True

def to_v( field_value ):
    return field_value or ''
