from fastapi import HTTPException, status


class get_exception_type:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email_notfound_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find email",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email_already_registered_exception = HTTPException(
        status_code=400,
        detail="email already registered",
    )
    member_notfound_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find member",
    )
    member_already_registered_exception = HTTPException(
        status_code=400,
        detail="username already registered",
    )
    password_wrong_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="password is wrong",
    )
    credentials_info_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find member or email",
        headers={"WWW-Authenticate": "Bearer"},
    )
    member_disalbe_exception = HTTPException(
        status_code=400, detail="Inactive user"
    )
    not_authorized_exception = HTTPException(
        status_code=403, detail="Access denied, You dont have access to this operation"
    )
    article_notfound_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find article number",
    )
    payload_notfound_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="you don't input anything to change",
    )
