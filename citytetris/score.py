from dataclasses import dataclass

from citytetris.constants import SCORES


@dataclass
class Score:
    full_rows: int
    longest_road: int
    l_j_communities: int
    t_community: int

    def get_total_score(self) -> int:
        score_total = (
            self.full_rows * SCORES.full_rows
            + self.longest_road * SCORES.longest_road
            + self.l_j_communities * SCORES.l_j_communities
            + self.t_community * SCORES.t_community
        )
        return score_total
