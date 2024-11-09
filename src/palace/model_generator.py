from typing import List, Optional
from openai import AsyncOpenAI
from PIL import Image
import io
import base64

class ModelGenerator:
    def __init__(self, client: AsyncOpenAI):
        self.client = client

    async def generate_scene_image(self, description: str) -> str:
        """根据场景描述生成图片"""
        try:
            # 构建DALL-E的prompt
            image_prompt = f"""
            Create a detailed 3D visualization of this memory palace scene:
            {description}
            Style: 3D rendering, architectural visualization, detailed, realistic
            """

            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )

            return response.data[0].url

        except Exception as e:
            raise Exception(f"场景图片生成失败: {str(e)}")

    def prepare_3d_instructions(self, description: str) -> dict:
        """准备3D模型生成说明"""
        return {
            "scene_description": description,
            "recommended_tools": [
                {
                    "name": "Blender",
                    "instructions": "使用Blender的程序化建模功能创建场景",
                    "steps": [
                        "创建新场景",
                        "使用基础几何体搭建主要结构",
                        "添加材质和纹理",
                        "设置光照",
                        "渲染场景"
                    ]
                },
                {
                    "name": "Unity",
                    "instructions": "使用Unity创建可交互的3D场景",
                    "steps": [
                        "导入基础资源",
                        "搭建场景结构",
                        "添加材质和光照",
                        "设置漫游相机",
                        "构建应用"
                    ]
                }
            ],
            "export_formats": ["FBX", "GLTF", "OBJ"]
        } 