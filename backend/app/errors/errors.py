from fastapi import FastAPI, HTTPException, status


class MissingAttribute(HTTPException):
    def __init__(self, attribute):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"{attribute} is missing")
        self.attribute = attribute


class EntityNotFound(HTTPException):
    def __init__(self, entity):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"{entity} not found")


class JWTDecodeError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token")


class CookieNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Cookie not found")


class UnAuthenticated(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Incorrect email or password")
