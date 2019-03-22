def handle(key, vars_):
    if key is not None:
        try:
            code = int(key.key_code)
        except AttributeError:
            code = None
            
        if code in (-203, -204, -205, -206, 13, 10, -300, 113, 81):
            return code
        else:
            return False