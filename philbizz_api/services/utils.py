
from typing import Optional

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth.hashers import make_password, check_password
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum
import jwt
import secrets
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.permissions import BasePermission


def hash_password(plain_text: str) -> str:
    return make_password(plain_text)

def verify_password(plain_text: str, hashed_password: str) -> bool:
    return check_password(plain_text, hashed_password)

class AccessInformation(BaseModel):
    token_type: str = "Bearer"
    access_token: Optional[str] = Field(None, alias="access_token")
    refresh_token: Optional[str] = Field(None, alias="refresh_token")
    expiration: datetime

class ResponseCode(Enum):
    Success = 200
    CounterUpdateObjectNull = 1001
    CounterGreaterThanZeroOne = 200
    CounterNullException = 1002
    CompScratchObjectNullException = 1003
    ThetaZeroCumulativeObjectNullException = 1004
    ExamLoggerObjectNullException = 1005
    CSExamLoggerObjectNullException = 1005
    ResourceDataNullException = 1006
    DisplayNextItemObjectNullException = 1007
    ServerCalcObjectNullException = 1008
    CalcObjectNullException = 1009
    CalcAlreadyExistException = 1010
    QuestionSessionObjectNullException = 1011
    InternalAccountExists = 1012
    InternalServerError = 500
    EmptyParameters = 404
    InternalAccountNotFound = 404
    ErrorWrongPasswordOrUsername = 500
    InvalidAccessTokenOrRefreshToken = 401
    ForceExitApplication = 1013
    CategoryExistException = 1014
    DataExistException = 1015
    InvalidApplication = 1016
    NotFound = 1017
    Error = 1018
    ActiveProductExceed = 1019
    PaymentFailed = 1020
    ActionRequired = 1021
    PaymentMethodAttached = 1022
    AccountNotFound = 404
    Account2FA = 201
    Invalid2FACode = 500
    InvalidVerificationCode = 500
    CodeExpires = 501
    MaximumVerificationCodeSent = 504
    EmailNotFound = 404
    WaitForNextAttempt = 508
    Unauthorized = 401

class AccountLoginResponse(BaseModel):
    access_token_response: AccessInformation
    response_code: int
    is_2fa_enabled: Optional[bool] = None
    two_factor_code_expiry_time: Optional[datetime] = None
    account_id: Optional[UUID] = Field(default=None)
    access_level: Optional[str] = Field(default=None)

def generate_refresh_token():
    return secrets.token_urlsafe(64)

def create_token(claims):
    expiration_time = datetime.utcnow() + timedelta(minutes=settings.JWT_TOKEN_VALIDITY_IN_MINUTES)
    claims["exp"] = expiration_time

    try:
        token = jwt.encode(
            claims,
            settings.JWT_SECRET_KEY,
            algorithm="HS256"
        )
    except Exception as e:
        raise RuntimeError(f"Token encoding failed: {str(e)}")

    return token, expiration_time