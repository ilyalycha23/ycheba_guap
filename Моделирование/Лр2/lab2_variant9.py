import random

# Исходные данные
x = [-97.8, -80.7, -16.4, 4.2, 26.6, 71.2, 77.5]
p = [0.05, 0.248, 0.206, 0.124, 0.127, 0.186, 0.059]

# Проверка: сумма вероятностей = 1
assert abs(sum(p) - 1.0) < 1e-6, "Сумма вероятностей должна быть равна 1"

# Накопленные вероятности (метод обратного преобразования)
cum_p = []
s = 0
for pi in p:
    s += pi
    cum_p.append(s)

def generate_value():
    """Генерация одного значения дискретной СВ по методу обратного преобразования"""
    z = random.random()
    for i, cp in enumerate(cum_p):
        if z < cp:
            return x[i]
    return x[-1]

# Генерация выборки объёмом n = 500
random.seed(42)
n = 500
sample = [generate_value() for _ in range(n)]

# ========== ВЫВОД РЕЗУЛЬТАТОВ ==========
print("=" * 50)
print("ПЕРВЫЕ 30 ЗНАЧЕНИЙ ВЫБОРКИ")
print("=" * 50)
for i in range(30):
    print(f"  {i+1:2}. {sample[i]:7.2f}", end="")
    if (i + 1) % 5 == 0:
        print()
if 30 % 5 != 0:
    print()

# Теоретические характеристики (формулы 3.1 и 3.2)
# M(x) = Σ xj * pj
M_theor = sum(xi * pi for xi, pi in zip(x, p))
# D(x) = Σ pj * (xj - M)²
D_theor = sum(pi * (xi - M_theor)**2 for xi, pi in zip(x, p))

# Эмпирические оценки
M_emp = sum(sample) / n
D_emp = sum((xi - M_emp)**2 for xi in sample) / (n - 1)  # несмещённая

print("\n" + "=" * 50)
print("СРАВНЕНИЕ ЧИСЛОВЫХ ХАРАКТЕРИСТИК")
print("=" * 50)
print(f"M (теор)  = {M_theor:.4f}")
print(f"M* (эмп)  = {M_emp:.4f}")
print(f"|dM|      = {abs(M_theor - M_emp):.4f}")
print()
print(f"D (теор)  = {D_theor:.4f}")
print(f"D* (эмп)  = {D_emp:.4f}")
print(f"|dD|      = {abs(D_theor - D_emp):.4f}")

# Эмпирические вероятности (частоты)
counts = [sample.count(xi) for xi in x]
emp_p_ordered = [c / n for c in counts]

print("\n" + "=" * 50)
print("СРАВНЕНИЕ ВЕРОЯТНОСТЕЙ")
print("=" * 50)
print("   xj        pj(теор)   pj*(эмп)")
for i in range(len(x)):
    print(f"{x[i]:8.2f}    {p[i]:.3f}      {emp_p_ordered[i]:.3f}")

# ========== ГРАФИКИ ==========
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    index = list(range(len(x)))
    width = 0.35

    ax1.bar([i - width/2 for i in index], emp_p_ordered, width, label='Эмпирические', color='steelblue', alpha=0.8)
    ax1.bar([i + width/2 for i in index], p, width, label='Теоретические', color='coral', alpha=0.8)
    ax1.set_xticks(index)
    ax1.set_xticklabels([f'{xi:.1f}' for xi in x])
    ax1.set_xlabel('Значения случайной величины x')
    ax1.set_ylabel('Вероятность')
    ax1.set_title('Гистограммы: эмпирические и теоретические вероятности')
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    for i in range(len(x)):
        ax1.text(i - width/2, emp_p_ordered[i] + 0.01, f'{emp_p_ordered[i]:.2f}', ha='center', fontsize=8)
        ax1.text(i + width/2, p[i] + 0.01, f'{p[i]:.2f}', ha='center', fontsize=8)

    categories = ['M (мат. ожидание)', 'D (дисперсия)']
    ax2.bar([0 - 0.175, 1 - 0.175], [M_theor, D_theor], 0.35, label='Теоретические', color='coral', alpha=0.8)
    ax2.bar([0 + 0.175, 1 + 0.175], [M_emp, D_emp], 0.35, label='Эмпирические', color='steelblue', alpha=0.8)
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(categories)
    ax2.set_ylabel('Значение')
    ax2.set_title('Сравнение числовых характеристик')
    ax2.legend()
    ax2.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('lab2_variant9_results.png', dpi=150, bbox_inches='tight')
    plt.close()
except ImportError:
    print("\n(matplotlib не установлен — графики не построены)")
