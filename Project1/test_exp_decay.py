from exp_decay import ExponentialDecay


def test_exp_decay():
    """Tests the call method in ExponentialDecay."""
    decay_model = ExponentialDecay(0.4)
    computed = decay_model(0, 3.2)
    expected = -1.28
    assert abs(expected - computed) < 1e-14
