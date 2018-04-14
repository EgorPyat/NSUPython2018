#!/usr/bin/python3

class Vector:
    """Linear algebra vector
    Attributes
    ----------
    elems : tuple of numbers - int, float
    """
    def __init__(self, *args):
        """Vector constructor
        Parameters
        ----------
        args : tuple of numbers
        Returns
        -------
        new instance of Vector
        Raises
        ------
        TypeError
            if args are null
        """
        if len(args) == 0:
            raise TypeError("Zero length vector")
        elem_type = int
        for item in args:
            if type(item) == float:
                if elem_type == int:
                    elem_type = float
            elif type(item) == complex:
                if elem_type == float:
                    elem_type = complex
            elif type(item) != int:
                raise TypeError('bad type')
        self.elems = list([elem_type(item) for val in args])

    def __add__(self, vec):
        """Vectors addition
        Parameters
        ----------
        vec : Vector
        Returns
        -------
        Vector
            sum of vectors elements in new instance of vector
        Raises
        ------
        ValueError
            if vectors' lengths are different
        """
        if len(self) != len(vec):
            raise ValueError("vectors must have the same length")
        return Vector(*(x + y for x, y in zip(self, vec)))

    def __sub__(self, vec):
        """Vectors substruction
        Parameters
        ----------
        vec : Vector
        Returns
        -------
        Vector
            sub of vectors elements in new instance of vector
        Raises
        ------
        ValueError
            if vectors' lengths are different
        """
        if len(self) != len(vec):
            raise ValueError("vectors must have the same length")
        return Vector(*(x - y for x, y in zip(self, vec)))

    def __mul__(self, vec):
        """Vectors multiplication
        Parameters
        ----------
        vec : Vector
        Returns
        -------
        Vector or int
            mul on scalar in new instance of Vector or scalar mul of vectors elements
        Raises
        ------
        ValueError
            if vectors' lengths are different
        """
        if(type(self) == type(vec)):
            if len(self) != len(vec):
                raise ValueError("vectors must have the same length")
            return sum(x * y for x, y in zip(self, vec))
        elif type(vec) is int or float:
            return Vector(*(x * vec for x in self.elems))

    def __rmul__(self, vec):
        """Vectors multiplication in case multiplicator is on right
        Parameters
        ----------
        vec : Vector
        Returns
        -------
        Vector
            mul of vectors elements in new instance of vector
        Raises
        ------
        TypeError
            if vectors' lengths are different
        """
        return self.__mul__(vec)

    def __truediv__(self, vec):
        """Vector true divison on number
        Parameters
        ----------
        vec : Vector
        Returns
        -------
        Vector
            elements are divided on number in new instance of vector
        Raises
        ------
        TypeError
            if divisor is not number
        """
        if type(vec) is int or float:
            return Vector(*(x / vec for x in self.elems))
        else:
            raise TypeError("invalid argument value")

    def __floordiv__(self, vec):
        """Vector floor divison on number
        Parameters
        ----------
        vec : Vector
        Returns
        -------
        Vector
            elements are divided on number in new instance of vector
        Raises
        ------
        TypeError
            if divisor is not number
        """
        if type(vec) is int or float:
            return Vector(*(x // vec for x in self.elems))
        else:
            raise TypeError("invalid argument value")

    def __eq__(self, vec):
        """Vectors' equation
        Parameters
        ----------
        vec : Vector
        Returns
        -------
        boolean
            false if Vectors hve different elements or vec is not a Vector
        """
        if(type(self) != type(vec)):
            return False
        return self.elems == vec.elems

    def __getitem__(self, index):
        """Get Vector element by index
        Parameters
        ----------
        index : int
        Returns
        -------
        int or float
            vector element
        Raises
        ------
        IndexError
            if index is out of range
        """
        if len(self) - 1 < index or index < -len(self):
            raise IndexError("vector index out of range")
        return self.elems[index]

    def __repr__(self):
        """String representation of Vector
        Returns
        -----------
        str: string
            string representation of Vector
        """
        return str(self.elems)

    def __len__(self):
        """Number of elements in vector
        Returns
        -------
        int
            number of elements in vector
        """
        return len(self.elems)

a = Vector(1, -10, -1, 0, 2)
b = Vector(2, 3, 2, 32, 's')
print("a ", a)
print("b ", b)
print(b + a)
print(b * a)
print(b - a)
print(a / 8)
print(a // 8)
print(a == b)
print(a == a)
