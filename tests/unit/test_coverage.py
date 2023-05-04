from gcovr.coverage.model import Branch, Line
import pytest


def test_adding_branches_sums_count():
    b1 = Branch(count=12, fallthrough=False, throw=False)
    b2 = Branch(count=99, fallthrough=True, throw=True)

    result = b1 + b2

    assert isinstance(result, Branch)
    assert result.count == b1.count + b2.count


@pytest.mark.parametrize("t1", [True, False])
@pytest.mark.parametrize("t2", [True, False])
def test_adding_branches_adds_throw_and_fallthrough_by_or(t1: bool, t2: bool):
    b1 = Branch(count=12, fallthrough=t1, throw=t2)
    b2 = Branch(count=99, fallthrough=t2, throw=t1)

    result = b1 + b2

    assert isinstance(result, Branch)
    assert result.throw == t1 | t2
    assert result.fallthrough == t1 | t2


def test_adding_lines_sums_up_count():
    l1 = Line(lineno=1, count=12, function_name="fake_func")
    l2 = Line(lineno=1, count=34, function_name="fake_func")

    result = l1 + l2

    assert result.count == l1.count + l2.count


def test_adding_up_lines_merges_branches():
    l1 = Line(
        lineno=1,
        count=12,
        function_name="fake_func",
        branches={
            1: Branch(count=12),
            2: Branch(count=0),
            3: Branch(count=11),
            4: Branch(count=0),
        },
    )
    l2 = Line(
        lineno=1,
        count=12,
        function_name="fake_func",
        branches={
            1: Branch(count=12),
            2: Branch(count=99),
        },
    )

    result = l1 + l2

    assert 1 in result.branches
    assert 2 in result.branches
    assert 3 in result.branches
    assert 4 in result.branches

    assert result.branches[1].count == 24
    assert result.branches[2].count == 99
    assert result.branches[3].count == 11
    assert result.branches[4].count == 0
