# TODO this does nothing, collection of methods that were IN THE WRONG PLACE FFS DEVIN

class DifficultyManager:
    DEFAULT_TARGET_BLOCK_TIME = 10

    def __init__(self, blockchain):
        self.blockchain = blockchain

    def adjusted_difficulty(self, target_block_time):
        if len(self.blockchain.chain) <= 10:
            return self.blockchain.difficulty
        last_10_blocks = self.blockchain.chain[-10:]
        total_time = sum(last_10_blocks[i].timestamp - last_10_blocks[i - 1].timestamp for i in range(1, 10))
        average_block_time = total_time / 9
        if average_block_time < target_block_time:
            return self.blockchain.difficulty + 1
        elif average_block_time > target_block_time:
            return max(1, self.blockchain.difficulty - 1)
