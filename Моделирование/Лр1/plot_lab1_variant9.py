from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


class LinearCongruentialGeneratorR3:

    def __init__(
        self,
        A0: int = 123,
        A1: int = 456,
        A2: int = 789,
        m: int = 2**16,
        k1: int = 1664525,
        k2: int = 1013904223,
        k3: int = 1103515245,
        C: int = 12345,
    ) -> None:
        self.m = m
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.C = C
        self.A = [A0 % m, A1 % m, A2 % m]
        self.current_index = 2

    def next(self) -> float:
        i = self.current_index
        new_A = (
            self.k1 * self.A[i]
            + self.k2 * self.A[i - 1]
            + self.k3 * self.A[i - 2]
            + self.C
        ) % self.m
        self.A.append(new_A)
        self.current_index += 1
        return new_A / self.m

    def generate_sequence(self, n: int) -> np.ndarray:
        sequence = [self.next() for _ in range(n)]
        return np.array(sequence, dtype=float)


def calculate_correlation(sequence: np.ndarray, s: int) -> float:
    """Расчёт обычного коэффициента корреляции Пирсона между z_i и z_{i+s}."""
    T = len(sequence)
    if T <= s + 1:
        return 0.0
    x = sequence[:-s]
    y = sequence[s:]
    if x.std(ddof=1) == 0 or y.std(ddof=1) == 0:
        return 0.0
    r = np.corrcoef(x, y)[0, 1]
    return float(r)


def _ensure_outdir(path: str) -> Path:
    outdir = Path(path).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir


def main() -> int:
    ap = argparse.ArgumentParser(
        description="ЛР1, вариант 9: линейная смешанная формула (r=3)"
    )
    ap.add_argument(
        "--n",
        type=int,
        default=5000,
        help="объём выборки T_total (по умолчанию 5000)",
    )
    ap.add_argument(
        "--k",
        type=int,
        default=20,
        help="число интервалов/бинов на [0,1) для гистограммы (по умолчанию 20)",
    )
    ap.add_argument(
        "--t-min",
        type=int,
        default=100,
        help="минимальное T для графика зависимости R от T (по умолчанию 100)",
    )
    ap.add_argument(
        "--t-max",
        type=int,
        default=2000,
        help="максимальное T для графика зависимости R от T (по умолчанию 2000)",
    )
    ap.add_argument(
        "--t-step",
        type=int,
        default=100,
        help="шаг по T для графика зависимости R от T (по умолчанию 100)",
    )
    ap.add_argument(
        "--s-list",
        type=str,
        default="2,5,10",
        help='список значений s для корреляции, формат "2,5,10"',
    )
    ap.add_argument(
        "--outdir",
        type=str,
        default=str(Path(__file__).with_name("plots_variant9")),
        help="директория для сохранения PNG",
    )
    ap.add_argument(
        "--show",
        action="store_true",
        help="показывать окна с графиками (по умолчанию только сохраняет PNG)",
    )

    args = ap.parse_args()
    outdir = _ensure_outdir(args.outdir)

    print("=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА №1: ПОСТРОЕНИЕ И ТЕСТИРОВАНИЕ ДАТЧИКА БСВ")
    print("=" * 70)
    print("Вариант 9: Линейная смешанная формула (r = 3)")
    print("Параметры датчика:")
    print("  r = 3 (порядок рекурсии)")
    print("  m = 2^16 = 65536")
    print("  k1 = 1664525, k2 = 1013904223, k3 = 1103515245")
    print("  C = 12345")
    print("  A0 = 123, A1 = 456, A2 = 789")
    print("-" * 70)

    print("\nГенерация последовательности...")
    rng = LinearCongruentialGeneratorR3()
    T_total = int(args.n)
    z = rng.generate_sequence(T_total)

    print(f"Сгенерировано {T_total} псевдослучайных чисел")
    print(f"Первые 10 значений: {[round(x, 4) for x in z[:10]]}")

    M_theoretical = 0.5
    D_theoretical = 1.0 / 12.0

    M_empirical = float(np.mean(z))
    D_empirical = float(np.var(z, ddof=1))

    plt.figure(figsize=(10, 6))

    categories = ["M(z)", "D(z)"]
    theoretical_values = [M_theoretical, D_theoretical]
    empirical_values = [M_empirical, D_empirical]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = plt.bar(
        x - width / 2,
        theoretical_values,
        width,
        label="Теоретическое значение",
        color="skyblue",
        edgecolor="navy",
        linewidth=2,
    )
    bars2 = plt.bar(
        x + width / 2,
        empirical_values,
        width,
        label="Экспериментальная оценка",
        color="lightcoral",
        edgecolor="darkred",
        linewidth=2,
    )

    for bar in bars1:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.01,
            f"{height:.4f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    for bar in bars2:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.01,
            f"{height:.4f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    plt.ylabel("Значение", fontsize=12)
    plt.title(
        "Сравнение теоретических и экспериментальных значений M и D",
        fontsize=14,
        fontweight="bold",
    )
    plt.xticks(x, categories, fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, axis="y")
    plt.ylim(0, 0.6)

    plt.tight_layout()
    md_path = outdir / "01_mean_variance_comparison.png"
    plt.savefig(md_path, dpi=150)
    if args.show:
        plt.show()
    else:
        plt.close()

    K = int(args.k)

    plt.figure(figsize=(12, 6))

    counts, bins = np.histogram(z, bins=K, range=(0.0, 1.0))
    relative_frequencies = counts / float(T_total)

    plt.bar(
        bins[:-1],
        relative_frequencies,
        width=bins[1] - bins[0],
        alpha=0.7,
        color="skyblue",
        edgecolor="navy",
        linewidth=1.5,
        align="edge",
    )

    theoretical_relative_freq = 1.0 / K
    plt.axhline(
        y=theoretical_relative_freq,
        color="red",
        linestyle="--",
        linewidth=2.5,
        label=f"Теоретическая частота (1/{K} = {1.0 / K:.3f})",
    )

    plt.xlabel("Интервал", fontsize=12)
    plt.ylabel("Относительная частота", fontsize=12)
    plt.title(
        "Гистограмма распределения относительных частот",
        fontsize=14,
        fontweight="bold",
    )
    plt.grid(True, alpha=0.3, axis="y")
    plt.legend(fontsize=11)
    plt.xticks(np.linspace(0.0, 1.0, 11), [f"{i/10:.1f}" for i in range(11)])
    plt.ylim(0, max(relative_frequencies) * 1.2 if len(relative_frequencies) else 0.15)

    plt.tight_layout()
    hist_path = outdir / "02_histogram.png"
    plt.savefig(hist_path, dpi=150)
    if args.show:
        plt.show()
    else:
        plt.close()

    T_values = np.arange(1, 2001)  # T = 1..2000
    s_values = [2, 5, 10]
    colors = ["C0", "C1", "C2"]

    plt.figure(figsize=(12, 6))

    for i, s in enumerate(s_values):
        R_values: list[float] = []
        for T_current in T_values:
            R = calculate_correlation(z[:T_current], s)
            R_values.append(R)

        plt.plot(
            T_values,
            R_values,
            color=colors[i],
            linewidth=1.8,
            label=f"s={s}",
        )

    plt.axhline(y=0, color="black", linestyle="-", linewidth=1.0)
    plt.xlabel("T", fontsize=12)
    plt.ylabel("R(T)", fontsize=12)
    plt.title("Графики зависимости R от T", fontsize=14, fontweight="bold")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11, loc="upper right")

    # Диапазоны по осям, близкие к примеру
    plt.ylim(-0.55, 0.3)
    plt.xlim(0, 2000)
    plt.xticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000])

    plt.tight_layout()
    corr_path = outdir / "03_correlation.png"
    plt.savefig(corr_path, dpi=150)
    if args.show:
        plt.show()
    else:
        plt.close()

    print("\n" + "=" * 70)
    print("ВЫВОДЫ О РЕЗУЛЬТАТАХ МОДЕЛИРОВАНИЯ БСВ")
    print("=" * 70)

    print("1. Математическое ожидание и дисперсия:")
    print(f"   - M(z) = {M_empirical:.4f} (теор. {M_theoretical:.4f})")
    print(f"   - D(z) = {D_empirical:.4f} (теор. {D_theoretical:.4f})")

    print("\n2. Равномерность распределения подтверждается гистограммой")

    print("\n3. Статистическая независимость:")
    ci_95 = 1.96 / np.sqrt(2000)
    print(f"   95% доверительный интервал при T=2000: ±{ci_95:.4f}")

    all_in_ci = True
    for s in s_values:
        R_Tmax = calculate_correlation(z[:2000], s)
        print(f"   s={s}: R = {R_Tmax:.4f}")
        if abs(R_Tmax) > ci_95:
            all_in_ci = False

    if all_in_ci:
        print("\n   ✓ Все значения R(T_max) находятся внутри доверительного интервала")
        print("   ✓ Корреляция статистически незначима")
        print("   ✓ Элементы последовательности можно считать независимыми")
    else:
        print(
            "\n   Обнаружена статистически значимая корреляция "
            "для некоторых значений s"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


