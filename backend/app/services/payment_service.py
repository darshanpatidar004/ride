import razorpay
from app.core.config import settings

class PaymentService:
    def __init__(self):
        if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
            self.client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
        else:
            self.client = None

    def create_razorpay_order(self, amount_in_paise: int, receipt: str):
        if not self.client:
            # Fallback for dev if keys aren't provided
            return {"id": "fake_order_id", "amount": amount_in_paise, "currency": "INR"}
            
        data = {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": receipt,
            "payment_capture": 1
        }
        return self.client.order.create(data=data)

    def verify_payment_signature(self, params_dict: dict):
        if not self.client:
            return True
        return self.client.utility.verify_payment_signature(params_dict)

payment_service = PaymentService()
