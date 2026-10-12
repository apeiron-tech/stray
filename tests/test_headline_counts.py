"""The catalog's size on the front door is generated, never typed (`catalog_store.headline_counts`)."""
from stray.domain.catalog import store as catalog_store


def test_headline_counts_round_down_and_skip_routed():
    cat = catalog_store.Catalog()
    for i in range(3218):
        cat.by_id[f"p{i % 69}.e{i}"] = {"id": f"p{i % 69}.e{i}", "provider": f"p{i % 69}"}
    for i in range(75):
        cat.by_id[f"stray.r{i}"] = {"id": f"stray.r{i}", "provider": "stray", "kind": "routed"}
    assert catalog_store.headline_counts(cat) == ("3,200+", 69)


