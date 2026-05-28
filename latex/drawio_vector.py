import sys
import io
import numpy as np


def arrow(x1, y1, x2, y2, size=5.0, aspect=0.33, fill_color="#000000"):
	"""
	塗りつぶし矢印を描く
	- x1, y1: 始点
	- x2, y2: 終点
	- size: 三角形の縦方向長さ
	- aspect: 横方向(開き)比率
	- fill_color: 矢印先端の塗り色
	"""
	dx = x2 - x1
	dy = y2 - y1
	L = np.hypot(dx, dy)
	if L == 0:
		return

	ux, uy = dx / L, dy / L
	vx, vy = -uy, ux

	# 三角形の座標
	tip_x, tip_y = x2, y2
	base_x = x2 - size * ux
	base_y = y2 - size * uy
	left_x = base_x + size * aspect * vx
	left_y = base_y + size * aspect * vy
	right_x = base_x - size * aspect * vx
	right_y = base_y - size * aspect * vy

	# 線の本体を描く
	print('<path>')
	print(f'  <move x="{x1:.3f}" y="{y1:.3f}" />')
	print(f'  <line x="{base_x:.3f}" y="{base_y:.3f}" />')
	print('</path>')
	print('<stroke />')

	# 矢印の先端
	print(f'<fillcolor color="{fill_color}" />')
	print('<path>')
	print(f'  <move x="{tip_x:.3f}" y="{tip_y:.3f}" />')
	print(f'  <line x="{left_x:.3f}" y="{left_y:.3f}" />')
	print(f'  <line x="{right_x:.3f}" y="{right_y:.3f}" />')
	print('  <close />')
	print('</path>')
	print('<fill />')


def generate_content() -> str:
	buffer = io.StringIO()
	old_stdout = sys.stdout
	try:
		sys.stdout = buffer

		# === XML出力 ===
		print('<shape w="100" h="100" aspect="variable" strokewidth="inherit">')
		print('<foreground>')

		# ── ここは自由に編集できる箇所 ──────────────────────────────
		cx, cy = 50.0, 50.0
		Theta = 45 * (np.pi / 180)

		r = [np.sin(Theta), np.sin(Theta - 2*np.pi/3), np.sin(Theta - 4*np.pi/3)]
		# r = [1,1,1]
		R = 33.33
		for k in range(3):
			theta = np.deg2rad(-120 * k)
			x1, y1 = cx, cy
			x2 = cx + r[k] * np.cos(theta) * R
			y2 = cy - r[k] * np.sin(theta) * R
			if np.hypot(x2 - x1, y2 - y1) > 0.1:
				arrow(x1, y1, x2, y2, size=5.0, aspect=0.33)
		# 合成ベクトル
		x2 = cx + (r[0] * np.cos(0) + r[1] * np.cos(-2*np.pi/3) + r[2] * np.cos(2*np.pi/3)) * R
		y2 = cy - (r[0] * np.sin(0) + r[1] * np.sin(-2*np.pi/3) + r[2] * np.sin(2*np.pi/3)) * R
		arrow(cx, cy, x2, y2, size=7.0, aspect=0.33)
		# ────────────────────────────────────────────────────────────

		print('</foreground>')
		print('</shape>')

		return buffer.getvalue()
	finally:
		sys.stdout = old_stdout


def copy_to_clipboard(text: str) -> bool:
	try:
		import pyperclip
		pyperclip.copy(text)
		return True
	except Exception:
		return False


def main():
	result = generate_content()
	print(result)
	if copy_to_clipboard(result):
		print("クリップボードにコピーしました。")
	else:
		print("クリップボードへのコピーに失敗しました。")


if __name__ == "__main__":
	main()