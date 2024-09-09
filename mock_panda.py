class MockPanda:
    def __init__(self):
        pass
    def connect(self):
        print('Mock PANDA connected')
    def close(self):
        print('Mock PANDA closed')
    def health(self):
        return {'uptime': 0, 'voltage': 12.0, 'current': 0}
