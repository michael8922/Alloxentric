import json
import logging
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

from app.config import keycloak_settings, dbclient


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=keycloak_settings.keycloak_url_token)

roles = json.loads(open("app/roles.json").read())

# Funcion para verificar si el usuario tiene permisos para acceder a un recurso
def has_permission(user_roles: List[str], resource: str, method: str) -> bool:
    for role in user_roles:
        if role in roles:
            if resource in roles[role]:
                if method in roles[role][resource]:
                    return True
    return False


def get_db(resource: str, method: str) -> AsyncIOMotorClient:
    def get_token_db(token: Optional[str] = None) -> AsyncIOMotorClient:
        if token:  # Si se proporciona un token, se valida
            try:
                payload = jwt.decode(token, keycloak_settings.keycloak_public_key, algorithms=[ALGORITHMS.RS256],
                                    options={"verify_signature": True, "verify_aud": False, "exp": True})
                logging.debug(payload)
                db_name: str = payload.get("bdName")
                roles: List[str] = payload.get("resource_access")[keycloak_settings.keycloak_client_id]["roles"]

                if not has_permission(roles, resource, method):
                    logging.error(f"Not enough permissions for {roles} to access {resource} with method {method}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Not enough permissions",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            except JWTError as err:
                logging.error(err)
                credentials_exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                raise credentials_exception
            return dbclient[db_name]
        else:  # Si no se proporciona un token, se devuelve acceso sin autenticación
            if resource == "resource1" and method in ["GET", "POST", "PUT", "DELETE"]:
                return dbclient["Cliente1_db"]  # Acceso a Cliente1_db sin autenticación
            elif resource == "resource2" and method in ["GET", "POST", "PUT", "DELETE"]:
                return dbclient["Cliente2_db"]  # Acceso a Cliente2_db sin autenticación
            else:
                # Si no se proporciona un token y no se accede a un recurso permitido sin autenticación
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )

    return get_token_db