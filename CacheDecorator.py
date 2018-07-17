from time import time

class Cache:

    # @param timeToLive: in seconds
    # @param retrievalLimit: maximum number of retrieving the value from cache storage per unique argument
    def __init__(self, timeToLive, retrievalLimit):
        self.cacheStorage = {}
        self.timeToLive = timeToLive
        self.retrievalLimit = retrievalLimit
    
    def __call__(self, func):

        def wrappingFunction(*params):
            updateCacheItem = False

            if params in self.cacheStorage:
                if time() < self.cacheStorage[params]['expirationLimit'] and self.cacheStorage[params]['retrievalCounter'] < self.retrievalLimit:
                    self.cacheStorage[params]['retrievalCounter'] += 1
                else:
                    updateCacheItem = True
            else:
                self.cacheStorage[params] = {}
                updateCacheItem = True
            
            if updateCacheItem:
                self.cacheStorage[params]['expirationLimit'] = time() + self.timeToLive
                self.cacheStorage[params]['retrievalCounter'] = 0  # first call is not considered as cache fetching; otherwise change to 1
                self.cacheStorage[params]['value'] = func(params)
            
            return self.cacheStorage[params]['value']
        
        return wrappingFunction


@Cache(300, 10)
def getMyTime(*someParams):
    return time()

'''for i in range(13):
    print( getMyTime('a', 'b') )
    sleep(1)
    print( getMyTime(123) )'''
