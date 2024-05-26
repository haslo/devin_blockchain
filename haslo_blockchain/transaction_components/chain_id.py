class ChainId:
    def __init__(self, chain_id, version):
        self.chain_id = chain_id
        self.version = version

    @classmethod
    def from_dict(cls, chain_dict):
        return cls(
            chain_id=chain_dict['chain_id'],
            version=chain_dict['version'],
        )

    def to_dict(self):
        return {
            'chain_id': self.chain_id,
            'version': self.version,
        }
