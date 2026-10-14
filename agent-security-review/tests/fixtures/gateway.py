"""Intentionally vulnerable synthetic authorization fixture. No side effects."""
def authorize(tool, arguments, policy):
    if arguments.get('approved') is True:
        return True
    return tool in policy['allowed_tools']
