#!/usr/bin/env python3
"""
PaddleOCR 本地部署测试脚本
"""

import os
from paddleocr import PaddleOCR

def test_basic_ocr():
    """测试基本OCR功能"""
    print("正在初始化PaddleOCR...")
    
    # 初始化OCR引擎，禁用文档方向分类和文档展开以加快测试速度
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False
    )
    
    print("PaddleOCR初始化成功！")
    
    # 使用示例图片URL进行测试
    test_image_url = "https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png"
    
    print(f"正在对图片进行OCR识别: {test_image_url}")
    
    try:
        # 执行OCR识别
        result = ocr.predict(input=test_image_url)
        
        print("\nOCR识别结果:")
        print("=" * 50)
        
        # 处理并显示结果
        for idx, res in enumerate(result):
            print(f"第 {idx + 1} 页结果:")
            res.print()  # 打印结果
            
            # 保存结果到文件
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            
            res.save_to_img(output_dir)
            res.save_to_json(output_dir)
            
            print(f"结果已保存到 {output_dir} 目录")
        
        print("\n✅ PaddleOCR本地部署测试成功！")
        return True
        
    except Exception as e:
        print(f"❌ OCR识别失败: {e}")
        return False

def test_cli_command():
    """测试命令行功能"""
    print("\n测试命令行功能...")
    try:
        import subprocess
        result = subprocess.run([
            "python", "-m", "paddleocr", "ocr", "--help"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ 命令行功能正常")
            return True
        else:
            print(f"❌ 命令行功能异常: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 命令行测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始PaddleOCR本地部署测试...")
    print("=" * 60)
    
    # 测试基本OCR功能
    ocr_success = test_basic_ocr()
    
    # 测试命令行功能
    cli_success = test_cli_command()
    
    print("\n" + "=" * 60)
    if ocr_success and cli_success:
        print("🎉 PaddleOCR本地部署完全成功！")
        print("您现在可以使用PaddleOCR进行文本识别了。")
    else:
        print("⚠️  PaddleOCR部署存在一些问题，请检查上述错误信息。")
