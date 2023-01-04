import dataclasses
import json
import os
import logging
import re
from typing import Dict

import jsonpickle
from pydantic import ValidationError

from config import Config
from payfast import PayFast
from transaction import HTTPResponse, Transaction, TransactionRequest

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))

    config = Config()
    config.initialise_from_env()

    # Validate and serialise body
    try:
        body = json.loads(event["body"])
        input_dict = {
            key.name: body[snake_case_to_camel_case(key.name)]
            for key in dataclasses.fields(TransactionRequest)
        }
        transaction_request = TransactionRequest(**input_dict)
    except (KeyError, ValidationError, json.JSONDecodeError) as e:
        logger.error("Malformed body", exc_info=1)
        return generate_http_response(
            status_code=400,
            body=f'Malformed body: {e}'
        )
    
    if not transaction_request:
        return generate_http_response(
            status_code=500,
            body='Malformed body. See the logs for details.'
        )

    # Build Transaction and send to Payfast
    transaction = Transaction(
        **dataclasses.asdict(transaction_request),
        merchant_id=config.payfast_merchant_id,
        merchant_key=config.payfast_merchant_key,
        email_confirmation=config.payfast_email_confirmation,
        confirmation_address=config.payfast_confirmation_address
    )

    # Generate Payfast payment identifier
    payfast = PayFast(config=config, transaction=transaction)
    identifier = payfast.generate_payment_identifier()

    if identifier:
        return generate_http_response(
            status_code=200,
            body=json.dumps({'identifier': identifier})
        )
    else:
        return generate_http_response(
            status_code=500,
            body='Payfast Payment Identifier could not be created'
        )

def snake_case_to_camel_case(key: str) -> str:
    """
    Changes 'snake_case_name' to 'SnakeCaseName'
    """
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), key)


def generate_http_response(status_code: int, body: str) -> Dict:
    response = HTTPResponse(
        statusCode=status_code,
        body=body,
        headers={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Access-Control-Allow-Headers': 'X-Amz-Date,X-Api-Key,X-Amz-Security-Token,X-Requested-With,X-Auth-Token,Referer,User-Agent,Origin,Content-Type,Authorization,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers',
            'Access-Control-Allow-Credentials': 'true',
        },
        isBase64Encoded=False
    )
    logger.info("response:")
    logger.info(dataclasses.asdict(response))
    logger.info('## RETURN\r' + jsonpickle.encode(dataclasses.asdict(response)))
    return dataclasses.asdict(response)