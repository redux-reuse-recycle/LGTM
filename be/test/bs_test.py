from be.test import bs_main


def test_main():
    map = bs_main.run()
    assert len(map.keys()) == 20
