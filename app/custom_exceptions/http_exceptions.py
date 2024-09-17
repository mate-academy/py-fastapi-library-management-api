from fastapi import HTTPException


class InstanceNotFoundException(HTTPException):
    def __init__(self, model_name: str) -> None:
        super().__init__(
            status_code=404,
            detail=f"{model_name.capitalize()} not found"
        )


class AuthorNotFoundException(InstanceNotFoundException):
    def __init__(self) -> None:
        super().__init__(model_name="Author")


class BookNotFoundException(InstanceNotFoundException):
    def __init__(self) -> None:
        super().__init__(model_name="Book")
