import numpy as np

import io
import pyperclip
import sys

buffer = io.StringIO()
sys.stdout = buffer  # 標準出力をバッファに切り替え

def printlinep(x,y):
    if x ==0:
        print(f'<move x="{(x*100):.04}" y="{float(50-y*50):.04}" />')
    else:
        print(f'<line x="{(x*100):.04}" y="{float(50-y*50):.04}" />')

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

v = 0
swsw = 1
for x in np.linspace(0, 4*np.pi, 10000):
    #print(f'<line x="{:.04}" y="{:.04}" />')
    A = 0.8
    Fc = 9
    theta_digital = np.floor((x-0.5 * np.pi/Fc) * Fc/np.pi) * np.pi/Fc +0.5 * np.pi/Fc
    Vu = np.sin(theta_digital)
    Vv = np.sin(theta_digital - np.pi*2/3)
    Vw = np.sin(theta_digital + np.pi*2/3)

    # Vz = svm(Vu, Vv, Vw)
    # Vz = np.sin(x*3)/6
    # Vz = np.sin(x*3)/4
    Vz = 0
    Vu += Vz
    Vv += Vz
    Vw += Vz
    Vu *= A
    Vv *= A
    Vw *= A
    # Vu = min(max(Vu, -1), 1)
    # Vv = min(max(Vv, -1), 1)
    # Vw = min(max(Vw, -1), 1)
    #Vz = -min([Vu,Vv,Vw])-1
    carrier = -triangle(x*Fc)
    sw_u = int((Vu) > carrier)
    sw_v = int((Vv) > carrier)
    sw_w = int((Vw) > carrier)
    sw_uv = sw_u-sw_v
    sw_vw = sw_v-sw_w
    sw_wu = sw_w-sw_u
    vn = (sw_u + sw_v + sw_w)/3
    sw_un = sw_u - vn
    sw_vn = sw_v - vn
    sw_wn = sw_w - vn
    # printlinep(100*x/(2*np.pi), float(min(max(np.sin(x*2 + np.pi*4/3) *50 * 0.75 +triangle(x*3)*0 + swv * 0,-70),70)))
    # printlinep(100*x/(2*np.pi), float((np.sin((np.floor((x * (180/np.pi))/60+30*np.pi/180))*np.pi*60/180-30*np.pi/180)*50)))


    printlinep(x/(2*np.pi),sw_wn*3/2)
    # printlinep(x/(2*np.pi),v)
    # printlinep(x/(2*np.pi),sw_u * 2-1)
    # v += ((sw_u * 2 - 1) - v) * 0.001
    # if v < max(sw_u, 0):
    #     v = max(sw_u, 0)
    # else:
    #     v = v*0.9999

    # printlinep(x/(2*np.pi), swsw*2-1)

print('</path>')
print('<stroke />')
print('</foreground>')

print('</shape>')

sys.stdout = sys.__stdout__  # 標準出力を元に戻す

result = buffer.getvalue()
print(result)  # 確認用
pyperclip.copy(result)  # クリップボードへコピー

print("クリップボードにコピーしました。")