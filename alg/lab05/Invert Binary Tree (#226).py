class Solution:
    def invertTree(self, root: TreeNode | None) -> TreeNode | None:
        if not root:
            return None

        # Рекурсивно инвертируем поддеревья
        left_inverted = self.invertTree(root.left)
        right_inverted = self.invertTree(root.right)

        # Меняем местами
        root.left, root.right = right_inverted, left_inverted
        return root