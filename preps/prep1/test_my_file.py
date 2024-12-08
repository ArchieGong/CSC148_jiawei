from my_file import foo

def test_my_first_test():
    expected = 'Pass'
    actual=foo(50)
    assert expected == actual, "50 should pass"

if __name__ == '__main__':
    import pytest
    pytest.main()

