from dataclasses import dataclass

@dataclass
class VaemConfig():
    ip              : str
    port            : int
    slave_id        : int

