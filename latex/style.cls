\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{style}[2025/09/15 v1.1 author: IR2110]
% jlreq 内で calc 由来の長さ式を使うため先に読み込む

\LoadClass[base=lines,twocolumn,twoside,fleqn,line_length=24zw,column_gap=2zw, baselineskip=18Q, fontsize=12Q, jafontsize=12Q, number_of_lines=50, paper=b5j,lualatex]{jlreq}

% 便利マクロ
\newcommand{\un}[1]{~[\textrm{#1}]}%変数に対する単位
\newcommand{\unn}[1]{~\textrm{#1}}%数字に対する単位
\newcommand{\mr}[1]{\textrm{#1}}


% パッケージ
% Engine/locale and math
\RequirePackage{luatexja-preset}
\RequirePackage{amssymb}
\RequirePackage{mathtools}
\RequirePackage{mleftright}
\RequirePackage{siunitx}
\RequirePackage{unicode-math}
\RequirePackage{newunicodechar}
\RequirePackage{dotseqn}

% Colors, graphics, SVG
\RequirePackage[table]{xcolor}
\RequirePackage{graphicx}
\RequirePackage{svg}
\DeclareGraphicsExtensions{.png,.pdf}

% Core utilities
\RequirePackage{ifthen}
\RequirePackage{calc}
\RequirePackage{float}
\RequirePackage{ascmac}
\RequirePackage{xparse}

% Tables
\RequirePackage{array}
\RequirePackage{tabularx}

% Listings and boxes
\RequirePackage{listings}
\RequirePackage[breakable,listingsutf8, most]{tcolorbox}
\tcbuselibrary{hooks}
\usetikzlibrary{calc}

% Multicolumn and formatting
\RequirePackage{enumitem}
\RequirePackage{multicol}
\RequirePackage{titlesec}
\RequirePackage{titletoc}
\RequirePackage{jlreq-complements}

% Index, header/footer
\RequirePackage{makeidx}
\RequirePackage{fancyhdr}

% Document inclusion
\RequirePackage{docmute}

% URLs and hyperlinks (near the end)
\RequirePackage{xurl}
\RequirePackage[pdfencoding=auto]{hyperref}
\RequirePackage{bookmark}
\RequirePackage[noabbrev]{cleveref}

% Wide floats
\RequirePackage{cuted}

% 色
\definecolor{boxgray}{rgb}{0.937,0.937,0.937}
\definecolor{darkgray}{rgb}{0.443,0.443,0.443}
% \definecolor{darkgray}{rgb}{0.88671,0.32,0.5781} % カラー版

% 全角約物の詰め・句読点置換
\newunicodechar{（}{\hspace{-0.4em}（}
\newunicodechar{）}{）\hspace{-0.4em}}
\newunicodechar{。}{．}
\newunicodechar{、}{，}

% 数式
\mleftright
\setmathfont{Latin Modern Math}
\setmathfont{A-OTF-RyuminPr6N-Math.otf}[
range={up/{latin,Latin,num},it/{latin,Latin}},
Scale=1.0
]

% \mathrange{letterspace=-1}{\alpha\beta\gamma}

% フォント定義（重複記述の整理）
\newcommand*\MainSerif{A-OTF-RyuminPr6-Light.otf}
\newcommand*\MainSans {A-OTF-GothicBBBPr6-Medium.otf}
\newcommand*\MainBold {A-OTF-FutoGoB101Pr6-Bold.otf}

\setmainjfont[
	UprightFont=*,
	BoldFont=\MainBold,
	ItalicFont=*,
	ItalicFeatures={RawFeature={+ital}}
]{\MainSerif}
\setmainfont[
	UprightFont=*,
	BoldFont=\MainBold,
	ItalicFont=*,
	ItalicFeatures={RawFeature={+ital}}
]{\MainSerif}
\setsansfont[
	UprightFont=*,
	BoldFont=\MainBold,
	ItalicFont=*,
	ItalicFeatures={RawFeature={+ital}}
]{\MainSans}
\setsansjfont[
	UprightFont=*,
	BoldFont=\MainBold,
	ItalicFont=*,
	ItalicFeatures={RawFeature={+ital}}
]{\MainSans}

% 等幅
\setmonofont{CourierNew.ttf}
\setmonojfont{A-OTF-ShinGoPr6-Light.otf}

% 和文アキ
\renewcommand{\jlreqxkanjiskip}{0.1\zw plus 0.1\zw minus 0.1\zw}

% 任意フォント呼び出しマクロ
\directlua{kpse.set_program_name("luatex")}
\newcommand{\definenewfont}[2]{
	\newcommand{#1}{
		\jfontspec{#2}\fontspec{#2}
	}
}
\definenewfont{\junM}{A-OTF-Jun34Pro-Medium.otf}
\definenewfont{\junL}{A-OTF-Jun101Pr6-Medium.ttf}
\definenewfont{\newsgothic}{NewsGothic.ttf}
\definenewfont{\mbgothic}{A-OTF-GothicMB101-Pr6N.ttf}
\definenewfont{\bbbgothic}{A-OTF-GothicBBBPr6-Medium.otf}
\definenewfont{\bgothic}{A-OTF-FutoGoB101Pr6-Bold.otf}
\definenewfont{\shingothicR}{A-OTF-ShinGoPr6-Regular.otf}
\definenewfont{\shingothicM}{A-OTF-ShinGoPr6-Medium.otf}
\definenewfont{\shingothicB}{A-OTF-ShinGoPr6-Bold.otf}
\definenewfont{\shingothicL}{A-OTF-ShinGoPr6-Light.otf}

% 特殊スタイル
\newcommand{\ital}[1]{
	{\hspace{-0.25em}\addfontfeatures{RawFeature={+ital}}#1\hspace{-0.25em}}
}
\newcommand{\hwid}[1]{
	{\addfontfeatures{RawFeature={+hwid}}#1\hspace{-0.25em}}
}

% 単位長さ
\newlength{\Q}
\setlength{\Q}{0.25mm}

% ドットリーダ（式）
\makeatletter
\renewcommand\EqnDots{\hspace{0mm}\leaders\hbox{\kern1\p@ \hspace{-2pt}…\kern1\p@}\hfill\hspace{-1mm}}
\makeatother

\newcommand{\linegap}{\dimexpr\baselineskip-\ht\strutbox\relax}

% adaptive arc
\tcbset{
	/tcb/adaptive arc/.initial=0mm,
	auto arc/.style={
			enhanced,frame empty,
			interior code={
					\path let\p1=(interior.north east),\p2=(interior.south west),
					\n{height}={\y1-\y2},\n{width}={\x1-\x2}
					in\pgfextra{
						\pgfkeysgetvalue{/tcb/adaptive arc}{\adaptivetargetarc}
						\pgfmathsetmacro{\finalarc}{min(\adaptivetargetarc, \n{height}/2)}
						\path[tcb fill interior, rounded corners=\finalarc pt]
						(interior.south west) rectangle (interior.north east);
					};
				}
		}
}
% 式とかのボックス
\newtcolorbox{defbox}{
	enhanced,breakable, boxrule=0.0mm,top=1.125mm,bottom=1.125mm,
	arc=2mm,colback=boxgray,boxsep=0mm,beforeafter skip=0mm,beforeafter skip balanced=0mm,
	enlarge bottom by=1.125mm,enlarge top by=1.125mm,
	left=1.5mm,right=1.5mm,colframe=white,
	segmentation style={
			% 中間ページでは角丸無効
			middle style={sharp corners},
			% 最初ページでは上だけ角丸
			first style={sharpish corners=south},
			% 最後ページでは下だけ角丸
			last style={sharpish corners=north},
		}
}
\newenvironment{eq}{\begin{flushleft}\begin{defbox}\begin{equation}}{\end{equation}\end{defbox}\end{flushleft}}
\newenvironment{eqpre}{\begin{flushleft}\begin{defbox}\vspace{-1em}}{\end{defbox}\end{flushleft}}

% 図表説明ボックス
\newtcolorbox{expfig}{
	auto arc, adaptive arc=2mm,boxrule=0.0mm,top=0.375mm,bottom=0.375mm,boxsep=0mm,
	colback=boxgray,left=1.5mm,right=1.5mm,before skip=0mm,after skip=0mm, beforeafter skip balanced=0mm,
	colframe=white,
	fontupper=\fontsize{10\Q}{0mm}\bbbgothic,
	halign=flush left,
	enlarge top by=0mm,enlarge bottom by=0mm,
}
\newcommand{\figdescription}[1]{\vspace{-1mm}\begin{expfig}#1\end{expfig}}
\newcommand{\newlinefix}[1]{\\[#1]}

% セクション見出し用
\newtcolorbox{sectionbox}{
	height=12mm,boxrule=0.3mm,arc=0mm,
	beforeafter skip=0.0mm, beforeafter skip balanced=0mm,
	enlarge top by=0.625mm, enlarge bottom by=0.0mm,
	colback=white,colframe=darkgray,
	valign=center,sharp corners=all,
	halign=flush center
}

% パート見出し用
\newtcolorbox{partbox}{
	height=48mm,width=\linewidth,boxrule=0.5mm,
	arc=0mm,colback=white,colframe=darkgray,
	enlarge bottom by=0mm,valign=top,sharp corners=all,
	sidebyside,lefthand width=42mm,text fill,
	halign=flush center,left=0mm,boxsep=0mm,right=0mm,
	subtitle style={
			boxrule=0mm,colframe=darkgray,colback=darkgray
		}
}

% 表ボックス
\newtcolorbox{tablebox}[1]{
	tabularx={#1},
	boxrule=0.25mm,arc=0mm,
	colback=white,colframe=black,
	valign=center,sharp corners=all,
	halign=flush center,
	enlarge bottom by=-3mm,
	enlarge top by=-3mm
}
\newtcbox{\smalltablebox}{
	boxrule=0.25mm,arc=0mm,
	colback=white,colframe=black,
	boxsep=0mm,top=0mm,bottom=0mm,left=0mm,right=0mm,
	valign=center,sharp corners=all,
	halign=flush center,
	enlarge bottom by=-3mm,
	enlarge top by=-3mm
}

% 図表キャプション（jlreq）
\newcommand{\indexheading}{
	ぴっちぴち！！！！！！！！！！！！！！！！！！！
}
\jlreqsetup{
	caption_font=\fontsize{10\Q}{0mm}\bgothic,
	caption_label_font=\bgothic,
	caption_after_label_space=0.5em,
	caption_align=left,
	theindex_heading=\indexheading,
	theindex_twocolumn=true,
	theindex_column_gap=6mm,
	theindex_pagestyle=fancy,
	theindex_column_rule_width=0mm
}

% コラム
\newcounter{column}
\setcounter{column}{1}
\renewcommand{\thecolumn}{コラム\arabic{part}−\arabic{column}}

\newtcolorbox{columnbox}[2][]{
	boxrule=0.5mm,width=\linewidth,
	arc=0mm,colback=white,left=2mm,right=2mm,bottom=3mm,top=3mm,
	colframe=black,sharp corners=all,
	squeezed title*=\scalebox{1.1}[1]{#2},
	attach title to upper={\\},coltitle=black,
	fonttitle=\fontsize{9.21pt}{0mm}\shingothicM,#1
}
\newenvironment{column}[2][]{
	\addtocounter{column}{1}
	\begin{columnbox}{{\addfontfeatures{RawFeature={+hwid}}\thecolumn}　#2}
		\\[-10mm]
		\phantomsection
		\addcontentsline{toc}{section}{\thecolumn　#2}
		\begin{multicols}{2}
			\parindent=3mm
			#1
			}{
		\end{multicols}\end{columnbox}
}

% セクション番号を非表示
\setcounter{secnumdepth}{0}

% 見出しスタイル
\SetBlockHeadingSpaces{
[lines=3]{_subsection,0.5em,_subsubsection{before_lines=0},0.5em}
{_section{*},_subsection{before_lines=0, after_lines=0, lines=1, before_space=0.0mm, after_space=0.0mm}}
{_section{*},_subsection{before_lines=0, after_lines=0, lines=1, before_space=0.0mm, after_space=0.0mm}, _subsubsection{before_lines=0, after_lines=0, lines=1, before_space=0.0mm, after_space=0.0mm} }
}
\RenewBlockHeading{section}{1}{
	font=\fontsize{16\Q}{0mm}\junM,
	align=center,label_format={},
	subtitle_format={},
	format={\parbox[c][3\baselineskip][c]{\linewidth}{\centering \begin{sectionbox}\jlreqHeadingLabel{#1}\quad \jlreqHeadingText{#2}\\\jlreqHeadingSubtitle{#3}\end{sectionbox}}},
	before_lines=0,
	before_space=0mm,
	after_space=0mm,
	after_lines=0,
	subtitle_break=false,
	lines=3,
}

\RenewBlockHeading{subsection}{1}{
	font=\normalsize\bfseries,
	align=left,label_format={},indent=0mm,
	subtitle_format={（#1）},
	format={
			\begin{itemize}[nosep,leftmargin=1.5em,labelwidth=1em,labelsep=0.5em]
				\item[\color{darkgray}●]\jlreqHeadingText{#2}
			\end{itemize}
		},
	subtitle_break=true,
	before_lines=1,
	lines=1,
	after_lines=0,
}

% \makeatletter
% \let\oldsubsection\subsection
% \renewcommand{\subsection}[1]{%
% 	% タイトルを仮ボックスに入れて高さを測る
% 	\setbox0=\vbox{\hsize=\linewidth\normalsize\bfseries #1}%
% 	\ifdim\ht0>\baselineskip
% 		\PackageWarning{mydoc}{Subsection title is more than 1 line: `#1'}%
% 	\fi
% 	% 元の \subsection を呼び出す
% 	\oldsubsection{#1}%
% }
% \makeatother

\RenewBlockHeading{subsubsection}{1}{
	font=\normalsize,align=left,label_format={},
	subtitle_format={（#1）},
	format={
			\begin{itemize}[nosep,leftmargin=1em,labelwidth=1em,labelsep=0em]
				\item[▶]\jlreqHeadingText{#2}
			\end{itemize}
		},
	subtitle_break=true,
	lines=1,
	before_lines=1,
	after_lines=0,
}

% パート見出し
\titlespacing*{\part}{0pt}{0pt}{0pt}[0pt]
\titleformat{\part}[hang]{}{}{0pt}{\fontsize{23.39pt}{4.125mm}\shingothicM\hspace{-2.5mm}}{}

\newcommand{\prepart}[3]{
	\begin{partbox}
		\ifx\relax#3\relax
			\parbox[c][42mm][c]{47mm}{\centering\texttt{のいまげ}}%
			\PackageWarning{style}{画像指定ないよ。のいまげってこと？}%
		\else
			\includegraphics[width=47mm]{#3}%
		\fi
		\tcblower
		\vspace{3mm}
		\fboxrule=0mm
		\addtocounter{part}{1}
		\tcbsubtitle{\fontsize{14.45pt}{0mm}\shingothicB \fbox{\addfontfeatures{RawFeature={+fwid}}\thepart}}
		\addtocounter{part}{-1}
		\fontsize{23.39pt}{4.125mm}\shingothicM\part[#1]{#2}
	\end{partbox}
}
\newcommand{\partset}[3]{
	\begin{figure*}[!t]
		\prepart{#1}{#2}{#3}
	\end{figure*}
}

% 目次
\setcounter{tocdepth}{1}
\contentsmargin{0.0em}
\titlecontents{part}
[0pt]
{\addvspace{2em}\fontsize{14.17pt}{0mm}\shingothicM}
{\addfontfeatures{RawFeature={+fwid}}\contentslabel{0.0em}}
{}
{\normalsize\mbgothic\titlerule*{…} \newsgothic p.\contentspage}
[\addvspace{0.25em}\hrule height 0.1mm depth 0.1mm width 80mm]
\titlecontents{section}
[2em]
{\addvspace{1.5em}\normalsize\shingothicR}
{}
{}
{\normalsize\mbgothic\titlerule*{…} \newsgothic p.\contentspage}
[\addvspace{-0.5em}]

% 索引
\makeindex
\newcommand{\makeidxhead}[1]{
	{\shingothicM{#1}\vspace{1mm}\hrule height 0.1mm depth 0.1mm width \linewidth\vspace{1mm}}
}
\newcommand{\idxdelim}{\titlerule*{…}\newsgothic ~}
\newcommand{\symbolindexname}{記号・数字}
\newcommand{\idxheadstyle}{\rmfamily}

% ヘッダ・フッタ
\newcommand{\volume}[1]{
	\fancyfoot[RE, LO]{\vspace{5mm}\includegraphics[height=2.7mm]{figure/logo.png}\hspace{1.5mm}\raisebox{0.3mm}[0pt][0pt]{#1}}
	\newcommand{\volumetext}{#1}
}

\makeatletter
\@onlypreamble\volume
\makeatother

\renewcommand{\headrulewidth}{0pt}
\pagestyle{fancy}
\fancyfoot{\newsgothic}\fancyhead{}
\fancyfoot[RO, LE]{\newsgothic\selectfont\thepage}

% 偶数白ページにもレイアウト適用
\makeatletter
\newcommand{\clearemptydoublepage}{
	\clearpage
	{\pagestyle{fancy}
		\if@twoside
			\ifodd\c@page
				\hbox{}
				\vspace*{\fill}
				\thispagestyle{fancy}
				\newpage
				\if@twocolumn
					\hbox{}
					\newpage
				\fi
			\fi
		\fi
	}
}
\makeatother

% ソースコード（listings）
\lstset{
	basicstyle={\fontsize{7.09pt}{3mm}\ttfamily},
	frame={tbrl},
	breaklines=true,
	numbers=left,
	showspaces=false,
	xleftmargin=5mm,
	numbersep=2mm,
	showstringspaces=false,
	showtabs=false,
	numberstyle=\ttfamily,
	keywordstyle=\color{black},
	commentstyle=\color{black}\addfontfeatures{RawFeature={+ital}},
	identifierstyle=\color{black},
	stringstyle=\color{black},
	captionpos=t,
	columns=[l]{fullflexible},
}
\lstdefinestyle{splitbox}{
	frame=none,
	xleftmargin=3mm,
	showstringspaces=false,
	columns=[l]{fullflexible},
}

\newcommand{\SplitListingTwoColumn}[1]{
	\begin{tcolorbox}[
			boxrule=0.4pt,arc=0mm,boxsep=0mm,
			colback=boxgray,colframe=black,
			enlarge bottom by=0.0mm,enlarge top by=0.0mm,
			beforeafter skip=0.0mm, beforeafter skip balanced=0mm,
			colback=white
		]
		\setlength{\premulticols}{0pt} % multicol前の余白
		\setlength{\postmulticols}{0pt}% multicol後の余白
		\setlength{\multicolsep}{0pt}  % multicol前後の余白
		\setlength{\columnseprule}{0.4pt}
		\begin{multicols}{2}
			\lstinputlisting[style=splitbox]{#1}
		\end{multicols}
	\end{tcolorbox}
}


\renewcommand{\lstlistingname}{リスト}

% 図表配置
\renewcommand{\topfraction}{1.0}
\renewcommand{\bottomfraction}{1.0}
\renewcommand{\textfraction}{.15}
\renewcommand{\floatpagefraction}{.66}
\setcounter{topnumber}{100}
\setcounter{bottomnumber}{100}
\setcounter{totalnumber}{100}

% 表組
\newcolumntype{C}{>{\centering\arraybackslash}X}
\newcolumntype{R}{>{\raggedright\arraybackslash}X}
\newcolumntype{L}{>{\raggedleft\arraybackslash}X}


\makeatletter
\newdimen\arrayrulewidthb
\arrayrulewidthb=\p@\relax
\newcolumntype{I}{!{\vrule width \arrayrulewidthb}}
\def\hlineb{%
	\noalign{\ifnum0=`}\fi\hrule \@height \arrayrulewidthb \futurelet
		\reserved@a\@xhlineb}
	\def\@xhlineb{\ifx\reserved@a\hlineb
			\vskip\doublerulesep
			\vskip-\arrayrulewidthb
		\fi
		\ifnum0=`{\fi}}
\makeatother

% ハイパーリンク
\hypersetup{
	setpagesize=false,
	luatex,
	hidelinks,
	unicode,
	bookmarksdepth=3,
	bookmarksnumbered=true,
	final,
	hypertexnames=false,
	pdftitle={インバータ技術2025年12月号},
	pdfsubject={インバータの創り方},
	pdfauthor={IR製作所, Pv電子製作所},
	pdfkeywords={インバータ; PWM; 誘導モータ},
	pdfcreator={IR2110},
	pdfproducer={LuaLaTeX},
	pdflang={ja_JP},
	pdfdisplaydoctitle=true,
	pdfpagemode=UseOutlines,
	pdfpagelayout=TwoPageRight
}


\makeatletter

% 塗り足し（必要時に前文で \nuritashi）
\newcommand{\nuritashi}{
	\RequirePackage[lualatex,trimmarks_paper=+6mm,bleed_margin=3mm,show={digital}]{jlreq-trimmarks}
}
\@onlypreamble\nuritashi

% サンプル用ウォーターマーク（前文で \sampleWaterMark）
\newcommand{\sampleWaterMark}{
	\RequirePackage{eso-pic}
	\AddToShipoutPictureFG{
		\AtPageCenter{
			\makebox(0,0){
				\rotatebox{45}{
					\fontsize{180\Q}{180\Q}\selectfont\junL
					\textcolor{red}{サンプル}
				}
			}
		}
	}
}

\@onlypreamble\sampleWaterMark
\makeatother

% 番号付け
\makeatletter
\@addtoreset{equation}{part}
\renewcommand{\theequation}{\arabic{part}.\arabic{equation}}

\@addtoreset{figure}{part}
\renewcommand{\thefigure}{\arabic{part}.\arabic{figure}}

\@addtoreset{table}{part}
\renewcommand{\thetable}{\arabic{part}.\arabic{table}}

\@addtoreset{section}{part}
\renewcommand{\thesection}{\arabic{part}.\arabic{section}}

\@addtoreset{subsection}{part}
\renewcommand{\thesubsection}{\arabic{part}.\arabic{subsection}}

\@addtoreset{column}{part}
\@addtoreset{footnote}{part}

\AtBeginDocument{
	\renewcommand*{\thelstlisting}{\arabic{part}.\arabic{lstlisting}}
	\@addtoreset{lstlisting}{part}
}
\makeatother

\renewcommand{\thepart}{第\arabic{part}章}

% 参照マクロ
\newcommand{\figref}[1]{\mbox{\textbf{図\ref{fig.\arabic{part}.#1}}}}
\newcommand{\figrefex}[2]{\mbox{\textbf{図\ref{fig.#2.#1}}}}
\newcommand{\tableref}[1]{\mbox{\textbf{表\ref{tab.\arabic{part}.#1}}}}
\renewcommand{\eqref}[1]{\mbox{式(\ref{eq.\arabic{part}.#1})}}
\newcommand{\listref}[1]{\mbox{\textbf{リスト\ref{#1}}}}
\newcommand{\figlabel}[1]{\label{fig.\arabic{part}.#1}}
\newcommand{\tablelabel}[1]{\label{tab.\arabic{part}.#1}}
\newcommand{\eqlabel}[1]{\label{eq.\arabic{part}.#1}}
\newcommand{\listlabel}[1]{\label{#1}}
