# Simplifying-Polynomial-Equations
The problem my program will try to solve is simplifying polynomial equations into standard form. It will take any number of polynomial equations being 
multiplied and/or added/subtracted as input. Below, there will be a generic equitation of what this program will take as input and output. This program 
will also account for common conventions in writing polynomial equations such as: omitting a term if its coefficient is 0, omitting a coefficient if it is 1, 
or a term only showing the coefficient if the x is of power 0. The program will achieve this by breaking the problem into two steps. The first step is 
transcribing the equation from a string into a series of lists on lists. Each level of lists will signify different operations. The upmost level will 
represent addition and subtraction. The next level will represent multiplication. The final level will represent the exponent on each polynomial. 
The second step will be doing the math to simplify into standard form. The program will achieve this by simplifying the bottom most lists and work its way 
up until the equation is fully simplified into standard form.

Example:
    Generic Input:
        (a1x^n1 + a2x^n1-1 + … + a3x + a4)^p1 … (b1x^n2 + b2x^n2-1 + … + b3x + b4)^p2 + … + (c1x^n3 + c2x^n3-1 + … + c3x + c4)^p3 … (d1x^n4 + d2x^n4-1 + … + d3x + d4)^p4
    Generic Output:
        g1x^n + g2x^n-1 + … + g3x + g4
