def validate_code(code, language):
    if language == 'python':
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False
    elif language == 'cpp':
        try:
            return True
        except Exception:
            return False
    # TODO: Добавить проверки для других языков
    return True