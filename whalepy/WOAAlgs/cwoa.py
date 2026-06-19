from whalepy.WOAAlgs.base import BaseWOAAlg


class CWOA(BaseWOAAlg):

    def next_epoch(self) -> None:
        # TODO: implement chaotic map integration for WOA.
        raise NotImplementedError("CWOA epoch logic is not implemented yet.")
