いろいろ調べると `clambc -c flag.cbc` でバイトコードを読みやすくしたものが出力されることが分かるので読む。
`F.0`はエントリポイント、`F.1`では4byteごとに区切って`F.2`を通した結果と定数との比較、`F.2`では4byte文字からのdigest的計算が行われている。
`F.2`をPythonに移植したのち、`F.2`の逆関数を求めて、`F.1`中に残されている定数を逆変換して連結すると`byT3c0d3_1nT3rpr3T3r_1s_4_L0T_0f_fun`になり、flagはこれを包んだ`SECCON{byT3c0d3_1nT3rpr3T3r_1s_4_L0T_0f_fun}`。
ソルバは[solver.py](solver.py)。

