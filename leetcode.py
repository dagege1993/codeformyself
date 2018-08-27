# class Solution(object):
# 	def multiply(self, num1, num2):
# 		"""
# 		:type num1: str
# 		:type num2: str
# 		:rtype: str
# 		"""
# 		num1, num2 = num1[::-1], num2[::-1]
# 		res = [0] * (len(num1) + len(num2))
# 		for i in xrange(len(num1)):
# 			for j in xrange(len(num2)):
# 				res[i + j] += int(num1[i]) * int(num2[j])
# 				res[i + j + 1] += res[i + j] / 10
# 				res[i + j] %= 10
#
# 		# Skip leading 0s.
# 		i = len(res) - 1
# 		while i > 0 and res[i] == 0:
# 			i -= 1
#
# 		return ''.join(map(str, res[i::-1]))
#
#
# if __name__ == "__main__":
# 	print(Solution().multiply("123", "1000"))

class Solution:
	# @param A, a list of integers
	# @return an integer
	def trap(self, A):
		result = 0
		top = 0
		for i in range(len(A)):
			if A[top] < A[i]:
				top = i
		
		second_top = 0
		for i in range(top):
			if A[second_top] < A[i]:
				second_top = i
			result += A[second_top] - A[i]
		
		second_top = len(A) - 1
		for i in reversed(range(top, len(A))):
			if A[second_top] < A[i]:
				second_top = i
			result += A[second_top] - A[i]
		
		return result


class Solution2:
	# @param A, a list of integers
	# @return an integer
	def trap(self, A):
		result = 0
		stack = []
		
		for i in xrange(len(A)):
			mid_height = 0
			while stack:
				[pos, height] = stack.pop()
				result += (min(height, A[i]) - mid_height) * (i - pos - 1)
				mid_height = height
				
				if A[i] < height:
					stack.append([pos, height])
					break
			stack.append([i, A[i]])
		
		return result


if __name__ == "__main__":
	print(Solution().trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
