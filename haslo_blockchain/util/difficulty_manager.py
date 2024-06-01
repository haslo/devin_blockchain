class DifficultyManager:
    DEFAULT_TARGET_BLOCK_TIME = 10
    MAX_PERCENTAGE_DIFFERENCE = 5

    def __init__(self, blockchain):
        self.blockchain = blockchain

    def adjusted_difficulty(self, target_block_time):
        if len(self.blockchain.chain) <= 10:
            return self.blockchain.difficulty
        last_10_blocks = self.blockchain.chain[-10:]
        total_time = sum(last_10_blocks[i].timestamp - last_10_blocks[i - 1].timestamp for i in range(1, 10))
        average_block_time = total_time / 9
        percentage_difference = abs((average_block_time - target_block_time) / target_block_time * 100)
        if percentage_difference < self.MAX_PERCENTAGE_DIFFERENCE:
            return self.blockchain.difficulty
        elif average_block_time < target_block_time:
            return self.blockchain.difficulty + 1
        elif average_block_time > target_block_time:
            return max(1, self.blockchain.difficulty - 1)
