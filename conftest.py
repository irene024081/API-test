def pytest_addoption(parser):
    parser.addini("base_url", help = "the host url",default="https://0708.cloudx.safeuem.com/")
    parser.addini("username", help = "the username for testing",default="administrator")
    parser.addini("password", help = "the password for testing",default="Safeuem0420")
    parser.addini("android_group_password", help = "the password for android group",default="ailingapi")
    parser.addini("group_id", help = "the group id for testing",default="1b01ad74-0859-4c93-8c7a-93a21607fad7")
    parser.addini("device_token", help = "the device id for testing",default="8d9579fe-3247-4ccd-ab2b-ea641a14c9e7")
    parser.addini("group_id2", help = "the group id for testing",default="cfec0772-d0d7-472b-9642-99b458e65ce2")
    parser.addini("template", help = "the template id for testing",default="7c8ceacc-a18d-456b-ad4d-e8fb71ec3bb6") 
    parser.addini("image_path", help = "the image path for testing",default='/Users/ailingwang/Library/Mobile Documents/com~apple~CloudDocs/SafeUEM/测试用文件/1200px-SNice.svg.png')