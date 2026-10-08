from cvxpert.guidelines import load_guidelines


def test_catalogue_loads_exactly_g01_to_g24_with_titles_and_sources():
    guidelines = load_guidelines()

    assert list(guidelines) == [f"G{n:02d}" for n in range(1, 25)]
    for guideline in guidelines.values():
        assert guideline.title
        assert guideline.rule
        assert guideline.sources
    assert (
        guidelines["G02"].title == "Quantify only with numbers the candidate supplied"
    )
    assert guidelines["G02"].rule.startswith("Where scale or impact can be measured")
    assert guidelines["G24"].sources[0].startswith("MIT-PDF")
