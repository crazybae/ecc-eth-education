# 'E: y^2 = x^3 + 20*x + 8 (mod 23)  -->  #E/F23: 31

import sys
from tinyec.ec import SubGroup, Curve, Point, mod_inv


def print_curve_params(curve):
    print(f'curve name:       {curve.name}')
    print(f'curve equation:   y^2 = x^3 + {curve.a}x + {curve.b} (mod p)')
    print(f'base field order: {curve.field.p}')
    print(f'EC group order:   {curve.field.n}')
    print(f'Generator.x:      {curve.g.x}')
    print(f'Generator.y:      {curve.g.y}')

def check_on_curve(curve, x, y):
    if curve.on_curve(x, y):
        print(f'({x},{y}) is on the curve')
    else:
        print(f'({x},{y}) is NOT on the curve')

def print_generated_group_elements(curve):
    print(f'Generator G is ({curve.g.x}, {curve.g.y})')
    for i in range(1, 40):
        P = i * curve.g
        print(f'{i} * G = ({P.x}, {P.y})')

def print_generated_group_elements_with_tangent(curve):
    for i in range(1, 40):
        P = i * curve.g
        tgt = "Undefined"
        if P.x is not None:
            # tangent = (3*x^2+a)/2y  (mod p)
            tgt = ((3*P.x*P.x + curve.a) * mod_inv(2*P.y, curve.field.p) ) % curve.field.p
        print(f'{i} * G = ({P.x}, {P.y}), its tangent is {tgt}')

def main():

    if len(sys.argv) != 2:
        print("\nUsage: $ python ecpractice.py (params | check | generate)\n")
        return

    basefield = SubGroup(p=23, g=(16, 13), n=31, h=1)
    curve = Curve(a=20, b=8, field=basefield, name='Test Curve')

    option = sys.argv[1]
    if option == "params":
        # print curve params
        print_curve_params(curve)

    elif option == "check":
        # check points
        check_on_curve(curve, 5,5)
        check_on_curve(curve, 13,2)

    elif option == "generate":
        # generate EC group by a generator
        print_generated_group_elements_with_tangent(curve)

    else:
        print("\nUsage: $ python ecpractice.py (params | check | generate)\n")

if __name__ == "__main__":
    main()
