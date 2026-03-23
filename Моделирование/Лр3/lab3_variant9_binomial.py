import sys
import io
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except (AttributeError, OSError):
    pass  # Windows console without UTF-8

import math
import random
import numpy as np

# ========== ИСХОДНЫЕ ДАННЫЕ ==========
n = 9          # число испытаний
p = 0.45       # вероятность успеха
q = 1 - p      # вероятность неудачи
N = 500        # объём моделируемой выборки

# ========== ТЕОРЕТИЧЕСКИЕ ВЫЧИСЛЕНИЯ ==========
def factorial(k):
    return math.factorial(k) if k >= 0 else 0

def C(n, k):
    """Число сочетаний C(n,k) = n! / (k!(n-k)!)"""
    if k < 0 or k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def binomial_pmf(k):
    """P(X = k) = C(n,k) * p^k * (1-p)^(n-k)"""
    return C(n, k) * (p ** k) * (q ** (n - k))

# Ряд распределения: x = 0, 1, 2, ..., n
x_values = list(range(n + 1))
p_theor = [binomial_pmf(k) for k in x_values]

# Функция распределения F(x) = P(X <= x)
F_theor = []
cum = 0
for k in x_values:
    cum += binomial_pmf(k)
    F_theor.append(cum)

# Числовые характеристики (теоретические)
# M(X) = n*p, D(X) = n*p*q, σ(X) = sqrt(D)
M_theor = n * p
D_theor = n * p * q
sigma_theor = math.sqrt(D_theor)

# ========== МОДЕЛИРОВАНИЕ (метод суммирования Бернулли) ==========
def generate_binomial_bernoulli(n_trials, prob):
    """Генерация одной реализации Bin(n, p) как суммы n испытаний Бернулли"""
    success_count = 0
    for _ in range(n_trials):
        if random.random() < prob:
            success_count += 1
    return success_count

# Генерация выборки
random.seed(42)
sample = [generate_binomial_bernoulli(n, p) for _ in range(N)]

# Альтернатива: через numpy (для проверки)
np.random.seed(42)
sample_np = np.random.binomial(n, p, size=N)

# ========== ЭМПИРИЧЕСКИЕ ОЦЕНКИ ==========
M_emp = sum(sample) / N
D_emp = sum((xi - M_emp) ** 2 for xi in sample) / (N - 1)
sigma_emp = math.sqrt(D_emp)

# Эмпирические вероятности (частоты)
counts = [sample.count(k) for k in x_values]
p_emp = [c / N for c in counts]

# ========== ВЫВОД РЕЗУЛЬТАТОВ ==========

print("\n1. РЯД РАСПРЕДЕЛЕНИЯ (теоретический)")
print("-" * 40)
print("   k      P(X=k)      F(x)=P(X<=k)")
for k in x_values:
    print(f"  {k:2d}     {p_theor[k]:.4f}       {F_theor[k]:.4f}")
print(f"  Summa   {sum(p_theor):.4f}  (proverka summy)")

print("\n2. ЧИСЛОВЫЕ ХАРАКТЕРИСТИКИ")
print("-" * 40)
print(f"  M(X) теор.  = {M_theor:.4f}")
print(f"  M(X) эмп.   = {M_emp:.4f}")
print(f"  |dM|        = {abs(M_theor - M_emp):.4f}")
print()
print(f"  D(X) теор.  = {D_theor:.4f}")
print(f"  D(X) эмп.   = {D_emp:.4f}")
print(f"  |dD|        = {abs(D_theor - D_emp):.4f}")
print()
print(f"  σ(X) теор.  = {sigma_theor:.4f}")
print(f"  σ(X) эмп.   = {sigma_emp:.4f}")

print("\n3. СРАВНЕНИЕ ВЕРОЯТНОСТЕЙ")
print("-" * 40)
print("   k      P(X=k) теор.   P*(X=k) эмп.")
for k in x_values:
    print(f"  {k:2d}       {p_theor[k]:.4f}          {p_emp[k]:.4f}")

print("\n4. ВЫЧИСЛЕНИЕ ЗАДАННЫХ ВЕРОЯТНОСТЕЙ")
print("-" * 40)
# P(X = 3)
P_3 = binomial_pmf(3)
print(f"  P(X = 3) = {P_3:.4f}")

# P(X >= 1) = 1 - P(X = 0)
P_at_least_1 = 1 - binomial_pmf(0)
print(f"  P(X >= 1) = 1 - P(X=0) = {P_at_least_1:.4f}")

# P(X <= 4) = F(4)
P_no_more_4 = F_theor[4]
print(f"  P(X <= 4) = F(4) = {P_no_more_4:.4f}")

# P(2 ≤ X ≤ 5) = P(X=2)+P(X=3)+P(X=4)+P(X=5) = F(5)-F(1)
P_2_to_5 = sum(binomial_pmf(k) for k in range(2, 6))
print(f"  P(2 <= X <= 5) = {P_2_to_5:.4f}")

print("\n5. ПЕРВЫЕ 30 ЗНАЧЕНИЙ ВЫБОРКИ")
print("-" * 40)
for i in range(30):
    print(f"  {i+1:2d}. {sample[i]}", end="")
    if (i + 1) % 10 == 0:
        print()
if 30 % 10 != 0:
    print()

# ========== ГРАФИКИ ==========
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 1. Многоугольник распределения (теор. и эмп.)
    ax1 = axes[0, 0]
    width = 0.35
    x_pos = np.arange(len(x_values))
    ax1.bar(x_pos - width/2, p_theor, width, label='Теоретические', color='coral', alpha=0.8)
    ax1.bar(x_pos + width/2, p_emp, width, label='Эмпирические', color='steelblue', alpha=0.8)
    ax1.set_xlabel('k (число успехов)')
    ax1.set_ylabel('Вероятность')
    ax1.set_title('Ряд распределения: теоретический и эмпирический')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([str(k) for k in x_values])
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    # 2. Функция распределения F(x)
    ax2 = axes[0, 1]
    ax2.step(x_values, F_theor, where='post', label='Теоретическая F(x)', color='darkgreen', linewidth=2)
    ax2.scatter(x_values, F_theor, color='darkgreen', s=30, zorder=5)
    ax2.set_xlabel('x')
    ax2.set_ylabel('F(x) = P(X <= x)')
    ax2.set_title('Функция распределения')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.05, 1.05)

    # 3. Сравнение M и D
    ax3 = axes[1, 0]
    categories = ['M(X)', 'D(X)', 'σ(X)']
    theor_vals = [M_theor, D_theor, sigma_theor]
    emp_vals = [M_emp, D_emp, sigma_emp]
    x_cat = np.arange(len(categories))
    ax3.bar(x_cat - width/2, theor_vals, width, label='Теоретические', color='coral', alpha=0.8)
    ax3.bar(x_cat + width/2, emp_vals, width, label='Эмпирические', color='steelblue', alpha=0.8)
    ax3.set_xticks(x_cat)
    ax3.set_xticklabels(categories)
    ax3.set_ylabel('Значение')
    ax3.set_title('Числовые характеристики')
    ax3.legend()
    ax3.grid(axis='y', linestyle='--', alpha=0.5)

    # 4. Гистограмма выборки
    ax4 = axes[1, 1]
    ax4.hist(sample, bins=range(-1, n+2), density=True, alpha=0.7, color='steelblue', 
             edgecolor='black', label='Эмпирическая выборка')
    ax4.bar(x_values, p_theor, width=0.6, alpha=0.5, color='coral', label='Теоретическое PMF')
    ax4.set_xlabel('k')
    ax4.set_ylabel('Вероятность / Плотность')
    ax4.set_title('Гистограмма выборки и теоретическое распределение')
    ax4.legend()
    ax4.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('lab3_variant9_results.png', dpi=150, bbox_inches='tight')
    plt.close()
except ImportError:
    print("\n(matplotlib не установлен — графики не построены)")
