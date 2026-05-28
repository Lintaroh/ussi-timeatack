import numpy as np

import io
import pyperclip
import sys

buffer = io.StringIO()
sys.stdout = buffer  # 標準出力をバッファに切り替え


def printlinep(t, x,y):
    if t == 0:
        print(f'<move x="{(float(x)*100):.4f}" y="{(50.0 - float(y)*50.0):.4f}" />')
    else:
        print(f'<line x="{(float(x)*100):.4f}" y="{(50.0 - float(y)*50.0):.4f}" />')

def triangle(theta):
    theta %= np.pi*2
    if theta >= 0 and theta < np.pi/2:
        y = theta/(np.pi/2)
    elif theta >= np.pi/2 and theta < np.pi*3/2:
        y = 2-theta/(np.pi/2)
    else:
        y = -4+theta/(np.pi/2)
    return y

def svm(Vu, Vv, Vw):
    return (min([Vu, Vv, Vw]) + max([Vu, Vv, Vw]))/-2

print('<shape h="100" w="100" aspect="variable" strokewidth="inherit">')
print('<foreground>')
print('<path>')
print('<move x="0.0" y="100"/>')
for t in np.linspace(-0, 1, 10000):

    x = t*2
    zeta = 0.7
    omega_n = 20
    omega_d = omega_n * np.sqrt(1-zeta**2)
    # if t > 0:
    #     y = 1-np.exp(-zeta*omega_d*t)*(np.sin(omega_d*t) * (zeta/np.sqrt(1-zeta**2)) + np.cos(omega_d*t))
    # else:
    #     y = 0
    y = 1-np.exp(-zeta*omega_d*t)
    printlinep(t, x, y * 2 - 1)


    # s = t
    # torque = (10 / s) / ((0.5 + 1/s)**2 + 20)
    # if np.isnan(torque):
    #     torque = 0
    # printlinep(t, s, torque * 2-1)

print('</path>')
print('<stroke />')
print('</foreground>')

print('</shape>')

sys.stdout = sys.__stdout__  # 標準出力を元に戻す

result = buffer.getvalue()
print(result)  # 確認用
pyperclip.copy(result)  # クリップボードへコピー

print("クリップボードにコピーしました。")