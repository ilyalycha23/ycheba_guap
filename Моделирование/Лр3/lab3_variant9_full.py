# -*- coding: utf-8 -*-
"""
Лабораторная работа №2 (Лр3): Моделирование непрерывной и дискретной СВ
Вариант 9: + Биномиальное распределение
Пять видов распределений на основе БСВ (базовой случайной величины).
"""
import sys
import io
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except (AttributeError, OSError):
    pass

import math
import random
import numpy as np

# Параметры для всех распределений
N = 2000       # объём выборки
random.seed(42)
np.random.seed(42)

# ========== 1. ЭКСПОНЕНЦИАЛЬНОЕ (формула 2.5) ==========
# x = -ln(z) / lambda; M = 1/lambda, D = 1/lambda^2
LAMBDA = 1.0

def gen_exponential():
    z = random.random()
    return -math.log(z) / LAMBDA

sample_exp = [gen_exponential() for _ in range(N)]
M_exp_theor = 1 / LAMBDA
D_exp_theor = 1 / (LAMBDA ** 2)
M_exp_emp = sum(sample_exp) / N
D_exp_emp = sum((x - M_exp_emp)**2 for x in sample_exp) / (N - 1)

# ========== 2. РАВНОМЕРНОЕ (формула 2.7) ==========
# x = A + z*(B-A); M = (A+B)/2, D = (B-A)^2/12
A, B = 0, 5

def gen_uniform():
    z = random.random()
    return A + z * (B - A)

sample_unif = [gen_uniform() for _ in range(N)]
M_unif_theor = (A + B) / 2
D_unif_theor = (B - A)**2 / 12
M_unif_emp = sum(sample_unif) / N
D_unif_emp = sum((x - M_unif_emp)**2 for x in sample_unif) / (N - 1)

# ========== 3. ЭРЛАНГА порядка K (формула 2.11) ==========
# x = -(1/lambda) * sum(ln(zi)); M = k/lambda, D = k/lambda^2
K_ERLANG = 3
LAMBDA_ERL = 1.0

def gen_erlang():
    s = 1.0
    for _ in range(K_ERLANG):
        z = random.random()
        s *= z
    return -math.log(s) / LAMBDA_ERL if s > 0 else 0

sample_erlang = [gen_erlang() for _ in range(N)]
M_erl_theor = K_ERLANG / LAMBDA_ERL
D_erl_theor = K_ERLANG / (LAMBDA_ERL ** 2)
M_erl_emp = sum(sample_erlang) / N
D_erl_emp = sum((x - M_erl_emp)**2 for x in sample_erlang) / (N - 1)

# ========== 4. НОРМАЛЬНОЕ (формула 2.14, Бокс-Мюллер) ==========
# x1 = sqrt(-2*ln(z1))*sin(2*pi*z2), x2 = sqrt(-2*ln(z1))*cos(2*pi*z2)
# M = m, D = sigma^2
M_NORM, SIGMA_NORM = 0, 1.0

def gen_normal():
    z1, z2 = random.random(), random.random()
    x_std = math.sqrt(-2 * math.log(z1)) * math.sin(2 * math.pi * z2)
    return M_NORM + SIGMA_NORM * x_std

sample_norm = [gen_normal() for _ in range(N)]
M_norm_theor = M_NORM
D_norm_theor = SIGMA_NORM ** 2
M_norm_emp = sum(sample_norm) / N
D_norm_emp = sum((x - M_norm_emp)**2 for x in sample_norm) / (N - 1)

# ========== 5. БИНОМИАЛЬНОЕ (вариант 9) ==========
n_binom, p_binom = 9, 0.45

def gen_binomial():
    count = 0
    for _ in range(n_binom):
        if random.random() < p_binom:
            count += 1
    return count

sample_binom = [gen_binomial() for _ in range(N)]
M_binom_theor = n_binom * p_binom
D_binom_theor = n_binom * p_binom * (1 - p_binom)
M_binom_emp = sum(sample_binom) / N
D_binom_emp = sum((x - M_binom_emp)**2 for x in sample_binom) / (N - 1)

# ========== ВЫВОД СРАВНЕНИЯ M и D ==========
print("=" * 70)
print("ЛАБОРАТОРНАЯ РАБОТА №2: МОДЕЛИРОВАНИЕ НЕПРЕРЫВНОЙ СЛУЧАЙНОЙ ВЕЛИЧИНЫ")
print("Вариант 9 (Биномиальное) + 4 стандартных распределения")
print("=" * 70)

results = [
    ("Экспоненциальное (lambda=1)", M_exp_theor, D_exp_theor, M_exp_emp, D_exp_emp),
    ("Равномерное [0,5]", M_unif_theor, D_unif_theor, M_unif_emp, D_unif_emp),
    ("Эрланга (K=3, lambda=1)", M_erl_theor, D_erl_theor, M_erl_emp, D_erl_emp),
    ("Нормальное (m=0, sigma=1)", M_norm_theor, D_norm_theor, M_norm_emp, D_norm_emp),
    ("Биномиальное (n=9, p=0.45)", M_binom_theor, D_binom_theor, M_binom_emp, D_binom_emp),
]
print("\nСравнение M и D (теор. vs эмп.):")
print("-" * 70)
for name, Mt, Dt, Me, De in results:
    print(f"  {name}")
    print(f"    M: теор={Mt:.4f}  эмп={Me:.4f}  |dM|={abs(Mt-Me):.4f}")
    print(f"    D: теор={Dt:.4f}  эмп={De:.4f}  |dD|={abs(Dt-De):.4f}")
    print()

# ========== 5 ГРАФИКОВ (гистограммы) ==========
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.flatten()

    # 1. Экспоненциальное
    ax = axes[0]
    ax.hist(sample_exp, bins=40, density=True, alpha=0.7, color='steelblue', edgecolor='black')
    x_plot = np.linspace(0, max(sample_exp), 200)
    ax.plot(x_plot, LAMBDA * np.exp(-LAMBDA * x_plot), 'r-', lw=2, label='Теор. f(x)')
    ax.set_title('1. Экспоненциальное (формула 2.5)')
    ax.set_xlabel('x')
    ax.legend()
    ax.grid(alpha=0.3)

    # 2. Равномерное
    ax = axes[1]
    ax.hist(sample_unif, bins=30, density=True, alpha=0.7, color='steelblue', edgecolor='black')
    ax.axhline(1/(B-A), color='r', linestyle='-', lw=2, label=f'Теор. 1/(B-A)={1/(B-A):.2f}')
    ax.set_title('2. Равномерное (формула 2.7)')
    ax.set_xlabel('x')
    ax.legend()
    ax.grid(alpha=0.3)

    # 3. Эрланга
    ax = axes[2]
    ax.hist(sample_erlang, bins=40, density=True, alpha=0.7, color='steelblue', edgecolor='black')
    # Теоретическая плотность Эрланга
    from scipy import stats as sps
    x_erl = np.linspace(0, max(sample_erlang), 200)
    ax.plot(x_erl, sps.erlang.pdf(x_erl, K_ERLANG, scale=1/LAMBDA_ERL), 'r-', lw=2, label='Теор. f(x)')
    ax.set_title('3. Эрланга порядка K (формула 2.11)')
    ax.set_xlabel('x')
    ax.legend()
    ax.grid(alpha=0.3)

    # 4. Нормальное
    ax = axes[3]
    ax.hist(sample_norm, bins=40, density=True, alpha=0.7, color='steelblue', edgecolor='black')
    x_norm = np.linspace(min(sample_norm), max(sample_norm), 200)
    ax.plot(x_norm, (1/(SIGMA_NORM*np.sqrt(2*np.pi)))*np.exp(-0.5*((x_norm-M_NORM)/SIGMA_NORM)**2), 'r-', lw=2, label='Теор. f(x)')
    ax.set_title('4. Нормальное (формула 2.14, Бокс-Мюллер)')
    ax.set_xlabel('x')
    ax.legend()
    ax.grid(alpha=0.3)

    # 5. Биномиальное (вариант 9)
    ax = axes[4]
    bins_binom = np.arange(-0.5, n_binom + 1.5, 1)
    ax.hist(sample_binom, bins=bins_binom, density=True, alpha=0.7, color='steelblue', edgecolor='black', label='Эмп.')
    k_vals = list(range(n_binom + 1))
    p_theor = [math.comb(n_binom, k) * (p_binom**k) * ((1-p_binom)**(n_binom-k)) for k in k_vals]
    ax.bar(k_vals, p_theor, width=0.4, alpha=0.6, color='coral', label='Теор. P(X=k)')
    ax.set_title('5. Биномиальное (вариант 9)')
    ax.set_xlabel('k')
    ax.legend()
    ax.grid(alpha=0.3)

    # Убираем 6-й пустой subplot
    fig.delaxes(axes[5])

    plt.tight_layout()
    plt.savefig('lab3_variant9_5graphs.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Графики сохранены в lab3_variant9_5graphs.png")
except ImportError as e:
    # Без scipy - строим Эрланг без теоретической кривой
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.flatten()

    ax = axes[0]
    ax.hist(sample_exp, bins=40, density=True, alpha=0.7, color='steelblue', edgecolor='black')
    x_plot = np.linspace(0, max(sample_exp), 200)
    ax.plot(x_plot, LAMBDA * np.exp(-LAMBDA * x_plot), 'r-', lw=2, label='Теор. f(x)')
    ax.set_title('1. Экспоненциальное (формула 2.5)')
    ax.set_xlabel('x')
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[1]
    ax.hist(sample_unif, bins=30, density=True, alpha=0.7, color='steelblue', edgecolor='black')
    ax.axhline(1/(B-A), color='r', linestyle='-', lw=2, label=f'Теор. 1/(B-A)={1/(B-A):.2f}')
    ax.set_title('2. Равномерное (формула 2.7)')
    ax.set_xlabel('x')
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[2]
    ax.hist(sample_erlang, bins=40, density=True, alpha=0.7, color='steelblue', edgecolor='black')
    ax.set_title('3. Эрланга порядка K (формула 2.11)')
    ax.set_xlabel('x')
    ax.grid(alpha=0.3)

    ax = axes[3]
    ax.hist(sample_norm, bins=40, density=True, alpha=0.7, color='steelblue', edgecolor='black')
    x_norm = np.linspace(min(sample_norm), max(sample_norm), 200)
    ax.plot(x_norm, (1/(SIGMA_NORM*np.sqrt(2*np.pi)))*np.exp(-0.5*((x_norm-M_NORM)/SIGMA_NORM)**2), 'r-', lw=2, label='Теор. f(x)')
    ax.set_title('4. Нормальное (формула 2.14)')
    ax.set_xlabel('x')
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[4]
    bins_binom = np.arange(-0.5, n_binom + 1.5, 1)
    ax.hist(sample_binom, bins=bins_binom, density=True, alpha=0.7, color='steelblue', edgecolor='black', label='Эмп.')
    k_vals = list(range(n_binom + 1))
    p_theor = [math.comb(n_binom, k) * (p_binom**k) * ((1-p_binom)**(n_binom-k)) for k in k_vals]
    ax.bar(k_vals, p_theor, width=0.4, alpha=0.6, color='coral', label='Теор. P(X=k)')
    ax.set_title('5. Биномиальное (вариант 9)')
    ax.set_xlabel('k')
    ax.legend()
    ax.grid(alpha=0.3)

    fig.delaxes(axes[5])
    plt.tight_layout()
    plt.savefig('lab3_variant9_5graphs.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Графики сохранены в lab3_variant9_5graphs.png (без scipy)")

print("\n" + "=" * 70)
