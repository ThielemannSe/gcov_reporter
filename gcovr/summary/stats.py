from dataclasses import dataclass


@dataclass
class CoverageStat:
    total: int
    covered: int


@dataclass
class CoverageSummary:
    line_coverage: CoverageStat
    function_coverage: CoverageStat
    branch_coverage: CoverageStat
