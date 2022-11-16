tss = ""

gdb.execute('handle SIGSEGV pass')


# >>> b'SECCON{T'.hex()
# '534543434f4e7b54'

def setbreak(s):
	s = gdb.execute('b* %s' % s,to_string=True)
	i = s.split(' ')[1]
	return int(i)

def rembreak(i):
	gdb.execute('d %d' % i)


qmask = 0xffffffffffffffff

def showrcdx(res):
	res = ((res >> 64) & qmask, res & qmask)
	return ('rcx',hex(res[0]),'rdx',hex(res[1]))

def step1(s):
	b = 1
	res = 0
	for c in s:
		c = ord(c)
		for d in range(2):
			res += ((c & 0xf0) >> 4) * b
			c <<= 4 
			b *= 256
	
	print('step1',s,'->',showrcdx(res))
	
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
print(list(map(hex,arr)))
# exit()
"""
gdb-peda$ x/10xg $rbp+0x2a
0x55555555a2ca:	0x04060e01070d030805090b020a0f000c
"""

def step2(r,arri):
	t2a = 0x04060e01070d030805090b020a0f000c
	v = arr[arri]
	print('arrv',hex(v))
	for i in range(8):
		rp = ((r >> (8 * (i * 2))) & 0xf)
		nv = ((v >> (i*8)) & 0xff)  
		k = rp ^ nv 
		kv = ((t2a >> (8 * k)) & 0xff)
		print(hex(nv),hex(k),hex(kv))
		r = r ^ (kv << (8 * (i * 2 + 1)))
		print(hex(r)) 
	print('step2','->',showrcdx(r))
	return r

"""
49036b21
df85eca7
"""

"""
c18be3a9
570d642f
"""

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
		
		

# c18be3a9570d642f
def step3(r):
	table = gen_table()
	# table = "49036b21df85eca7"
	# table = list(map(lambda c: int(c,16),table))
	#print(hex(r))
	res = 0
	b = 1
	for i in range(16):
		tk = table[i]
		res += b * ((r >> (tk * 8)) & 0xff)
		b *= 256
	print('step3',showrcdx(r),'->',showrcdx(res))
	return res


"""
	gdb-peda$ x/10xg $rbp+0x196
	0x55555555a436:		0x0000000000000000
"""
def step4(r):
	br = r
	t2a = 0x04060e01070d030805090b020a0f000c
	t196 = 0x0d0a000f020d0603
	for i in range(8):
		rp = ((r >> (8 * (i * 2))) & 0xf)
		nv = ((t196 >> (i*8)) & 0xff)  
		k = rp ^ nv
		kv = ((t2a >> (8 * k)) & 0xff)
		print(hex(nv),hex(k),hex(kv))
		r = r ^ (kv << (8 * (i * 2 + 1)))
		print(hex(r)) 
	print('step4',showrcdx(br),'->',showrcdx(r))
	return r

def step5(r):
	br = r
	b = 1
	res = 0
	for i in range(8):
		v = r & 0xffff
		print(hex(v))
		res |= (((v & 0xff00) >> 8) | ((v & 0xff) << 4)) * b
		r >>= 16
		b *= 256
	
	print('step5',showrcdx(br),'->','rsi',hex(res))
	return res

def run():
	print('run =================================')
	flag = 'SECCON{TWINE_wr1tt3n_1n_3xc3pt10n_0r13nt3d_pr0gr4m}AAAA'
	# flag = "wf3GGXZy3"
	# flag = 'AAAAAAAA'+ 'X' + 'A' * 36
	gdb.execute('handle SIGSEGV stop')
	gdb.execute('r ' + flag )
	for _ in range(10):
		gdb.execute('c')

	gdb.execute('handle SIGSEGV nostop')

	shows = []
	def stopshow(diff,regs):
		def f():
			i = setbreak('heart+%d' % diff)
			gdb.execute('c',to_string=True)
			print('heart+' + str(diff))
			for reg in regs:
				print(reg)
				gdb.execute('i r %s' % reg)
			rembreak(i)
		shows.append(f)
	
	def pshow(s):
		def f():
			print(s)
		shows.append(f)
	
	def setf(f):
		shows.append(f)
	
	pshow("first step ================================")

	stopshow(1005,['rax'])
	stopshow(1017,['rdx'])

	stopshow(1023,['rax'])
	stopshow(1068,['rdx'])

	stopshow(1084,['rax'])
	stopshow(1125,['rdx'])

	stopshow(1141,['rax'])
	stopshow(1182,['rdx'])

	stopshow(1188,['rax'])
	stopshow(1204,['rcx'])

	stopshow(1210,['rax'])
	stopshow(1247,['rcx'])

	stopshow(1253,['rax'])
	stopshow(1286,['rcx'])

	stopshow(1292,['rax'])
	stopshow(1325,['rcx'])
	
	rcxrdx = 0
	def f():
		nonlocal rcxrdx
		rcxrdx = step1(flag[:8])
	setf(f)
	
	pshow("second step ============================================================")

	stopshow(1356,['r14'])
	stopshow(1366,['r14','rax'])
	stopshow(1371,['rax'])
	stopshow(1373,['rdx'])

	stopshow(1414,['rdx'])
	
	stopshow(1428,['rax'])
	stopshow(1431,['rax'])
	stopshow(1438,['r14'])
	stopshow(1443,['r14'])
	stopshow(1460,['rdx'])
	
	stopshow(1498,['rdx'])
	# stopshow(1366,['r14','rax'])
	# stopshow(1371,['rax'])
	# stopshow(1373,['rdx'])

	stopshow(1521,['rcx'])
	stopshow(1561,['rcx'])
	stopshow(1608,['rcx'])
	stopshow(1646,['rdx','rcx'])

	def f():
		nonlocal rcxrdx
		rcxrdx = step2(rcxrdx,0)
	setf(f)

	pshow("third step ============================================================")
	stopshow(1647,['rcx','rdx'])

	stopshow(1839,['rcx','rdx','rip'])
	
	def f():
		nonlocal rcxrdx
		rcxrdx = step3(rcxrdx)
	setf(f)
	"""
	stopshow(1836,[])
	stopshow(1839,['rdx','rcx'])
	def f():
		nonlocal rcxrdx
		rcxrdx = step2(rcxrdx,1)
		rcxrdx = step3(rcxrdx)
	setf(f)
	"""
	
	def f():
		nonlocal rcxrdx
		for i in range(1,((0x196-0x7e)//8)):
			rcxrdx = step2(rcxrdx,i)
			rcxrdx = step3(rcxrdx)
	setf(f)

	stopshow(1853,['rdx','rcx','rip'])
	def f():
		print('finally',showrcdx(rcxrdx))
	setf(f)
	
	pshow("forth step ============================================================")
	# stopshow(1853,['rcx','rdx'])
	stopshow(1860,['rax'])
	stopshow(1869,['rsi'])

	stopshow(1876,['rcx','rdx'])
	stopshow(1919,['rcx','rdx'])
	stopshow(1962,['rcx','rax'])

	stopshow(2150,['rdx','rax'])
	

	def f():
		nonlocal rcxrdx
		rcxrdx = step4(rcxrdx)
	setf(f)
	
	pshow("fifth step ============================================================")
	
	stopshow(2379,['rsi'])
	stopshow(2382,['rsi'])
	

	def f():
		nonlocal rcxrdx
		rcxrdx = step5(rcxrdx)
	setf(f)

	stopshow(2379,['rdx','rsi'])
	stopshow(2382,['rdx'])
	
	stopshow(2379,['rdx','rsi'])
	stopshow(2382,['rdx'])

	stopshow(2379,['rdx','rsi'])
	stopshow(2382,['rdx'])

	stopshow(2379,['rdx','rsi'])
	stopshow(2382,['rdx'])

	stopshow(2379,['rdx','rsi'])
	stopshow(2382,['rdx'])

	stopshow(2379,['rdx','rsi'])
	stopshow(2382,['rdx'])
	
	for s in shows:
		s()
	

		
	#gdb.execute('b* heart+2416')
	
	"""
	# gdb.execute('b* heart+2335')
	gdb.execute('b* heart+1647')
	gdb.execute('b* heart+1839')
	# gdb.execute('b* heart+2346')
	# gdb.execute('b* heart+2346')
	# gdb.execute('b* heart+2399')
	# gdb.execute('b* heart+2460')
	gdb.execute('c')

	gdb.execute('c')
	print('rcx')
	gdb.execute('i r rcx')
	print('rsi')
	gdb.execute('x/10xg $rsi')
	print('r12')
	gdb.execute('x/10xg $r12')
	"""

run()

