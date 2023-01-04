# Lodge Booking Payment Lambda
A Python-based lambda to handle Payfast payments on our Accommodation Booking page

## Development

Set up your virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Deployment

Adapted from [the AWS docs](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html):

```bash
cd venv/lib/python3.8/site-packages/
zip -r ../../../../payments.zip .
cd ../../../../
zip -g payments.zip *.py
aws lambda update-function-code --function-name MyLambdaFunction --zip-file fileb://payments.zip

```

Set the environment variables. The examples below are for [Payfast's Sandbox environment](https://support.payfast.co.za/portal/en/kb/articles/how-do-i-make-test-payments-in-sandbox-mode)
```bash
# Set env variables
aws lambda update-function-configuration --function-name SimSafari_Lodge_Booking_Payment_API \
    --environment "Variables={\
    APP_PAYFAST_MERCHANT_ID=10004002,\
    APP_PAYFAST_MERCHANT_KEY=q1cd2rdny4a53,\
    APP_PAYFAST_PASSPHRASE=payfast,\
    APP_PAYFAST_ONSITE_URL=https://sandbox.payfast.co.za/onsite/process,\
    APP_PAYFAST_EMAIL_CONFIRMATION=1,\
    APP_PAYFAST_CONFIRMATION_ADDRESS=dirk@laarse.co.za\
    }"
```