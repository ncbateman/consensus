from pydantic import BaseModel

from bittensor.core.chain_data.axon_info import AxonInfo

class Node(BaseModel):
    uid: int
    stake: float
    rank: float
    trust: float
    consensus: float
    incentive: float
    dividends: float
    emission: float
    validator_trust: float 
    validator_permit: bool
    last_update: int
    active: bool
    axon: AxonInfo | None
    hotkey: str
    coldkey: str

    class Config:
        from_attributes = True