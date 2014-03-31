def override(interfaceClass):
    def overrider(method):
        assert(method.__name__ in dir(interfaceClass))
        return method
    return overrider
