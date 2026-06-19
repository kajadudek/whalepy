from whalepy.WOAAlgs.base import BaseWOAAlg


class MutationWOA(BaseWOAAlg):

    def next_epoch(self) -> None:
        # TODO: implement mutation hooks for WOA.
        raise NotImplementedError("Mutation WOA epoch logic is not implemented yet.")
