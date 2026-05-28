# インバータ技術 style.cls 執筆ガイド

**インバータ技術（本誌） 執筆マニュアル**

---

## 目次

- [第0章 はじめに](#第0章-はじめに)
  - [図作成用Pythonスクリプト](#図作成用pythonスクリプト)
- [第1章 原稿ファイルの構成](#第1章-原稿ファイルの構成)
- [第2章 見出しと本文](#第2章-見出しと本文)
- [第3章 図の挿入](#第3章-図の挿入)
- [第4章 表・数式・コード](#第4章-表数式コード)
- [第5章 特殊レイアウト](#第5章-特殊レイアウト)
- [付録 リファレンス](#付録-リファレンス)

---

# 第0章 はじめに

## このガイドの目的

このガイドは、`style.cls`を使って本誌（インバータ技術）を執筆する際のルールとパターンをまとめたものです。「こういうレイアウトにしたいときはこう書く」という形式で、コピペして使えることを重視しています。

## 必要な環境

### VScode+LaTeX Workshop
必須ではありませんが、快適な開発をするために必要です。

### LuaLaTeX

TeX Live 2024以降を推奨します。`style.cls`はLuaLaTeX専用です。

```bash
# バージョン確認
lualatex --version
```

### フォント
リポジトリにフォントファイルがあるのでインストール不要ですが、一応使っているフォントを示しておきます:

- A-OTF-RyuminPr6-Light（本文明朝）
- A-OTF-GothicBBBPr6-Medium（本文ゴシック）
- A-OTF-FutoGoB101Pr6-Bold（太字）
- A-OTF-ShinGoPr6 シリーズ（章見出し）
- Jun34Pro シリーズ（セクション見出し）
- A-OTF-ShinGoPr6-Light（等幅和文）
- CourierNew（等幅欧文）
- NewsGothic（ページ数）

### Draw.io Desktop

図の編集に使用します。コンパイル開始時にpythonが勝手に走って更新があった`.drawio`ファイルを自動で`.png`に変換します。

- [Draw.io Desktop ダウンロード](https://github.com/jgraph/drawio-desktop/releases)

### Python 3

`drawio_convert.py`などの実行に必要です。

```bash
python3 --version
```

## ビルド方法

### VScode+LaTeX Workshop
Ctrl(Command)+Sで保存とかしたら勝手にコンパイル（`latexmk master.tex`を実行）するようにsettings.json入れてます。

### 基本コマンド

```bash
latexmk master.tex
```

これだけでOKです。`latexmkrc`が以下を自動で行います:

1. `.drawio` → `.png` 変換（`drawio_convert.py`を実行）
2. 中間ファイルを`.tex_intermediates/`に作りながら頑張ってコンパイル
3. PDF完成
4. `out/`にpdfコピーして`.tex_intermediates/`削除
5. （指定がある場合）SNS投稿用サンプルの各ページのwebpファイル出力

### SNS投稿用サンプルの出力
latexmkrcファイルの`# system("python3 pdf2png_convert.py $pdf");`のコメントアウトを解除するとコンパイル終了時に`pdf2png_convert.py`が実行され、`/out/master/`ディレクトリの中にwebp形式で全ページが書き出されます。基本的に`master.tex`の`\sampleWaterMark`と併用することを想定しています。

## リポジトリ構成

```
.
├── master.tex			# メインファイル
├── style.cls			# クラスファイル
├── latexmkrc			# ビルド設定
├── 0.tex 〜 n.tex		# 各章
├── tableofcontents.tex		# 目次・まえがき
├── appendix.tex		# 付録
├── atogaki.tex			# あとがき
├── okuzuke.tex			# 奥付
├── figure/			# 図フォルダ
│   ├── 0/			# 第0章用
│   ├── 1/			# 第1章用
│   └── n/			# 第n章用
├── drawio_convert.py		# .drawio→.png変換
├── drawio_vector.py		# ベクトル図生成
├── drawio_wave.py		# 波形図生成
├── drawio_xyplot.py		# XYプロット生成
└── pdf2png_convert.py		# PDF→PNG変換
```

## 図作成用Pythonスクリプト

Draw.ioには「カスタムシェイプ」機能があり、XML形式で図形を定義できます。以下のPythonスクリプトは、数式から正確な図形（ベクトル、波形、グラフ）を生成し、Draw.ioに貼り付けられるXMLをクリップボードにコピーします。

### 共通の使い方

1. スクリプト内のパラメータや数式を編集
2. `python3 スクリプト名.py` を実行
3. XMLがクリップボードにコピーされる
4. Draw.ioで「配置」→「挿入」→「図形…」→ペースト

### drawio_vector.py — ベクトル図

3相交流のベクトル図など、矢印を使った図を生成します。

```python
# 主な編集箇所
cx, cy = 50.0, 50.0          # 中心座標（100x100の座標系）
Theta = 45 * (np.pi / 180)   # 基準角度

# 3相の振幅（この例では位相45 degでの瞬時値）
r = [np.sin(Theta), np.sin(Theta - 2*np.pi/3), np.sin(Theta - 4*np.pi/3)]
R = 33.33                     # ベクトルの最大長さ
```

**用途例:**
- 回転磁界のベクトル図
- 3相電流の合成ベクトル
- フェーザ図

**arrow関数のパラメータ:**
| 引数 | 説明 | デフォルト |
|------|------|-----------|
| `x1, y1` | 始点座標 | — |
| `x2, y2` | 終点座標 | — |
| `size` | 矢印の頭の大きさ | 5.0 |
| `aspect` | 矢印の頭の開き具合 | 0.33 |
| `fill_color` | 矢印の塗り色 | `#000000` |

### drawio_wave.py — 波形図

PWM波形やスイッチング波形など、時間軸に沿った波形を生成します。

```python
# 主な編集箇所
A = 0.8           # 振幅（変調率）
Fc = 9            # キャリア周波数倍率

# 波形の種類を切り替え（コメントアウトで選択）
printlinep(x/(2*np.pi), sw_wn*3/2)  # W相の中性点電圧
# printlinep(x/(2*np.pi), sw_u * 2-1)  # U相のスイッチング状態
```

**用途例:**
- 正弦波PWMの出力波形
- 3相インバータの線間電圧
- 搬送波と信号波

**座標系:**
- X軸: 0〜100（時間軸、`x/(2*np.pi)`で正規化）
- Y軸: 0〜100（中心が50、振幅±50）

### drawio_xyplot.py — XYプロット

パラメータ$t$をもつ$(x(t), y(t))$をグラフとしてプロットします。

```python
# 主な編集箇所
for t in np.linspace(0, 1, 10000):
    x = t * 2  # X座標（0〜2の範囲を0〜100に変換）

    # 例: 1次遅れ系のステップ応答
    zeta = 0.7
    omega_n = 20
    omega_d = omega_n * np.sqrt(1 - zeta**2)
    y = 1 - np.exp(-zeta * omega_d * t)

    printlinep(t, x, y * 2 - 1)  # Y軸は-1〜1を0〜100に変換
```

**用途例:**
- 伝達関数のステップ応答
- トルク-すべり特性曲線
- B-H曲線

**座標系:**
- 入力: X軸 0〜1（または任意）、Y軸 -1〜1
- 出力: 100x100のDraw.io座標系に変換

### 実行例

```bash
# ベクトル図を生成
python3 drawio_vector.py
```
出力例:
```xml
<shape w="100" h="100" aspect="variable" strokewidth="inherit">
<foreground>
<path>
  <move x="50.000" y="50.000" />
  <line x="73.570" y="26.430" />
</path>
...
</shape>
```

### Draw.ioへの貼り付け手順

1. Draw.ioを開く
2. メニュー「配置」→「図形を挿入」→「XMLを編集」
3. テキストエリアにペースト（Ctrl+V / Cmd+V）
4. 「挿入」をクリック
5. 挿入された図形を選択し、サイズ・位置を調整

### Tips

- **座標系は100x100**: すべてのスクリプトは100x100の座標系を使用。Draw.io上で自由に拡大縮小できます
- **線の太さはinherit**: Draw.ioの図形プロパティで線の太さを変更できます
- **色の変更**: `fill_color`パラメータや、Draw.io上で後から変更可能
- **複数の図形**: スクリプトを複数回実行して、別々のシェイプとして貼り付けることも可能

---

# 第1章 原稿ファイルの構成

## master.tex の役割

`master.tex`はすべての章をまとめるメインファイルです。`\include`をコメントアウトしたりしなかったりして分割コンパイルが実現できます。例えば、第1章を編集してるときには
```latex
\include{1.tex}
\clearemptydoublepage
```
だけコメントアウトから除外すると他の章にコンパイル時間とられずに済みます。
### 基本構造

```latex
\documentclass{style}
\unimathsetup{warnings-off={mathtools-colon,mathtools-overbracket}}

% \nuritashi %塗り足し（入稿時に有効化）

% \sampleWaterMark %サンプル透かし（入稿時に削除、SNS投稿用に）

\volume{2025年12月号}

\begin{document}
\include{tableofcontents.tex}
\clearemptydoublepage

\include{0.tex}
\clearemptydoublepage

\include{1.tex}
\clearemptydoublepage

% ... 章を追加 ...

\include{appendix.tex}
\clearemptydoublepage

\include{atogaki.tex}
\clearpage

\include{okuzuke.tex}
\end{document}
```

### \include の順序

1. `tableofcontents.tex` — 目次・まえがき
2. `0.tex` 〜 `n.tex` — 本編各章
3. `appendix.tex` — 付録
4. `atogaki.tex` — あとがき
5. `okuzuke.tex` — 奥付

### \clearemptydoublepage

両面印刷で章が必ず奇数ページ（右ページ）から始まるようにします。偶数ページで終わった場合、空白ページが挿入されます。
標準で`\cleardoublepage`コマンドがあるのですが、それだと白紙が挿入されて誌のロゴやページ数が出ない状態になるので、それを解消してあります（要するにこっち使ってね）。

### \volume{} の設定

フッターに表示される号数を設定します。`\volume`がないとフッターがページ数だけになります。誌のロゴが出なくなります。

```latex
\volume{2025年12月号}
```

## 各章ファイルの構造

### 冒頭テンプレート（必須）

すべての章ファイルは以下のような形式で始めます:

```latex
\graphicspath{{./figure/1}}  % 章番号に合わせる

\partset{制御方式の基礎}{制御方式の\\基礎}{part}
\begin{defbox}
    この章では、インバータの基本構成と制御方式の全体像を整理します。\par
    図や式の書き方、章立ての例としても使えるように、短い導入文にしています。
\end{defbox}

\section{PWMとは？}
PWM（パルス幅変調）の基本概念と、平均電圧（または電流）の制御方法を説明します。\par
```

### \graphicspath

その章で使う図のフォルダを指定します。

```latex
\graphicspath{{./figure/3}}  % 第3章なら figure/3/
```

### \partset{目次での表示}{タイトル}{画像}

| 引数 | 説明 | 例 |
|------|------|-----|
| 第1引数 | 目次・ヘッダー用の名前 | `おちんぽみるくでちゃう〜〜` |
| 第2引数 | 扉ページのタイトル（長い時`\\`で改行可） | `おちんぽみるく\\でちゃう〜〜` |
| 第3引数 | 扉画像のファイル名（pngなら拡張子なしも可。ファイルが見つからないとのいまげになる） | `part` |

上の例は不適切な表現が含まれるため、以下のような技術的な表現を使用してください。

```latex
% 改行を入れる例
\partset{インバータの動作原理}{インバータの\\動作原理}{part}
```

### まえがき・あとがき・奥付

これらは特殊な構造を持つので、既存ファイルをコピーして編集してください。

- `tableofcontents.tex` — まえがき部分を編集
- `atogaki.tex` — あとがきを編集
- `okuzuke.tex` — 発行日、著者情報などを編集

## 入稿時の設定

### \nuritashi（塗り足し有効化）

印刷所に入稿する際は、塗り足し（トンボ）を有効にします。3mmの塗り足しがつくよ！

```latex
\nuritashi %コメントを外す
```

### \sampleWaterMark の削除

SNSサンプル版の透かしを消します。これコメントアウトしないと赤文字でサンプルってデカデカと入ります。

```latex
% \sampleWaterMark  %コメントアウトまたは削除
```

---

# 第2章 見出しと本文

## 見出し階層

### \partset → 章タイトル（扉ページ）

各章の冒頭で使用。扉ページが生成されます。

```latex
\partset{目次での表示名}{タイトル}{part}
```

### \section → 節

枠で囲まれた中央揃えの見出しになります。

```latex
\section{回路（内部）にプローブを当てる手順}
```
枠の中の改行位置を指定する場合、次みたいに書きます。[]の中が目次での表示になり、{}が枠の中の表示になります。
```latex
\section[回路（内部）にプローブを当てる手順]{回路（内部）に\\プローブを当てる手順}
```

### \subsection → 項

●マーク付きの見出しになります。

```latex
\subsection{回転磁界とは}
```

### \subsubsection → 小項

▶マーク付きの見出しになります。

```latex
\subsubsection{数の子天井}
```

## 本文の書き方

### \par で段落終了

段落の終わりには`\par`を付けます。

```latex
初潮の数ヶ月前から透明又は白色のおりものの増加が
見られるようになった後、初潮が発生します。\par

膣の周りをよく舐めてあげるなどしていち早く初潮に
気づいて、なるべく早く犯すようにしましょう。\par
```

**注意:** `\par`を忘れると、段落頭の1文字分のスペース（字下げ）がなくなります。

### ナカグロ挿入
英単語をカタカナで書いてる言葉は、単語間に「・」（ナカグロ）を入れます。例:フライバック・コンバータ　フィードバック（feedbackで1単語なので入れない）　オープン・ループ　コモン・モード・ノイズ・フィルタ

### 句読点の自動変換

`style.cls`では以下の自動変換が行われます:

| 入力 | 出力 |
|------|------|
| `。` | `．`（全角ピリオド） |
| `、` | `，`（全角カンマ） |

つまり、普通にtexには「。」「、」で書けばOKです。いちいちIMEの設定変えなくて良いです。

### 括弧の詰め処理

全角括弧の前後は自動で詰められます。基本的に和文では全角かっこを使うようにしてください。そのほうが綺麗なので。
| 入力 | 処理 |
|------|------|
| `（` | 前に-0.4emのスペース |
| `）` | 後に-0.4emのスペース |

## 強調・単位

### \ital{文字} — イタリック
数式モード使うと不都合なときに使ったりする。
```latex
電圧\ital{V}
```

### \un{単位} — 変数に対する単位

変数の後に単位を付ける場合（角括弧付き）:

```latex
直流リンク電圧$V\un{V}$は...  % → V [V]
```

### \unn{単位} — 数値に対する単位

数値の後に単位を付ける場合:

```latex
デバイスの耐圧は$3000\unn{V}$です。  % → 3000 V
```
現状、m^2みたいな上付き文字とかの単位に対応してないのでそこは`\mathrm`とかで頑張って書いてね（ごめんね）。

### \mr{文字} — 数式中のローマン体

数式中で立体（ローマン体）にしたい文字:

```latex
$V_\mr{in}$  % 添字がローマン体
$V_\mr{max}$
```
標準の`\mathrm`の短縮です。

### 太文字・ゴシック体の数式
例えば、キャプション中で`$`で囲んで数式環境にするとキャプションのフォントではなく強制的にリュウミン（本文の明朝フォント）になって統一感がないので、キャプション中とかで変数使うときは以下みたいに書きます。
```latex
\subsection[ゲート抵抗RGの役割]{ゲート抵抗\ital{R}$_\mr{\textbf{G}}$の役割}
```
```latex
\caption{\ital{V}${}_\textbf{GS}$=15~V} %
\figdescription{\ital{V}${}_\textsf{GS}$=15~V} % $V_{GS}=15\unn{V}$と等価？
```
`\figdescription`のような中ゴシックBBBのとこは`\textsf`、`\subsection`、`\caption`のような太ゴB101のとこは`\textbf`であることに注意です。


## 索引

### \index{よみがな@表示名}

索引に登録したいキーワードの直後に記述します:

```latex
直流リンク\index{ちょくりゅう@直流リンク}は、スイッチングによって...
```
索引結局使わなかったので多分今回も使わなそうですけどね。

---

# 第3章 図の挿入

## 基本パターン（1段幅）

最も基本的な図の挿入パターンです。

```latex
\begin{figure}[b!]
    \centering
    \includegraphics[width=\linewidth]{ファイル名}
    \caption{図のキャプション}
    \figdescription{補足説明をここに書く。}
    \figlabel{ラベル名}
\end{figure}
```

### 配置オプション

| オプション | 意味 |
|-----------|------|
| `t!` | ページ上部に強制配置 |
| `b!` | ページ下部に強制配置 |
| `h!` | その場に強制配置（レイアウトが崩れやすいので非推奨） |

基本的に2段組み`b!`か`t!`を使います。これは正直流派があったりLaTeXが思ったとおりに配置しなかったりするので根性でなんとかします。

### \figdescription

図の下に薄いグレーの補足説明ボックスを追加します。省略可能。

```latex
\figdescription{モータ断面の模式図。寸法や注釈は必要に応じて追記する。}
```

## 大きな図（2段抜き）

2段組の両方にまたがる大きな図には`figure*`を使います。

```latex
\begin{figure*}[b!]
    \centering
    \includegraphics[width=\linewidth]{大きな図}
    \caption{2段抜きの図}
    \figdescription{補足説明}
    \figlabel{大きな図ラベル}
\end{figure*}
```

## キャプション横配置

キャプションを図の左側に配置するパターンです。

```latex
\begin{figure*}[b!]
    \begin{minipage}[b]{0.25\linewidth}
        \centering
        \caption{キャプション}
        \figdescription{補足説明}
        \figlabel{ラベル}
    \end{minipage}
    \begin{minipage}[b]{0.74\linewidth}
        \centering
        \includegraphics[width=\linewidth]{画像ファイル}
    \end{minipage}
\end{figure*}
```
図側の幅、1-0.25って0.75のはずですが、0.74みたいにちょっと小さくしないと入らなかったりするので0.01くらい小さくしてね。

## 参照方法

### \figref{ラベル} — 同じ章内

```latex
\figref{モータ構造}を参照してください。
% → 図1.3を参照してください。
```

出力は**太字**で「**図1.3**」のようになります。

### \figrefex{ラベル}{章番号} — 他の章

```latex
第1章の\figrefex{子宮内膜}{1}で説明したように...
% → 第1章の図1.5で説明したように...
```

## 図ファイルの管理

### フォルダ構成

```
figure/
├── 0/          # 第0章用
│   └── part.png
├── 1/          # 第1章用
│   ├── part.png
│   ├── 端子配置.drawio
│   ├── 端子配置.drawio.png      # 自動生成
│   └── ...
└── ...
```

### .drawio → .png 自動変換

`latexmk`実行時に`drawio_convert.py`が自動で変換します。

- `端子配置.drawio` → `端子配置.drawio.png`が生成される
- LaTeX側では`\includegraphics{端子配置}`と拡張子なしで指定可

### part.png（章扉画像）

各章の扉ページに表示される画像です。`figure/章番号/part.png`に配置します。

---

# 第4章 表・数式・コード

## 表

### tablebox環境の基本

```latex
\begin{table}[t!]
    \centering
    \caption{部品一覧}
    \begin{tablebox}{|c|c|C|}
        \hline
        \rowcolor{boxgray}
        部品名 & 型番 & 備考 \\\hline
        MOSFET & TK10A60D & 耐圧600V \\\hline
        抵抗 & 10kΩ & 1/4W \\\hline
    \end{tablebox}
    \tablelabel{部品一覧}
\end{table}
```

### カスタム列タイプ

| 列タイプ | 説明 |
|---------|------|
| `C` | 中央揃え・可変幅 |
| `R` | 右揃え・可変幅 |
| `L` | 左揃え・可変幅 |
| `c` | 中央揃え・固定幅（標準） |
| `l` | 左揃え・固定幅（標準） |
| `r` | 右揃え・固定幅（標準） |

### \rowcolor{boxgray}

ヘッダー行をグレーにします。

```latex
\rowcolor{boxgray}
列1 & 列2 & 列3 \\\hline
```

### 参照

```latex
\tableref{犯され一覧}  % → 表1.2
```

## 数式

### eq環境（グレーボックス付き）

数式をグレーボックスで囲みます。equationとほとんど等価です。

```latex
\begin{eq}
    V = IR
    \eqlabel{オームの法則} % 参照用
\end{eq}
```

### eqpre環境

正直自分でもなんで定義したのかわかりませんが、eq環境のequationない版です。正直defboxでいいです。

### 複数行の数式

```latex
\begin{eq}
    \begin{aligned}
        v_\mr{u} &= V_m \sin(\omega t) \\
        v_\mr{v} &= V_m \sin(\omega t - \frac{2\pi}{3}) \\
        v_\mr{w} &= V_m \sin(\omega t + \frac{2\pi}{3})
    \end{aligned}
\end{eq}
```

### 参照

```latex
\eqref{オームの法則}  % → 式(1.5)
```

## コードリスト

### lstlisting環境

```latex
\begin{lstlisting}[caption=Lチカのコード, label=l-chika]
void setup() {
    pinMode(13, OUTPUT);
}

void loop() {
    digitalWrite(13, HIGH);
    delay(1000);
    digitalWrite(13, LOW);
    delay(1000);
}
\end{lstlisting}
```

### 言語指定

```latex
\begin{lstlisting}[caption=タイトル, label=ラベル, language=C]
// Cのコード
\end{lstlisting}
```

### 参照

```latex
\listref{l-chika}
```

### \SplitListingTwoColumn（2段組表示）

長いコードを2段組で表示します。

```latex
\SplitListingTwoColumn{code/main.c}
```

---

# 第5章 特殊レイアウト

## defbox環境

グレー背景のボックスを作成します。様々な用途に使えます。

### 章冒頭のイントロダクション

```latex
\begin{defbox}
    この章では、凛子ちゃんと衣吹ちゃんの犯し方を解説します。
\end{defbox}
```

### 箇条書きの囲み

```latex
\begin{defbox}
    \begin{itemize}
        \item バス電圧: $1.5\unn{kV}$
        \item 定格電流: $2\unn{kA}$
        \item スイッチング周波数: 1〜$2\unn{MHz}$
	\item ヒートシンク温度: $52\unn{\degree C}$
    \end{itemize}
\end{defbox}
```

### 重要事項のハイライト

```latex
\begin{defbox}
    	extbf{注意:} パラメータを再確認してください
\end{defbox}
```

## コラム（column環境）

囲み記事を作成します。`figure*`環境の中で使用します。

```latex
\begin{figure*}[t!]
    \centering
    \begin{column}{PWMの歴史}
        \noindent
        {\color{darkgray}●}\hspace{0.5em}\textbf{1960年代}\par
        パワーエレクトロニクスの基礎技術が整備され、各種変換回路が発展。\par

        \newpage\noindent  % 2段組での改ページ

        {\color{darkgray}●}\hspace{0.5em}\textbf{2022年}\par
        SiC/GaNデバイスの普及により高周波・高効率化が進展。\par
    \end{column}
\end{figure*}
```

### 2段組内での改ページ

コラム内で次の段に移りたいときは`\newpage\noindent`を使います。

## その他のテクニック

### \mbox{} で改行禁止

単語の途中で改行されたくないときはこうします:

```latex
\mbox{TK10A60D}
\mbox{100〜200~V} %~はスペースね
```

### ~（チルダ）で改行禁止スペース

数値と単位の間など。本当は`\unn`使えばいいんだけど、そういう気分じゃないときってあるじゃん。`\unn`だと数式モード内でしか使えないけどこれはいろんなとこで使える。
```latex
100~V
図~1.3
```

### \clearpage / \newpage の使い分け

| コマンド | 動作 |
|---------|------|
| `\newpage` | 現在の段を終了し次の段へ（2段組の場合） |
| `\clearpage` | 現在のページを終了し次のページへ |
| `\clearemptydoublepage` | 両面印刷用に奇数ページまでスキップ |

---

# 付録 リファレンス

## A. 全カスタムコマンド一覧

### 単位・数式

| コマンド | 引数 | 説明 | 例 |
|---------|------|------|-----|
| `\un{単位}` | 1 | 変数の単位 [V] | `$V\un{V}$` |
| `\unn{単位}` | 1 | 数値の単位 | `100\unn{Hz}` |
| `\mr{文字}` | 1 | 数式中ローマン体 | `$V_\mr{max}$` |

### フォントスタイル

| コマンド | 引数 | 説明 |
|---------|------|------|
| `\ital{文字}` | 1 | イタリック体 |
| `\hwid{文字}` | 1 | 半角幅文字 |

### 参照マクロ

| コマンド | 説明 | 出力例 |
|---------|------|--------|
| `\figref{ラベル}` | 図参照（同章） | **図1.3** |
| `\figrefex{ラベル}{章}` | 図参照（他章） | **図2.5** |
| `\tableref{ラベル}` | 表参照 | **表1.1** |
| `\eqref{ラベル}` | 式参照 | 式(1.5) |
| `\listref{ラベル}` | リスト参照 | **リスト1.2** |

### ラベル設定

| コマンド | 対象 |
|---------|------|
| `\figlabel{ラベル}` | 図 |
| `\tablelabel{ラベル}` | 表 |
| `\eqlabel{ラベル}` | 数式 |
| `\listlabel{ラベル}` | コードリスト |

### その他

| コマンド | 説明 |
|---------|------|
| `\partset{短縮名}{タイトル}{画像}` | 章見出し設定 |
| `\figdescription{説明}` | 図の補足説明 |
| `\volume{号数}` | フッターの号数設定 |
| `\nuritashi` | 塗り足し有効化 |
| `\sampleWaterMark` | サンプル透かし表示 |
| `\clearemptydoublepage` | 両面印刷用ページ調整 |
| `\index{よみ@表示}` | 索引登録 |

## B. 全カスタム環境一覧

| 環境 | 説明 |
|------|------|
| `defbox` | グレー背景ボックス |
| `eq` | 数式ボックス（equation内蔵） |
| `eqpre` | 数式ボックス（equation内蔵なし） |
| `tablebox{列指定}` | 表ボックス |
| `column{タイトル}` | コラム（figure*内で使用） |

## C. 定義済み色・フォント一覧

### 色

| 色名 | 用途 |
|------|------|
| `boxgray` | ボックス背景（薄グレー） |
| `darkgray` | 見出しマーク、枠線 |

### フォントコマンド

| コマンド | フォント | 用途 |
|---------|---------|------|
| `\junM` | Jun 34 Pro Medium | セクション見出し |
| `\shingothicR` | 新ゴ R | 目次 |
| `\shingothicM` | 新ゴ M | パート見出し |
| `\shingothicB` | 新ゴ B | パート番号 |

## D. hyperref設定

次号用に変更が必要な箇所（`style.cls`内）:

```latex
\hypersetup{
    pdftitle={インバータ技術2025年12月号},      % ← 号数を変更
    pdfsubject={インバータの創り方},            % ← 特集名を変更
    pdfauthor={IR製作所, Pv電子製作所},         % ← 著者を変更
    pdfkeywords={インバータ; PWM; 誘導モータ},  % ← キーワードを変更
    % ...
}
```

## E. コピペ用テンプレート集

### 章の冒頭

```latex
\graphicspath{{./figure/X}}  % Xを章番号に

\partset{章タイトル}{章タイトル}{part}
\begin{defbox}
    この章の概要を書く。
\end{defbox}

\section{最初のセクション}
```

### 図（1段幅）

```latex
\begin{figure}[b!]
    \centering
    \includegraphics[width=\linewidth]{ファイル名}
    \caption{キャプション}
    \figdescription{補足説明}
    \figlabel{ラベル}
\end{figure}
```

### 図（2段抜き）

```latex
\begin{figure*}[b!]
    \centering
    \includegraphics[width=\linewidth]{ファイル名}
    \caption{キャプション}
    \figdescription{補足説明}
    \figlabel{ラベル}
\end{figure*}
```

### 図（横キャプション）

```latex
\begin{figure*}[b!]
    \begin{minipage}[b]{0.25\linewidth}
        \centering
        \caption{キャプション}
        \figdescription{補足説明}
        \figlabel{ラベル}
    \end{minipage}
    \begin{minipage}[b]{0.74\linewidth}
        \centering
        \includegraphics[width=\linewidth]{ファイル名}
    \end{minipage}
\end{figure*}
```

### 表

```latex
\begin{table}[t!]
    \centering
    \caption{表のタイトル}
    \begin{tablebox}{|c|c|C|}
        \hline
        \rowcolor{boxgray}
        列1 & 列2 & 列3 \\\hline
        データ1 & データ2 & データ3 \\\hline
    \end{tablebox}
    \tablelabel{ラベル}
\end{table}
```

### 数式

```latex
\begin{eq}
    V = IR
    \eqlabel{ラベル}
\end{eq}
```

### 数式（複数行）

```latex
\begin{eq}
    \begin{aligned}
        a &= b + c \\
        d &= e + f
    \end{aligned}
\end{eq}
```

### コラム

```latex
\begin{figure*}[t!]
    \centering
    \begin{column}{コラムタイトル}
        \noindent
        {\color{darkgray}●}\hspace{0.5em}\textbf{小見出し}\par
        本文テキスト。\par
    \end{column}
\end{figure*}
```

## F. 既知の不具合

### subsectionとsubsubsection、複数行非対応
2行取りにするとなんかめっちゃ詰まっちゃう。だいたいjlreqのせい。僕のせいじゃないんだ。

---

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2025-12-10 | 初版作成 |
| 2026-05-28 | 全年齢版 |