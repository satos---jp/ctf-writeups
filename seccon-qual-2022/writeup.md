## eguite

RustでコンパイルされたらしいGUIプログラム。`eguite::Crackme::onclick` がそれらしい名前なので読んでみる。

冒頭の部分からflagが43文字であること、`SECCON{`のチェックをしていることが分かる。

途中はよく分からないので読み飛ばすと、最後のほうに謎の連立方程式を解いているので、[solver.py](eguite/solver.py)のようにして値を逆算する。

`if (uVar9 != 0x2d) {`のように途中で比較していることから区切り文字が`-`であると当たりをつけて数パターン試してみるとflagが`SECCON{8b228b98e458-5a7b12-8d072f-f9bf1370}`であることが分かる。


## Devil Hunter

いろいろ調べると `clambc -c flag.cbc` でバイトコードを読みやすくしたものが出力されることが分かるので読む。

`F.0`はエントリポイント、`F.1`では4byteごとに区切って`F.2`を通した結果と定数との比較、`F.2`では4byte文字からのdigest的計算が行われている。

`F.2`をPythonに移植したのち、`F.2`の逆関数を求めて、`F.1`中に残されている定数を逆変換して連結すると`byT3c0d3_1nT3rpr3T3r_1s_4_L0T_0f_fun`になり、flagはこれを包んだ`SECCON{byT3c0d3_1nT3rpr3T3r_1s_4_L0T_0f_fun}`。

ソルバは[solver.py](devil_hunter/solver.py)。

## eldercmp

プログラムを動的実行すると`hlt`まみれの`heart`関数に実行が飛び、sigactionによって`SIGSEGV`が飛ぶたびに`trampoline`関数に実行が飛ばされていることが分かる。

`heart`関数では、入力を8byteに区切って、5種類の変換を行ったのち、保存されている定数と比較している。

調べると`handle SIGSEGV pass`と`handle SIGSEGV nostop`を実行することででgdb上でも止まらずに実行できることが分かるので、これを用いて入力の変換動作を同時シミュレーションして突き合わせる[gdbscript.py](eldercmp/gdbscript.py)を書き、変換をPythonでシミュレートする関数`step1`~`step5`を実装する。

あとは`step1`~`step5`の逆関数を[solver.py](eldercmp/solver.py)で実装して、比較している定数テーブルの値を逆変換して連結するとflagが`SECCON{TWINE_wr1tt3n_1n_3xc3pt10n_0r13nt3d_pr0gr4m}`と分かる。

