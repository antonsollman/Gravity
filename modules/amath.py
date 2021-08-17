
# Anton's library of mathematical functions
# Version 0.4.1


pi = 3.1415926535897932384626433832795
tau = pi*2
e = 2.718281828459045


def root(x, r):
    return x**(1/r)


def sqrt(x):
    return root(x, 2)


phi = (sqrt(5)+1)/2


def cbrt(x):
    return root(x, 3)


def aabs(x):
    if x.imag == 0:
        if x < 0:
            return x*-1
        return x
    
    return sqrt(x.real**2+x.imag**2)


def sgn(x):
    if x == 0:
        return float(str(x.real).replace('0','1',1))
    
    sign = x/aabs(x)
    
    return sign


def trunc(x):
    return int(x)


def floor(x):
    if x < 0 and x != trunc(x):
        return trunc(x)-1
    
    else:
        return trunc(x)


def ceil(x):
    if x > floor(x):
        return floor(x)+1
    
    else:
        return trunc(x)


def mod(x, n):
    remainder = x-n*floor(x/n)

    return remainder


def around(x, n=0):
    m = 10**n
    
    if x > 0:
        if x*m-floor(x*m) >= 0.5:
            return ceil(x*m)/m
        
        return floor(x*m)/m
    
    else:
        if x*m-floor(x*m) <= 0.5:
            return floor(x*m)/m
        
        return ceil(x*m)/m


# Factorial
def fact(n):
    if n >= 0 and isinstance(n, int):
        product = 1
        
        for k in range(2,n+1):
            product *= k
            
        return product

    print("subfact input not integer >= 0")
    return False


# Derangement
def subfact(n):
    if n >= 0 and isinstance(n, int):
        if n >= 1:
            return floor(fact(n)/e+1/2)
        return 1

    print("subfact input not integer >= 0")
    return False


# Combinations
def choose(n, k):
    if 0 < k <= n and isinstance(k, int):
        
        combinations = int(fact(n)/(fact(k)*fact(n-k)))

        return combinations
    
    return False


# Permutations
def perm(n, k):
    if 0 < k <= n and isinstance(n, int):

        permutations = int(fact(n)/fact(n-k))

        return permutations

    return False


# Degrees to radians
def rad(deg):
    rad = deg*pi/180
    return rad


# Radians to degrees
def deg(rad):
    deg = rad*180/pi
    return deg


# Sine function
def sin(x):
    x = mod(x,tau)
    
    sign = -1
    series_sum = 0
    
    for n in range(32):
        sign *= -1
        series_sum += sign*x**(2*n+1)/fact(2*n+1)

    return series_sum


# Cosine function
def cos(x):
    return sin(x+pi/2)


# Tangent function
def tan(x):
    cosx = cos(x)
    if cosx == 0:
        return None
    
    return sin(x)/cosx


# First degree equation (ax+b=0)
def firstdegree(a, b):
    if a == 0:
        return False
        
    x = -b/a

    return x


# Quadratic equation (ax^2+bx+c=0)
def quadratic(a, b, c):
    if a == 0:
        return firstdegree(b, c)
    
    x1 = (-b-sqrt(b**2-4*a*c))/(2*a)
    x2 = (-b+sqrt(b**2-4*a*c))/(2*a)
    
    return around(x1.real,14)+around(x1.imag,14)*1j, around(x2.real,14)+around(x2.imag,14)*1j


# Cubic equation (ax^3+bx^2+cx+d=0)
def cubic(a, b, c, d):
    if a == 0:
        return quadratic(b, c, d)

    if (b == 0 or c == 0) and (a != 0):
        sgn_d = sgn(d)
        if sgn_d == -1:
            d *= sgn_d

        # Doesn't really work...

        x1 = around((-cbrt(d/a*sgn_d)).real*sgn_d, 14)-around((-cbrt(d/a*sgn_d)).imag*sgn_d, 14)*1j
        x2 = around(cbrt(-d/a).real,14)*sgn_d+around(cbrt(-d/a).imag,14)*1j
        x3 = x1.real-x1.imag*1j #-around((x1**2).real, 14)*sgn_d-around((x1**2).imag, 14)*1j*sgn_d
        
        return x1, x2, x3
        
        
    D0 = b**2-3*a*c
    D1 = 2*b**3-9*a*b*c+27*a**2*d

    s = (-1+sqrt(-3))/2

    C = cbrt((D1-sqrt(D1**2-4*D0**3))/2)

    x1 = -(b+C+D0/C)/(3*a)
    x2 = -(b+s*C+D0/(s*C))/(3*a)
    x3 = -(b+s**2*C+D0/(s**2*C))/(3*a)

    return x1, x2, x3


# Sorts a given list lowest to highest.
def sort(array):
    length = len(array)

    if length > 1:
        mid = length//2

        L = array[:mid]
        R = array[mid:]

        sort(L)
        sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                array[k] = L[i]
                i += 1
            else:
                array[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            array[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            array[k] = R[j]
            j += 1
            k += 1

        return array

def hypot(p):
    square_sum = 0
    for d in p:
        square_sum += d**2

    return sqrt(square_sum)

def dist3(p, q):
    return sqrt((p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2)

# Distance between two points in any given number of dimensions.
# Input numbers or lists/tuples.
def dist(p, q):
    if (isinstance(p, tuple) or isinstance(p, list)) and (isinstance(q, tuple) or isinstance(q, list)) and len(p) == len(q):
        dimensions = len(p)
        square_sum = 0
    
        for dimension in range(dimensions):
            dimension_distance = p[dimension]-q[dimension]
            square_sum += dimension_distance**2

        distance = sqrt(square_sum)
        return distance
    
    elif (isinstance(p, float) or isinstance(p, int)) and (isinstance(q, float) or isinstance(q, int)):
        return aabs(p-q)

    print("dist error. check type and number of dimensions.")
    return False


# Standard deviation
def stdev(input_list):
    if isinstance(input_list, list):
        number_list = []
        
        for i in input_list:
            if isinstance(i, float) or isinstance(i, int):
                
                number_list.append(i)

        number_list = sort(number_list)
        
        n = len(number_list)
        average = sum(number_list)/n
        s_nl = 0
        
        for k in number_list:
            s_nl += (k-average)**2
            
        stdev = sqrt(s_nl/(n))

        print(number_list)
        
        return stdev

    print("stdev error. input not list.")


# Order of magnitude, returns n in m*10**n
def magnitude_order(x):
    x = aabs(x)
    n = 0
    if 0 < x <= 1:
        while x < 1:
            x *= 10
            n -= 1
            
        return n
    
    if x > 1:
        while x >= 1:
            x /= 10
            n += 1
            
        return n-1
    
    return False

# Power of ten coefficient, returns m in m*10**n
def potco(x):
    return x/10**magnitude_order(x)

# Scientific notation, returns tuple (m, n) in m*10**n
def scientific(x):
    return potco(x), magnitude_order(x)

# Natural logarithm for low values of x
def ln0(x):
    s = 0
    for k in range(64):
        s += ((x-1)/(x+1))**(2*k+1)/(2*k+1)
    return 2*s


# Natural logarithm for any positive value of x
ln10 = ln0(2)+ln0(5)
def ln(x):
    if x == e:
        return 1.0
    
    if x < 0:
        sign_x = sgn(x)
        x = aabs(x)
        
        n = magnitude_order(x)
        m = x/10**n
        result = ln0(m)+n*ln10

        return result+pi*1j
        
    if x > 0:
        n = magnitude_order(x)
        m = x/10**n
        result = ln0(m)+n*ln10
        
        return result
    
    print("logarithm error. x possibly 0")

# Any logarithm for any positive value of x
def log(x, base=e):
    if (isinstance(x, float) or isinstance(x, int)) and base > 0:
        return ln(x)/ln(base)
    
    print(f"logarithm error. type(x)={type(x)}, type(base)={type(base)}")


### Arctangent for bigger numbers
##def atan1(x):
##    
##    if x >= 1:
##        sign = 1
##        series_sum = 0
##
##        for n in range(32):
##            sign *= -1
##            series_sum -= sign/((2*n+1)*(x**(2*n+1)))
##
##        return pi/2 - series_sum
##            
##
### Flawed arctangent
##def atan2(x):
##    sign_x = sgn(x)
##    x = aabs(x)
##    
##    if aabs(x) > 1:
##        return sign_x*atan1(x)
##    
##    if 0 < x <= 1:
##        return sign_x*(pi/2-atan1(1/x))
##
##
### Kind of works in first quadrant
##def polar(x):
##    m = aabs(x)
##    if x.imag >= x.real:
##        theta = atan2(x.imag/x.real)
##    if x.imag < x.real:
##        theta = pi/2-atan2(x.real/x.imag)
##
##    return m, theta
