# 2022-12-30
# dvanderlaarse
# Code adapted from https://developers.payfast.co.za/docs#onsite_payments

import dataclasses
import logging
import urllib.parse
import requests
import hashlib

from config import Config
from transaction import Transaction

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class PayFast:
    def __init__(self, config: Config, transaction: Transaction) -> None:
        self.config = config
        self.transaction = transaction

        self.prepare_data()

    def prepare_data(self) -> None:
        my_data = dataclasses.asdict(self.transaction)

        # Generate signature
        my_data["signature"] = self.generate_signature(my_data)

        # Convert the data array to a string
        self.pf_param_string = self.data_to_string(my_data)


    def data_to_string(self, data_dict: dict) -> str:
        pf_param_string = ""
        for key in data_dict:
            # Get all the data from PayFast and prepare parameter string
            pf_param_string += key + "=" + urllib.parse.quote_plus(data_dict[key].replace("+", " ")) + "&"
        # After looping through, cut the last & or append your passphrase
        pf_param_string = pf_param_string[:-1]
        if self.config.payfast_passphrase != '':
            pf_param_string += f"&passphrase={self.config.payfast_passphrase}"
        return pf_param_string

    def generate_payment_identifier(self):
        url = self.config.payfast_onsite_url
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        response = requests.post(url, data=self.pf_param_string, headers=headers)
        if response.status_code != 200:
            logger.error(f"Payfast Request Failed (status code {response.status_code}): {response.text}")
            return False
        try:
            response_json = response.json()
            uuid = response_json.get('uuid')
            return uuid
        except:
            logger.error(f"Unexpected Payfast Response: {response.text}", exc_info=1)
            return False

    def generate_signature(self, dataArray):
        payload = self.data_to_string(dataArray)
        return hashlib.md5(payload.encode()).hexdigest()
