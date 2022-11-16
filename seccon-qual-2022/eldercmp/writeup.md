プログラムを動的実行すると`hlt`まみれの`heart`関数に実行が飛び、sigactionによって`SIGSEGV`が飛ぶたびに`trampoline`関数に実行が飛ばされていることが分かる。

`heart`関数では、入力を8byteに区切って、5種類の変換を行ったのち、保存されている定数と比較している。

調べると`handle SIGSEGV pass`と`handle SIGSEGV nostop`を実行することででgdb上でも止まらずに実行できることが分かるので、これを用いて入力の変換動作を同時シミュレーションして突き合わせる[gdbscript.py](gdbscript.py)を書き、変換をPythonでシミュレートする関数`step1`~`step5`を実装する。

あとは`step1`~`step5`の逆関数を[solver.py](solver.py)で実装して、比較している定数テーブルの値を逆変換して連結するとflagが`SECCON{TWINE_wr1tt3n_1n_3xc3pt10n_0r13nt3d_pr0gr4m}`と分かる。
