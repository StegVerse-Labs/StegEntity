class StegEntityError(Exception):
    pass

class ValidationError(StegEntityError):
    pass

class AuthorityError(StegEntityError):
    pass

class AdapterError(StegEntityError):
    pass

class VerificationError(StegEntityError):
    pass
