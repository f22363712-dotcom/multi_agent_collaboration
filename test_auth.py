from auth import login

def test_login_success():
    success, msg = login("admin", "secret")
    assert success is True
    assert msg == "Login successful"

def test_login_fail():
    success, msg = login("user", "pass")
    assert success is False
    assert msg == "Invalid credentials"

if __name__ == "__main__":
    test_login_success()
    test_login_fail()
    print("All mock auth tests passed!")
