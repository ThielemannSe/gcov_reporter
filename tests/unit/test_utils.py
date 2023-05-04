from gcovr.utils import filter_congruent_coverage_files


def test_filtering_congruent_coverage_files_prefers_gcda():
    files = ["example.gcda", "example.gcno"]
    filtered = filter_congruent_coverage_files(files)

    assert "example.gcda" in filtered
    assert "example.gcno" not in filtered


def test_filtering_congruent_coverage_files_returns_gcno_if_gcda_doesnt_exist():
    files = ["example.gcno"]
    filtered = filter_congruent_coverage_files(files)

    assert "example.gcno" in filtered
    assert len(filtered) == 1
