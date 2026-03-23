# -*- coding: utf-8 -*-
"""
Лабораторная работа №2 (Лр3): Моделирование непрерывной СВ
Вариант 1: Бета-распределение
Пять видов распределений на основе БСВ (базовой случайной величины).
"""
import sys
import io
import os
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except (AttributeError, OSError):
    pass

import math
import random
import numpy as np

# Сохранение в папку Вариант1
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(OUT_DIR)

# Параметры для всех распределений
N = 2000       # объём выборки
random.seed(42)
np.random.seed(42)

# ========== 1. ЭКСПОНЕНЦИАЛЬНОЕ (формула 2.5) ==========
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

# ========== 5. БЕТА-РАСПРЕДЕЛЕНИЕ (вариант 1) ==========
# Beta(alpha, beta): X~Gamma(a,1), Y~Gamma(b,1) => X/(X+Y) ~ Beta(a,b)
# Gamma(k,1) = сумма k независимых Exp(1)
ALPHA_BETA, BETA_BETA = 2, 5

def gen_gamma_int(shape):
    """Gamma(shape, 1) для целого shape — сумма shape экспоненциальных"""
    s = 1.0
    for _ in range(shape):
        z = random.random()
        s *= z
    return -math.log(s) if s > 0 else 0

def gen_beta():
    x = gen_gamma_int(ALPHA_BETA)
    y = gen_gamma_int(BETA_BETA)
    s = x + y
    return x / s if s > 0 else 0.5  # на случай численной ошибки

sample_beta = [gen_beta() for _ in range(N)]
# M = alpha/(alpha+beta), D = alpha*beta / ((alpha+beta)^2 * (alpha+beta+1))
ab = ALPHA_BETA + BETA_BETA
M_beta_theor = ALPHA_BETA / ab
D_beta_theor = (ALPHA_BETA * BETA_BETA) / (ab**2 * (ab + 1))
M_beta_emp = sum(sample_beta) / N
D_beta_emp = sum((x - M_beta_emp)**2 for x in sample_beta) / (N - 1)

# Бета-функция для теоретической плотности
def beta_pdf(x, a, b):
    if x <= 0 or x >= 1:
        return 0
    return (x**(a-1) * (1-x)**(b-1)) / math.exp(math.lgamma(a) + math.lgamma(b) - math.lgamma(a+b))

# ========== ВЫВОД СРАВНЕНИЯ M и D ==========
print("=" * 70)
print("ЛАБОРАТОРНАЯ РАБОТА №2: МОДЕЛИРОВАНИЕ НЕПРЕРЫВНОЙ СЛУЧАЙНОЙ ВЕЛИЧИНЫ")
print("Вариант 1 (Бета-распределение) + 4 стандартных распределения")
print("=" * 70)

results = [
    ("Экспоненциальное (lambda=1)", M_exp_theor, D_exp_theor, M_exp_emp, D_exp_emp),
    ("Равномерное [0,5]", M_unif_theor, D_unif_theor, M_unif_emp, D_unif_emp),
    ("Эрланга (K=3, lambda=1)", M_erl_theor, D_erl_theor, M_erl_emp, D_erl_emp),
    ("Нормальное (m=0, sigma=1)", M_norm_theor, D_norm_theor, M_norm_emp, D_norm_emp),
    (f"Бета (alpha={ALPHA_BETA}, beta={BETA_BETA})", M_beta_theor, D_beta_theor, M_beta_emp, D_beta_emp),
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
    try:
        from scipy import stats as sps
        x_erl = np.linspace(0, max(sample_erlang), 200)
        ax.plot(x_erl, sps.erlang.pdf(x_erl, K_ERLANG, scale=1/LAMBDA_ERL), 'r-', lw=2, label='Теор. f(x)')
        ax.legend(loc='upper right')
    except ImportError:
        pass
    ax.set_title('3. Эрланга порядка K (формула 2.11)')
    ax.set_xlabel('x')
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

    # 5. Бета-распределение (вариант 1)
    ax = axes[4]
    ax.hist(sample_beta, bins=40, density=True, alpha=0.7, color='steelblue', edgecolor='black', label='Эмп.')
    x_beta = np.linspace(0.001, 0.999, 200)
    y_beta = np.array([beta_pdf(x, ALPHA_BETA, BETA_BETA) for x in x_beta])
    ax.plot(x_beta, y_beta, 'r-', lw=2, label='Теор. f(x)')
    ax.set_title(f'5. Бета-распределение (alpha={ALPHA_BETA}, beta={BETA_BETA})')
    ax.set_xlabel('x')
    ax.legend()
    ax.grid(alpha=0.3)

    fig.delaxes(axes[5])
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, 'lab3_variant1_5graphs.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Графики сохранены в {out_path}")
except ImportError:
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
    ax.hist(sample_beta, bins=40, density=True, alpha=0.7, color='steelblue', edgecolor='black', label='Эмп.')
    x_beta = np.linspace(0.001, 0.999, 200)
    y_beta = np.array([beta_pdf(x, ALPHA_BETA, BETA_BETA) for x in x_beta])
    ax.plot(x_beta, y_beta, 'r-', lw=2, label='Теор. f(x)')
    ax.set_title(f'5. Бета-распределение (alpha={ALPHA_BETA}, beta={BETA_BETA})')
    ax.set_xlabel('x')
    ax.legend()
    ax.grid(alpha=0.3)

    fig.delaxes(axes[5])
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, 'lab3_variant1_5graphs.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Графики сохранены в {out_path}")

print("\n" + "=" * 70)
