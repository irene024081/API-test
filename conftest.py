def pytest_addoption(parser):
    parser.addini("base_url", help = "the host url",default="https://0708.cloudx.safeuem.com/")
    parser.addini("username", help = "the username for testing",default="administrator")
    parser.addini("password", help = "the password for testing",default="Safeuem0420")
    parser.addini("android_group_password", help = "the password for android group",default="ailingapi")
    parser.addini("group_id", help = "the group id for testing",default="4fd33b72-b339-4d50-974a-8ba79bce218f")