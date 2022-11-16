
def step1(s):
	b = 1
	res = 0
	for c in s:
		c = ord(c)
		for d in range(2):
			res += ((c & 0xf0) >> 4) * b
			c <<= 4 
			b *= 256
	
	return res

arr = """
0x55555555a31e:	0x0405000108090905	0x0108080404050101
0x55555555a32e:	0x0803060108010f09	0x0305020303010108
0x55555555a33e:	0x0904090c0405030f	0x050101070108030b
0x55555555a34e:	0x01030f0a08030606	0x010f010103050806
0x55555555a35e:	0x0501030609040909	0x080e03090501000b
0x55555555a36e:	0x0301060201030105	0x0506080b010f0e08
0x55555555a37e:	0x040a09050501030b	0x0107000c080e0000
0x55555555a38e:	0x030901080301080a	0x0f010e0705060408
0x55555555a39e:	0x010c0306040a020f	0x0e0b00060107050a
0x55555555a3ae:	0x010108030309090d	0x060104070f010406
0x55555555a3be:	0x0a000205010c0501	0x0707050d0e0b040f
0x55555555a3ce:	0x0904090e01010d03	0x0100040a06010607
0x55555555a3de:	0x0c0c05010a000d00	0x0b0f040107070d0e
0x55555555a3ee:	0x01080d0109040f0b	0x010606000100050a
0x55555555a3fe:	0x00070d0c0c0c0e0c	0x07050d0c0b0f030a
0x55555555a40e:	0x04000f0101080203	0x000f050601060202
0x55555555a41e:	0x0c090e0700070d06	0x0f0003020705080b
0x55555555a42e:	0x0804020604000805	0x0d0a000f020d0603
0x55555555a43e:	0x0000000000000000	0x0000000000410000
"""
arr = list(map(lambda d: list(map(lambda v: int(v[2:],16),d.split('\t')[1:])),arr.split('\n')[1:-1]))
arr = sum(arr,[])
# print(list(map(hex,arr)))

def step2(r,arri):
	t2a = 0x04060e01070d030805090b020a0f000c
	v = arr[arri]
	for i in range(8):
		rp = ((r >> (8 * (i * 2))) & 0xf)
		nv = ((v >> (i*8)) & 0xff)  
		k = rp ^ nv 
		kv = ((t2a >> (8 * k)) & 0xff)
		r = r ^ (kv << (8 * (i * 2 + 1)))
	return r

def gen_table():
	rels = [
		(0x40504070c04040402040d040b040f05,
		 0x704040d050404020404050b040c040f),
		(0x9060c060f060e070306010709030a03,
     0x6090701060c0603070e0309060f030a),
    (0x2070e0608030c030203090300060b03,
     0x6020309070e0302030c03000308060b),
    (0x307060503050c0406040e0302060807 ,
     0x503040e07060506030c070204030608),
	]
	
	def tox(v):
		res = []
		for _ in range(16):
			res.append(v & 0xff)
			v >>= 8
		return res
	
	tvs = [-1 for _ in range(16)]
	tvs[1] = 2
	tvs[3] = 6
	tvs[5] = 0
	tvs[7] = 4
	tvs[9] = 10
	tvs[13] = 8
	tvs[14] = 15
	
	for (fr,to) in rels:
		fr = tox(fr)
		to = tox(to)
		# print(fr)
		# print(to)
		for i in range(16):
			if tvs[i] != -1:
				assert(to[i] == fr[tvs[i]])
				continue
			tv = to[i]
			if to.count(tv) > 1:
				# print('possible',i,list(filter(lambda j: fr[j] == tv,range(16))))
				continue
			tvs[i] = fr.index(tv)
	# print(tvs)
	assert(all(map(lambda v: v!=-1,tvs)))
	assert(len(set(tvs)) == 16)
	return tvs
		

def step3(r):
	table = gen_table()
	res = 0
	b = 1
	for i in range(16):
		tk = table[i]
		res += b * ((r >> (tk * 8)) & 0xff)
		b *= 256
	return res

def step4(r):
	br = r
	t2a = 0x04060e01070d030805090b020a0f000c
	t196 = 0x0d0a000f020d0603
	for i in range(8):
		rp = ((r >> (8 * (i * 2))) & 0xf)
		nv = ((t196 >> (i*8)) & 0xff)  
		k = rp ^ nv
		kv = ((t2a >> (8 * k)) & 0xff)
		r = r ^ (kv << (8 * (i * 2 + 1)))
	return r

def step5(r):
	br = r
	b = 1
	res = 0
	for i in range(8):
		v = r & 0xffff
		res |= (((v & 0xff00) >> 8) | ((v & 0xff) << 4)) * b
		r >>= 16
		b *= 256

	return res


def run(flag):
	print('input:',flag)
	assert(len(flag) == 8)
	
	v = step1(flag)
	for i in range(((0x196-0x7e)//8)):
		v = step2(v,i)
		v = step3(v)

	v = step4(v)
	v = step5(v)
	
	print('result',hex(v))
	return v



def rrun(resultv):
	def step1_inv(res):
		s = ''
		for _ in range(8):
			c = (res & 0xf) << 4 | (res & 0xf00) >> 8
			s += chr(c) 
			res >>= 16
		return s
	
	step2_ = step2
	step4_ = step4

	table_3 = gen_table()
	table_3_inv = [-1 for _ in range(16)]
	for i,v in enumerate(table_3):
		table_3_inv[v] = i
	
	def step3_(r):
		res = 0
		b = 1
		for i in range(16):
			tk = table_3_inv[i]
			res += b * ((r >> (tk * 8)) & 0xff)
			b *= 256
		return res
	
	def step5_(r):
		br = r
		b = 1
		res = 0
		for i in range(8):
			v = r & 0xff
			res |= (((v & 0x0f) << 8) | ((v & 0xf0) >> 4)) * b
			r >>= 8
			b *= 256 * 256
		print(hex(br),hex(res))
		return res

	
	def check_inv(f,finv,gen):
		for v in gen:
			tv = f(v)
			rv = finv(tv)
			if rv != v:
				print('finv error',hex(v),'->',hex(tv),'->',hex(rv))
				assert(False)
	
	step1_ = step1_inv
	
	check_inv(step5,step5_,[0x6030f0e])
	check_inv(step4,step4_,[0x6030f0e])
	check_inv(lambda v: step2(v,7),lambda v: step2_(v,7),[0x6030f0e])
	check_inv(step1,step1_,["fewrgee4"])
	check_inv(step3,step3_,[0x6030f0e])
	
	print('sv',hex(resultv))
	v = step5_(resultv)
	v = step4_(v)
	print('invv',hex(step5(step4(resultv))))

	for i in range(((0x196-0x7e)//8))[::-1]:
		v = step3_(v)
		v = step2_(v,i)

	res = step1_inv(v)
	return res


v = run('SECCON{T')
ts = rrun(v)
print(ts)

mvs = [
	0x3ca11fb09e498ab4,
	0xe1fefd554e662f7f,
	0xd853f981df45ab41,
	0xae6575961af354c,
	0x98ba6f1ff3cc98,
	0x5894a5af7f7693b7,
	0x94706b86ce8e1cce,
]
	
for v in mvs:
	print(rrun(v))

# SECCON{TWINE_wr1tt3n_1n_3xc3pt10n_0r13nt3d_pr0gr4mm1ng}

