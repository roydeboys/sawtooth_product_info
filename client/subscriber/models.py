from django.db import models

"""
    Store block data for each transaction
"""


class BlockInfo(models.Model):
    block_num = models.BigIntegerField()
    block_id = models.CharField(max_length=500)
    state_root_hash = models.CharField(max_length=500)
    previous_block_id = models.CharField(max_length=500)
    address = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return str(self.block_num)

