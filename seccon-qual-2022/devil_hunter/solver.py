
def f(s):
	v = 0xacab3c0
	for c in s:
		tv = v ^ ord(c)
		tv2 = (v >> 0x18) | (tv << 8)
		tv2 &= 0xffffffff
		v = tv2
	return v

v = 0x739e80a2

# first: 0x739e80a2
# last:  0x6cbfdd9f
v = "SECC"[::-1]
print(hex(f(v)))


ans = ""
def g(x):
	global ans
	v = 0xacab3c0
	for _ in range(1):
		cs = []
		for i in range(4)[::-1]:
			v1 = (v >> (i * 8)) & 0xff
			v2 = (x >> (i * 8)) & 0xff
			#print(hex(v1),hex(v2),chr(v1 ^ v2))
			cs.append(v1 ^ v2)
		
		cs = cs[3:] + cs[:3]
		for c in cs:
			print(chr(c))
			ans += chr(c)
		v = ((v >> 0x18) | (v << 8)) & 0xffffffff
	print('=====')

xs = [
	0x739e80a2,
	0x3aae80a3,
	0x3ba4e79f,
	0x78bac1f3,
	0x5ef9c1f3,
	0x3bb9ec9f,
	0x558683f4,
	0x55fad594,
	0x6cbfdd9f
]

for x in xs:
	g(x)

print(ans)

