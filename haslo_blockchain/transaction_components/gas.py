class Gas:
    def __init__(self, tip, max_fee, limit):
        self.tip = tip
        self.max_fee = max_fee
        self.limit = limit

    @classmethod
    def from_dict(cls, gas_dict):
        return cls(
            tip=gas_dict['tip'],
            max_fee=gas_dict['max_fee'],
            limit=gas_dict['limit'],
        )
