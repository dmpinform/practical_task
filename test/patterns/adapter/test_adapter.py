from patterns.adapter.client_code import get_all_documents


def test__get_all_documents():
    assert list(
        map(lambda doc: doc.get_author(), get_all_documents()),
    ).sort() == ['Rick', 'Morty'].sort()
