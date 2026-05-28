# 正弦波PWMの過変調時の信号波の振幅Aを求める
# - 波形選択を引数化（SPWM / THI / SVM）
# - 関数分割・型注釈・docstring

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Tuple

import numpy as np
from scipy.integrate import quad
from scipy.optimize import fsolve, minimize_scalar
import matplotlib.pyplot as plt


# =========================
# 波形定義
# =========================
def make_wave(mode: str = "SVM", thi_ratio: float = 0.25) -> Callable[[float], float]:
    """
    任意のtに対して u(t)+z(t) を返す波形関数を生成する。
    mode:
      - "SPWM": 三相正弦の基本波のみ（z=0）
      - "THI" : 三相に3次高調波を重畳（z = thi_ratio*sin(3t)）
      - "SVM" : 空間ベクトル変調相当 z = -(max(u,v,w)+min(u,v,w))/2
    thi_ratio: THI重畳時の係数（例: 1/6, 1/4）
    """
    def wave(t: float | np.ndarray) -> float | np.ndarray:
        u = np.sin(t)
        v = np.sin(t - 2 * np.pi / 3)
        w = np.sin(t + 2 * np.pi / 3)

        if mode.upper() == "SPWM":
            z = 0.0
        elif mode.upper() == "THI":
            z = thi_ratio * np.sin(3 * t)
        elif mode.upper() == "SVM":
            # np.maximum/np.minimum はスカラ/配列どちらにも対応
            z = -0.5 * (np.maximum.reduce([u, v, w]) + np.minimum.reduce([u, v, w]))
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        return u + z

    return wave


# =========================
# 基本関数
# =========================
def fourier_integrand(t: float, a: float, wave: Callable[[float], float]) -> float:
    """
    基本波の正弦係数用積分の integrand = sin(t) * min(1, a*wave(t))
    """
    return float(np.sin(t) * np.minimum(1.0, a * wave(t)))


def equation(a: float, m: float, max_wave_val: float, wave: Callable[[float], float]) -> float:
    """
    f(a) = m - S(a) = 0 を解く。
    積分で S(a) を評価。
    """
    s, _ = quad(lambda t: fourier_integrand(t, a, wave), 0.0, np.pi / 2.0, limit=200)
    return m - s


def find_max_wave_value(wave: Callable[[float], float]) -> float:
    """
    wave(t) の最大値 max_t wave(t) を [0, 2π] で探索。
    対称性に依存しないよう 2π で探索する。
    """
    res = minimize_scalar(lambda t: -float(wave(t)), bounds=(0.0, 2.0 * np.pi), method="bounded")
    return float(-res.fun)


# =========================
# 解法
# =========================
def solve_a_for_m(
    m: float,
    wave: Callable[[float], float],
    max_wave_val: float,
    a_prev: float | None = None,
) -> float:
    """
    与えられた m に対して a を求める。
    - 線形領域: 解析解 a = 4m/pi
    - 過変調: fsolve で数値解（直前の解を初期値に活用）
    """
    a_boundary = 1.0 / max_wave_val
    m_boundary = a_boundary * np.pi / 4.0

    # 線形領域は解析解で終了
    if m <= m_boundary:
        return float(4.0 * m / np.pi)

    # 過変調領域の初期値候補
    guesses: List[float] = []
    if a_prev is not None:
        guesses.append(max(a_prev, a_boundary * 1.01))
    # 線形推定値（過変調域では過小だが一応候補に）
    guesses.append(4.0 * m / np.pi)
    guesses.append(a_boundary * 1.05)
    # 徐々に大きめの値も試す
    guesses.extend([a_boundary * s for s in (1.1, 1.2, 1.5, 2.0, 3.0)])

    for g in guesses:
        try:
            sol, info, ier, _ = fsolve(
                lambda a: equation(a, m, max_wave_val, wave),
                x0=g,
                full_output=True,
                maxfev=5000,
            )
            if ier == 1:
                return float(sol[0])
        except Exception:
            pass

    raise RuntimeError(f"収束失敗: m={m:.6f}")


# =========================
# 設定
# =========================
@dataclass(frozen=True)
class Config:
    mode: str = "SVM"         # "SPWM" / "THI" / "SVM"
    thi_ratio: float = 0.25   # THIモードの重畳係数（例: 1/6, 1/4）
    m_start: float = 0.001
    m_stop: float = 1.000
    m_step: float = 0.001
    csv_path: Path = Path("output.csv")


# =========================
# メイン処理
# =========================
def main(cfg: Config) -> None:
    wave = make_wave(cfg.mode, cfg.thi_ratio)
    max_wave_val = find_max_wave_value(wave)

    a_boundary = 1.0 / max_wave_val
    m_boundary = a_boundary * np.pi / 4.0

    m_values = np.arange(cfg.m_start, cfg.m_stop, cfg.m_step)

    a_results: List[float] = []
    m_results: List[float] = []

    # CSVに保存
    with cfg.csv_path.open("w", newline="") as f:
        writer = csv.writer(f)

        a_prev: float | None = None
        for m in m_values:
            # 線形領域は解析解で即時決定
            if m <= m_boundary:
                a_val = 4.0 * m / np.pi
            else:
                a_val = solve_a_for_m(m, wave, max_wave_val, a_prev=a_prev)

            writer.writerow([f"{m:.3f}", f"{a_val:.8f}"])
            a_results.append(a_val)
            m_results.append(m)
            a_prev = a_val

    # 描画
    if a_results:
        plt.figure()

        # 過変調領域（数値解）
        plt.plot(a_results, m_results, color="black", linestyle="--", label="Overmodulation region")

        # 線形領域（解析解）
        a_linear = np.linspace(0.0, a_boundary, 200)
        m_linear = a_linear * np.pi / 4.0
        plt.plot(a_linear, m_linear, color="black", linestyle="-", label="Linear region")

        # 境界
        plt.axvline(x=a_boundary, color="black", linestyle=":")
        plt.plot(a_boundary, m_boundary, "ko")
        plt.text(a_boundary + 0.05, m_boundary, f"({a_boundary:.4g}, {m_boundary:.4g})", va="center", color="black")

        plt.xlabel("Modulation Index $A$", math_fontfamily="cm")
        plt.ylabel("Normalized Fundamental Component $M$", math_fontfamily="cm")
        plt.xlim(0, 4)
        plt.ylim(0, 1)
        plt.grid(True)
        plt.legend()
        plt.show()


if __name__ == "__main__":
    # 例: SVM（元コード相当）
    cfg = Config(
        mode="SPWM",
        thi_ratio=0.16666,
        m_start=0.001,
        m_stop=1.000,
        m_step=0.001,
        csv_path=Path("output.csv"),
    )
    main(cfg)