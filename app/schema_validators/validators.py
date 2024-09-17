class StrLengthValidator:
    @staticmethod
    def validate(column: str, data: str, constraint: int) -> None:
        if len(data) > constraint:
            raise ValueError(
                f"{column.capitalize()} must not be longer than ",
                f"{constraint} chars"
            )
