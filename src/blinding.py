import random
from math import gcd
from src.defender import Defender


# chatgpt helper function
def generate_coprime_to_modulo(modulo):
    """
    Generates a random integer e such that 1 < e < N and gcd(e, N) = 1.
    :param modulo: RSA public modulus
    :return: random coprime integer e
    """
    e = random.randint(2, modulo - 1)
    while gcd(e, modulo) != 1:
        e = random.randint(2, modulo - 1)
    return e


# my fast exponent implementation
def fast_exponent(base, exp, mod):
    trace = []
    if exp == 0:
        trace.append(random.uniform(0, 0.2))
        return 1
    if exp == 1:
        trace.append(random.uniform(0.1, 0.3))
        return base % mod
    binary_exponent = bin(exp)[3:]
    step = base
    for i in binary_exponent:
        step = step**2 % mod
        trace.append(random.uniform(0.6, 0.8))
        if i == "1":
            trace.append(random.uniform(0, 0.2))
            step = step * base % mod
            trace.append(random.uniform(0.8, 1))
    return step, trace


# fast exp with blinding
def fast_exponent_blinding(base, exp, mod, public_exp):
    trace = []
    v_f, v_i = generate_blinding_var(mod, public_exp)
    base = base * v_i % mod
    if exp == 0:
        trace.append(random.uniform(0, 0.2))
        return 1
    if exp == 1:
        trace.append(random.uniform(0.1, 0.3))
        return base % mod
    binary_exponent = bin(exp)[3:]
    step = base
    for i in binary_exponent:
        step = step**2 % mod
        trace.append(random.uniform(0.6, 0.8))
        if i == "1":
            trace.append(random.uniform(0, 0.2))
            step = step * base % mod
            trace.append(random.uniform(0.8, 1))
    step = step * v_f % mod
    return step, trace


def generate_blinding_var(mod, public_exp):
    # choose random v_i that is coprime with public exponent
    v_f = generate_coprime_to_modulo(mod)
    v_i = pow(v_f, - public_exp, mod)
    return v_f, v_i


def montgomery_ladder_bitwise(base, exp, modulus):
    """
    Calculates "base ** exp mod modulus" using the montgomery method
    :param base: integer base
    :param exp: integer exponent
    :param modulus: integer modulo
    :return: base^exp mod modulus
    """
    r_0 = 1
    r_1 = base
    exp_binary = bin(exp)[2:]
    # exp_binary = exp_binary[::-1]
    for bit in exp_binary:
        mask = -(bit == '0')    # 0 if bit '1' and -1 if bit '0'.
        r_0_old = r_0
        r_0 = ((r_0 ** 2 % modulus) & (mask)) | ((r_0 * r_1 % modulus) & (~mask))
        r_1 = ((r_0_old * r_1 % modulus) & (mask)) | ((r_1 ** 2 % modulus) & (~mask))
    return r_0


def montgomery_bitwise_w_blinding(base, exp, modulus, public_exp):
    """
    Calculates "base ** exp mod modulus" using the montgomery method and uses blinding.
    :param base: integer base
    :param exp: integer private exponent
    :param modulus: integer modulo
    :param public_exp: integer public exponent
    :return: base^exp mod modulus
    """
    v_f, v_i = generate_blinding_var(modulus, public_exp)
    base = base * v_i % modulus
    r_0 = 1
    r_1 = base
    exp_binary = bin(exp)[2:]
    # exp_binary = exp_binary[::-1]
    for bit in exp_binary:
        mask = -(bit == '0')    # 0 if bit '1' and -1 if bit '0'.
        r_0_old = r_0
        r_0 = ((r_0 ** 2 % modulus) & (mask)) | ((r_0 * r_1 % modulus) & (~mask))
        r_1 = ((r_0_old * r_1 % modulus) & (mask)) | ((r_1 ** 2 % modulus) & (~mask))
    r_0 = r_0 * v_f % modulus
    return r_0


if __name__ == "__main__":
    a = Defender()
    result, trace = fast_exponent(4288743, 8234214, 43)
    print(result)
    # result, trace = fast_exponent_blinding(4288743, 8234214, 43)
    result, trace = fast_exponent_blinding(4288743, a._e, a.n, a.d)
    print(result)
    print(pow(4288743, a._e, a.n))

    print("montgomery with blinding:")
    print(montgomery_bitwise_w_blinding(4288743, a._e, a.n, a.d))

