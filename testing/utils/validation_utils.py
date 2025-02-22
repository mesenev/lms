def validate_code(code, language):
    if language == 'python':
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False
    # TODO # Добавить проверки для других языков
    return True