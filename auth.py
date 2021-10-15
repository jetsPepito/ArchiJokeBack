from fastapi import HTTPException, Request, Security
import jwt

async def get_jwt(request: Request):
    jwt_header = request.headers.get("Authorization")

    if jwt_header:
        try:
            token = jwt.decode(jwt_header, "secret",algorithms=["HS512"])
            return {
                "userId" : token["userId"],
                "userName" : token["userName"]
            }
        except:
            raise HTTPException(status_code=401, detail="Unauthorized")
    raise HTTPException(status_code=401, detail="Unauthorized")

