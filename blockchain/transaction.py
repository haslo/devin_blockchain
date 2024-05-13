class Transaction:
    def __init__(self, type, sender, payload, nonce, chain, gas, signature):
        self.type = type
        self.sender = sender
        self.payload = payload
        self.nonce = nonce
        self.chain = chain
        self.gas = gas
        self.signature = signature

    def validate_transaction(self):
        """
        Validates a transaction to ensure it follows the new protocol structure and that the signature is valid.
        :param transaction: The transaction to validate.
        :raise ValueError: If the transaction is invalid.
        """
        required_fields = [("type", self.type),
                           ("sender", self.sender),
                           ("payload", self.payload),
                           ("nonce", self.nonce),
                           ("chain", self.chain),
                           ("gas", self.gas),
                           ("signature", self.signature)]
        for field in required_fields:
            if field[1] is None:
                raise ValueError(f"Transaction is missing required field: {field[0]}")
        if not isinstance(self.payload, dict) or "recipient" not in self.payload or "amount" not in self.payload:
            raise ValueError("Invalid payload structure")
        if not isinstance(self.nonce, int) or self.nonce < 0:
            raise ValueError("Invalid nonce")
        if not isinstance(self.gas, dict) or "tip" not in self.gas or "max_fee" not in self.gas or "limit" not in self.gas:
            raise ValueError("Invalid gas structure")
        if any(not isinstance(self.gas[key], int) or self.gas[key] < 0 for key in ["tip", "max_fee", "limit"]):
            raise ValueError("Invalid gas values")
        if (not isinstance(self.signature, dict) or
                "type" not in self.signature or
                "r" not in self.signature or
                "s" not in self.signature or
                "v" not in self.signature or
                "public_key" not in self.signature):
            raise ValueError("Invalid signature structure")

    def to_dict(self):
        """
        Exports the validated transaction data as a dictionary.

        If the transaction is not valid, raises a ValueError.

        :returns: A valid dictionary containing transaction details such as type, sender, payload, nonce, chain, gas, and signature.
        :rtype: dict
        :raises ValueError: If the validation of the transaction fails.
        """
        self.validate_transaction()
        return {
            "type": self.type,
            "sender": self.sender,
            "payload": self.payload,
            "nonce": self.nonce,
            "chain": self.chain,
            "gas": self.gas,
            "signature": self.signature
        }
