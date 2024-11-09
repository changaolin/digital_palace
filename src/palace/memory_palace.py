from .base_llm import BaseLLM
import aiohttp

class MemoryPalace:
    def __init__(self):
        self.llm = BaseLLM()

    async def generate_palace(self, numbers: list[int]) -> dict:
        """生成记忆宫殿及其相关资源"""
        try:
            # 1. 构建 prompt
            prompt = self._build_prompt(numbers)

            # 2. 检查缓存
            cached_result = self.llm.db_service.get_full_cached_response(numbers, prompt)
            if cached_result:
                return cached_result
            # 3. 生成文字描述
            description = await self.llm.generate(numbers=numbers, prompt=prompt)

            # 4. 生成场景图片
            image_data = await self._generate_scene_image(description)

            # 5. 保存描述和图片
            result = self.llm.db_service.save_response_with_model(
                numbers=numbers,
                prompt=prompt,
                response=description,
                model_data=image_data,
                model_type="image",
                file_format="png"
            )

            return {
                "description": result["response"],
                "image_path": result["model_path"],
                "numbers": numbers
            }

        except Exception as e:
            raise Exception(f"生成记忆宫殿失败: {str(e)}")

    async def _generate_scene_image(self, description: str) -> bytes:
        """生成场景图片"""
        try:
            image_prompt = f"""
            Create a detailed 3D visualization of this memory palace scene:
            {description}
            Style: 3D rendering, architectural visualization, detailed, realistic
            """

            response = await self.llm.client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )

            # 获取图片数据
            image_url = response.data[0].url
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    image_data = await response.read()
                    return image_data

        except Exception as e:
            raise Exception(f"场景图片生成失败: {str(e)}")

    def _build_prompt(self, numbers: list[int]) -> str:
        """构建提示词"""
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