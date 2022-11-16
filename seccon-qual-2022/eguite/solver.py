from z3 import *

# SECCON{8B228B98E458-5A7B12-8D072F-F9BF1370}

# SECCON{8b228b98e458-5a7b12-8d072f-f9bf1370}

idxs = ["4","10","11","8"]
bl = 256
x4 = BitVec('x4', bl)
x8 = BitVec('x8', bl)
x10 = BitVec('x10', bl)
x11 = BitVec('x11', bl)

xs = [x4,x8,x10,x11]

s = Solver()
s.add(x4 + x10 == 0x8b228bf35f6a)
s.add(x8 + x10 == 0xe78241)
s.add(x11 + x8 == 0xfa4c1a9f)
s.add(x4 + x11 == 0x8b238557f7c8)
s.add(x8 ^ x10 ^ x11 == 0xf9686f4d)
s.check()
m = s.model()
print(m)

for x in xs:
	v = m[x].as_long()
	print(hex(v))
	
"""
        if ((byte *)((long)puVar4 + (long)puVar10) != (byte *)0x8b228bf35f6a) {
          return false;
        }
        if ((byte *)((long)puVar8 + (long)puVar10) != (byte *)0xe78241) {
          return false;
        }
        if ((byte *)((long)puVar11 + (long)puVar8) == (byte *)0xfa4c1a9f) {
          if ((byte *)((long)puVar4 + (long)puVar11) == (byte *)0x8b238557f7c8) {
            return ((ulong)puVar8 ^ (ulong)puVar10 ^ (ulong)puVar11) == 0xf9686f4d;
          }
          return false;
"""
