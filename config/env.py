import os
from dotenv import load_dotenv

load_dotenv()


PAYSTACK_KEY = os.getenv('PAYSTACK_KEY')
CMC_KEY = os.getenv('CMC_KEY')