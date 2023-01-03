import dataclasses
import os
from typing import Optional
from pydantic.dataclasses import dataclass

@dataclass
class Config:
    """Class for configuration variables"""
    payfast_merchant_id: Optional[str] = None
    payfast_merchant_key: Optional[str] = None
    payfast_passphrase: Optional[str] = None
    payfast_onsite_url: Optional[str] = None
    payfast_email_confirmation: Optional[str] = None
    payfast_confirmation_address: Optional[str] = None

    def initialise_from_env(self) -> None:
        """
        Initialise dataclass using environment variables.
        The expected name is 'APP_[uppercase key name]'
        e.g. for a property 'secret_key', the corresponding environment variable
        is 'APP_SECRET_KEY'
        """
        for key in dataclasses.asdict(self).keys():
            self.__setattr__(key, os.getenv(f'APP_{key.upper()}'))
        
        if not all(dataclasses.asdict(self).values()):
            raise ValueError("Missing environment variables")
