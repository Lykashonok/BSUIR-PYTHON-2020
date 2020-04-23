class VectorByVlad:
    vector_values = []

    def __init__(self, initial_vector_values):
        '''List of vector values like [1, 2, 3] for x, y, z axis'''
        self.vector_values = list(initial_vector_values)

    def __repr__(self):
        return 'VBV(' + ', '.join(map(lambda x: str(x), self.vector_values)) + ')'

    def __str__(self):
        return 'VBV(' + ', '.join(map(lambda x: str(x), self.vector_values)) + ')'

    def __add__(self, other):
        if not isinstance(other, VectorByVlad): raise ValueError('Can operate with VectorByVlad vector only')
        return VectorByVlad(list(map(lambda a, b : a + b, self.vector_values, other.vector_values)))

    def __iadd__(self, other):
        if not isinstance(other, VectorByVlad): raise ValueError('Can operate with VectorByVlad vector only')
        self.vector_values = list(map(lambda a, b : a + b, self.vector_values, other.vector_values))
        return self

    def __sub__(self, other):
        if not  isinstance(other, VectorByVlad): raise ValueError('Can operate with VectorByVlad vector only')
        return VectorByVlad(list(map(lambda a, b : a - b, self.vector_values, other.vector_values)))

    def __isub__(self, other):
        if not isinstance(other, VectorByVlad): raise ValueError('Can operate with VectorByVlad vector only')
        self.vector_values = list(map(lambda a, b : a - b, self.vector_values, other.vector_values))
        return self
        
    def __mul__(self, other):
        if isinstance(other, VectorByVlad):
            valuesSumm = 0
            for i in range(len(self.vector_values)):
                valuesSumm += self.vector_values[i] * other.vector_values[i]
            return valuesSumm
        elif type(other) is float or type(other) is int:
            self.vector_values = list(map(lambda a: a * int(other), self.vector_values))
            return self

    def __imul__(self, other):
        if isinstance(other, VectorByVlad): raise ValueError('Can operate with scalars only')
        elif type(other) is float or type(other) is int:
            self.vector_values = list(map(lambda a: a * int(other), self.vector_values))
            return self

    def __abs__(self):
        valuesSumm = 0
        for value in self.vector_values:
            valuesSumm += value**2
        return valuesSumm**(0.5)

    def __bool__(self):
        return len(self.vector_values) != 0

    def __eq__(self, other):
        if isinstance(other, VectorByVlad):
            if len(self.vector_values) != len(other.vector_values): return False
            for i in range(len(self.vector_values)):
                if self.vector_values[i] != other.vector_values[i]: return False
            return True
        else:
            return False
    
    def __getitem__(self, index):
        if type(index) is int:
            if index >= 0 and index < len(self.vector_values):
                return self.vector_values[index]
            else: raise ValueError('Out of range')

    def __setitem__(self, index, value):
        if type(index) is int:
            self.vector_values[index] = value
            return self

    def __neg__(self):
        return VectorByVlad(list(map(lambda a: -a, self.vector_values)))