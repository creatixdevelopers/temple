from app.tasks import send_error_email, send_email


def test_send_error_email():
    assert send_error_email('a', 'b') is True


def test_send_email():
    assert send_email('a', 'b', 'c', 'd') is False
    assert send_email('a', 'b', 'c', "['test@test.com']") is False
    assert send_email(['test@test.com'], 'a', 'b', 'c') is True
