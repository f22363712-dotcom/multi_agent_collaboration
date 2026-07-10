def login(username, password):
    if username == "admin" and password == "secret":
        return True, "Login successful"
    return False, "Invalid credentials"
