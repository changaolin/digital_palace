import asyncio
from palace.memory_palace import MemoryPalace

async def main():
    # 示例数字序列
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    numbers = [879,222,34112]

    generator = MemoryPalace()
    try:
        description = await generator.generate_palace(numbers)
        print("生成的记忆宫殿描述：")
        print(description)
    except Exception as e:
        print(f"生成失败: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())