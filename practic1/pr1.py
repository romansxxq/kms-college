"""
Практичне заняття №1. Системи числення і машинне представлення даних.
Варіант 8: N=25, F=0.85, A=55, B=10, C=5.75
"""
import struct
 
 
def int_to_base(n: int, base: int) -> str:
    """Переведення цілого числа в систему числення з основою 2..16 (ділення на основу)."""
    if n == 0:
        return "0"
    digits = "0123456789ABCDEF"
    sign = "-" if n < 0 else ""
    n = abs(n)
    out = ""
    while n > 0:
        out = digits[n % base] + out
        n //= base
    return sign + out
 
 
def frac_to_base(f: float, base: int, precision: int = 6) -> str:
    """Переведення дробової частини в систему з основою base (множення на основу)."""
    digits = "0123456789ABCDEF"
    out = ""
    frac = f
    for _ in range(precision):
        frac *= base
        d = int(frac)
        out += digits[d]
        frac -= d
    return out
 
 
def twos_complement(n: int, bits: int = 8) -> str:
    """Запис цілого числа (додатного або від'ємного) у додатковому коді розрядністю bits."""
    if n < 0:
        n = (1 << bits) + n
    return format(n, f'0{bits}b')
 
 
def add_twos_complement(a: int, b: int, bits: int = 8):
    """Додавання a+b у додатковому коді; повертає (біти суми, десяткове значення, прапорець переповнення)."""
    mask = (1 << bits) - 1
    a_bits, b_bits = a & mask, b & mask
    sum_bits = (a_bits + b_bits) & mask
    sign_a = (a_bits >> (bits - 1)) & 1
    sign_b = (b_bits >> (bits - 1)) & 1
    sign_sum = (sum_bits >> (bits - 1)) & 1
    # переповнення: доданки одного знака, а сума - протилежного
    overflow = (sign_a == sign_b) and (sign_sum != sign_a)
    signed_result = sum_bits - (1 << bits) if sign_sum else sum_bits
    return format(sum_bits, f'0{bits}b'), signed_result, overflow
 
 
def float_to_ieee754(c: float):
    """Розбір float за форматом IEEE 754 single (32 біти): знак, порядок, мантиса."""
    packed = struct.pack('>f', c)
    bits = ''.join(f'{byte:08b}' for byte in packed)
    return bits, bits[0], bits[1:9], bits[9:]
 
 
def ieee754_to_float(bits: str) -> float:
    """Відновлення числа з 32-бітного запису IEEE 754."""
    n = int(bits, 2)
    return struct.unpack('>f', n.to_bytes(4, 'big'))[0]
 
 
if __name__ == "__main__":
    N, F, A, B, C = 25, 0.85, 55, 10, 5.75
 
    print("переведення N та F")
    print(f"N = {N} -> двійкова: {int_to_base(N, 2)}, "
          f"вісімкова: {int_to_base(N, 8)}, "
          f"шістнадцяткова: {int_to_base(N, 16)}")
    print(f"F = {F} -> двійковий дріб (6 розрядів): 0.{frac_to_base(F, 2, 6)}")
 
    print("\nдодавання в додатковому коді (8 біт)")
    print(f"A = {A} -> {twos_complement(A)}")
    print(f"B = {B} -> {twos_complement(B)}")
    sum_bits, signed_result, overflow = add_twos_complement(A, B)
    print(f"Сума (біти): {sum_bits}")
    print(f"Сума (десяткове): {signed_result}")
    print(f"Переповнення: {overflow}")
 
    print("\nIEEE 754 для C")
    bits, sign, exponent, mantissa = float_to_ieee754(C)
    print(f"C = {C}")
    print(f"32-бітний запис: {bits}")
    print(f"  знак: {sign}")
    print(f"  порядок: {exponent} (десяткове {int(exponent, 2)}, "
          f"справжній степінь {int(exponent, 2) - 127})")
    print(f"  мантиса: {mantissa}")
    restored = ieee754_to_float(bits)
    print(f"Відновлене значення: {restored} (== C: {restored == C})")
    print(f"Hex запис: 0x{int(bits, 2):08X}")
 
    print("\nпохибка дробів")
    a, b, expected = 0.1, 0.2, 0.3
    result = a + b
    print(f"{a} + {b} = {result!r}")
    print(f"{a} + {b} == {expected} -> {result == expected}")
    print(f"Різниця: {result - expected!r}")
