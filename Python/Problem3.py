class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root):
        return self.helper(root)

    def helper(self, node):
        if node is None:
            return 0

        left = self.helper(node.left)
        right = self.helper(node.right)

        return max(left, right) + 1