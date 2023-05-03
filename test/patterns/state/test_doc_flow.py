from patterns.state.doc_context import DocumentContext


def test_doc_flow():
    doc = DocumentContext()
    assert doc.is_close is False
    assert doc.get_current_state().get_name() == 'initial'
    doc.next()
    assert doc.get_current_state().get_name() == 'approve'
    doc.next()
    assert doc.get_current_state().get_name() == 'close'
    assert doc.is_close is True
