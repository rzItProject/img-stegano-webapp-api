from pydantic import BaseModel, constr, validator
from datetime import datetime
import re

from app.exceptions.custom_exceptions import (
    InvalidPasswordException,
    InvalidUsernameException,
    InvalidBirthdateException,
    InvalidEmailException,
    InvalidGenderException,
)
from app.infrastructure.database.orm_models.person import Gender


class RegisterValidators(BaseModel):
    username: constr(min_length=3, max_length=30)
    password: constr(min_length=8, max_length=30)
    birthdate: str
    gender: Gender

    @validator("password", pre=True, always=True)
    def validate_password(cls, password) -> str:
        regex = (
            r"^(?=.*[A-Z])"  # Au moins une majuscule
            r"(?=.*[a-z])"  # Au moins une minuscule
            r"(?=.*[0-9])"  # Au moins un chiffre
            r"(?=.*[\&\$\*\_?!])"  # Au moins un caractère spécial parmi &$*_?!
            r"[A-Za-z0-9\&\$\*\_?!]{8,}$"  # au minimum 8 caractère et Interdire les autres caractères spéciaux
        )
        if not re.match(regex, password):
            raise InvalidPasswordException(
                "Le mot de passe doit contenir au moins une majuscule, une minuscule, un chiffre, "
                "un caractère spécial parmi &$*_?! et aucun autre caractère spécial."
            )
        return password

    @validator("username", pre=True, always=True)
    def validate_username(cls, username: str) -> str:
        regex = (
            r"^[a-zA-Z]"  # Commence par une lettre
            r"[a-zA-Z0-9_-]{2,29}$"  # Seulement lettres, chiffres, tirets et underscores
        )
        if not re.match(regex, username):
            raise InvalidUsernameException(
                "Le nom d'utilisateur doit commencer par une lettre et ne peut contenir que des lettres, "
                "des chiffres, des tirets et des underscores."
            )
        return username

    @validator("birthdate", pre=True, always=True)
    def validate_birthdate(birthdate: str) -> str:
        # Vérification du format de la date
        regex = r"^\d{2}-\d{2}-\d{4}$"
        if not re.match(regex, birthdate):
            raise InvalidBirthdateException(
                "La date de naissance doit être au format 'dd-mm-yyyy'."
            )
        """ # Vérification que la date est antérieure à la date actuelle
        if birth_date_obj >= datetime.now():
            raise InvalidBirthdateException(
                "La date de naissance doit être antérieure à la date actuelle."
            ) """

        return birthdate
    
    @validator("gender", pre=True, always=True)
    def gender_validation(cls, gender):
        if hasattr(Gender, gender) is False:
            raise InvalidGenderException("Invalid input gender")
        return gender
