from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class AuthGuard(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthGuard, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            AuthGuard, self
        ).__call__(
            request
        )  # type: ignore
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="invalid authentication scheme.",
                )

            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid authorization code.",
            )
