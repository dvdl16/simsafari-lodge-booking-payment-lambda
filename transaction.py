
from typing import Dict
from pydantic.dataclasses import dataclass

@dataclass
class TransactionRequest:
    """Class for a Payfast Transaction Request"""
    name_first: str
    email_address: str
    m_payment_id: str
    amount: str
    item_name: str
    item_description: str
    custom_str1: str


@dataclass
class TransactionMerchant:
    """Class for a Payfast Transaction merchant info"""
    merchant_id: str
    merchant_key: str


@dataclass
class TransactionConfirmation:
    """Class for a Payfast Transaction confirmation info"""
    email_confirmation: str
    confirmation_address: str


@dataclass
class Transaction(TransactionConfirmation, TransactionRequest, TransactionMerchant):
    """Class for a Payfast Transaction"""
    # Inherit from multiple classes to keep correct order of parameters
    pass


@dataclass
class HTTPResponse:
    """Class to return an HTTP Response"""
    statusCode: int
    body: str
    headers: Dict[str, str]
    isBase64Encoded: bool
