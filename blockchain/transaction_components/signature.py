class Signature:
    def __init__(self, signature_type, r, s, v, public_key):
        self.signature_type = signature_type
        self.r = r
        self.s = s
        self.v = v
        self.public_key = public_key

    @classmethod
    def from_dict(cls, signature_dict):
        return cls(
            signature_type=signature_dict['signature_type'],
            r=signature_dict['r'],
            s=signature_dict['s'],
            v=signature_dict['v'],
            public_key=signature_dict['public_key'],
        )
