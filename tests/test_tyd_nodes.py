def test_tyd_from_text(test_tyd_from_text_params):
    obj, ans = test_tyd_from_text_params
    assert obj.to_tyd() == ans
