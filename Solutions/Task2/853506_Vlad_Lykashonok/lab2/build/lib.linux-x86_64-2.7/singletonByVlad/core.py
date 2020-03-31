from vectorByVlad.core import VectorByVlad
# singleton class
class VectorScalerByVlad(object):
    instance = None
    _scaleFactor_ = 1
    def __new__(self):
        if not self.instance:
            self.instance = super(VectorScalerByVlad, self).__new__(self)
        return self.instance
    def scale(self, vector):
        '''Scale vector by scaleFactor inside singleton class'''
        if isinstance(vector, VectorByVlad):
            for i in range(len(vector.vector_values)):
                vector[i] *= self._scaleFactor_
        else:
            raise ValueError('can scale only vector')
# singleton decorator
def SingletonDecoratorByVlad(SomeClass): 
    instances = {}
    def getInstance(*args, **kwargs):
        if SomeClass not in instances:
            instances[SomeClass] = SomeClass(*args, **kwargs)
        return instances[SomeClass]
    return getInstance

#example of class
@SingletonDecoratorByVlad
class VectorScalerByVlad2(object):
    instance = None
    _scaleFactor_ = 1
    def scale(self, vector):
        '''Scale vector by scaleFactor inside singleton class'''
        if isinstance(vector, VectorByVlad):
            for i in range(len(vector.vector_values)):
                vector[i] *= self._scaleFactor_
        else:
            raise ValueError('can scale only vector')

def checkWork():
    print('---Singleton decorator---')
    vector = VectorByVlad([1, 2, 3])
    scaler = VectorScalerByVlad2()
    scaler._scaleFactor_ = 2
    print('vector -', vector)
    scaler.scale(vector)
    print('after creating one instance of singleton class-', vector)
    # creating scaler2
    scaler2 = VectorScalerByVlad2()
    scaler2._scaleFactor_ = 100
    # but using scaler
    scaler.scale(vector)
    print('after creating another instance of singleton class', vector)

    print('---Singleton class---')
    vector = VectorByVlad([1, 2, 3])
    scaler = VectorScalerByVlad()
    scaler._scaleFactor_ = 2
    print('vector -', vector)
    scaler.scale(vector)
    print('after creating one instance of singleton class-', vector)
    # creating scaler2
    scaler2 = VectorScalerByVlad()
    scaler2._scaleFactor_ = 100
    # but using scaler
    scaler.scale(vector)
    print('after creating another instance of singleton class', vector)