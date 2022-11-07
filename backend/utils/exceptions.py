from fastapi import status, HTTPException

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
)

db_write_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Error creating record in database"
)

db_read_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Error reading record from database"
)

invalid_parameters_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid parameters specified"
)
