from pydantic import BaseModel, Field, field_validator


class PasswordOptions(BaseModel):
    length: int = Field(12, ge=8, le=128)
    include_numbers: bool = True
    include_symbols: bool = True

    @field_validator('length')
    def check_length(cls, value: int) -> int:
        if value < 8:
            raise ValueError("Password length must be at least 8 characters long.")
        return value
