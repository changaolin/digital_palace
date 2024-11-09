from palace.base_llm import BaseLLM

class MemoryPalace:
    def __init__(self):
        self.llm = BaseLLM()

    async def generate_palace(self, numbers: list[int]) -> str:
        # 构建 prompt
        prompt = self._build_prompt(numbers)

        # 调用修改后的 generate 方法，传入 number 参数
        try:
            response = await self.llm.generate(numbers=numbers, prompt=prompt)
            return response
        except Exception as e:
            raise Exception(f"生成记忆宫殿失败: {str(e)}")

    def _build_prompt(self, numbers: list[int]) -> str:
        numbers_str = " ".join(map(str, numbers))
        return f"""请为数字序列 {numbers_str} 创建一个生动、具体且易于记忆的场景描述。

要求：
1. 场景应该是一个连贯的、有逻辑的空间序列
2. 每个数字都要与场景中的具体物体或场景特征对应
3. 使用具象化的描写，包含视觉、听觉等感官细节
4. 场景之间的转换要自然流畅
5. 避免抽象或过于复杂的意象
6. 优先使用常见、容易想象的场景元素

输出格式：
1. 首先给出场景的整体概述（1-2句）
2. 然后按照数字顺序，详细描述每个数字对应的具体场景和记忆关联
3. 最后总结如何通过这个场景序列来记忆这组数字

示例结构：
整体概述：[场景整体描述]

详细场景：
- 数字[X]：[具体场景描述和记忆关联]
- 数字[Y]：[具体场景描述和记忆关联]
...

记忆路线：[如何按顺序回忆这些数字]

请确保描述既生动形象，又便于在头脑中构建3D场景。"""