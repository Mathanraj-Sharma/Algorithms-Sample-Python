import sys
from datetime import datetime

MIN = -((2 ** 15) - 1)

def cut_rod(p, n):
	if n == 0:
		return 0
	q = MIN

	# loop runs from 0 to n-1
	for i in range (0,n):
		# n-(i+1) because loop run from 0 instead of 1
		q = max([q, p[i]+cut_rod(p,n-(i+1))])

	return q


def memoized_cut_rod(p, n):
	r = dict()
	#  n+1 because we need a dict from [0....n] 
	for i in range(0,n+1):
		r[i] = MIN
	return memoized_cut_rod_aux(p, n, r)

def memoized_cut_rod_aux(p, n, r):
	q = MIN
	if r[n] >= 0:
		return r[n]
	if n == 0:
		q = 0
	elif q == MIN:
		for i in range(0, n):
			# n-(i+1) because loop run from 0 instead of 1
			q = max([q, p[i]+memoized_cut_rod_aux(p, n-(i+1), r)])
	r[n] = q
	# print(r)
	return q


def bottom_up_cut_rod(p, n):
	r = dict()
	r[0] = 0

	# for subproblem size n=1 to n
	for j in range(1, n+1):
		q = MIN

		# find solution using solutions of subproblems below choosen subproblem
		for i in range(0, j):
			q = max([q, p[i]+r[j-(i+1)]])
		r[j] = q
	return r[n]

def extended_bottom_up_cut_rod(p, n):
	r = dict()
	s = dict()
	r[0] = 0
	s[0] = 0
	# for subproblem size n=1 to n
	for j in range(1,n+1):
		q = MIN

		# find solution using solutions of subproblems below, choosen subproblem
		for i in range(0, j):
			if q < p[i] + r[j-(i+1)]:
				q = p[i]+r[j-(i+1)]
				s[j] = i+1
		r[j] = q
	return r,s

def print_cut_rod_solution(p, n):
	r, s = extended_bottom_up_cut_rod(p,n)
	print('extended_bottom_up_cut_rod outputs: ')
	print('r: ',r)
	print('s: ',s)
	while n > 0:
		print(s[n])
		n -= s[n]


def timeit_wrapper(f, p, n, name):
	start_time = datetime.now()
	print(f'Maximum revenue found using {name}: {f(p, n)}')
	print(f'Excution time of {name}: {(datetime.now() - start_time)}\n')	

if __name__ == '__main__':

	# price list, list is extended from the one in text book to see the time difference when problem size increases 
	p = ([1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 32, 35, 45, 46, 50])
	
	# problem size or rod size
	n = 14

	timeit_wrapper(f=cut_rod, p=p, n=n, name='cut_rod')
	timeit_wrapper(f=memoized_cut_rod, p=p, n=n, name='memoized_cut_rod')
	timeit_wrapper(bottom_up_cut_rod, p, n, 'bottom_up_cut_rod')
	
	print_cut_rod_solution(p, n)