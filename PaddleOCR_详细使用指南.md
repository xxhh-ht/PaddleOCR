# PaddleOCR 详细使用指南

## 📋 目录
1. [环境准备](#环境准备)
2. [基本OCR使用](#基本ocr使用)
3. [命令行参数详解](#命令行参数详解)
4. [Python API使用](#python-api使用)
5. [文件保存位置说明](#文件保存位置说明)
6. [常见报错及解决方案](#常见报错及解决方案)
7. [性能优化建议](#性能优化建议)
8. [实际应用示例](#实际应用示例)

## 🛠️ 环境准备

### 1. 安装PaddlePaddle框架
```bash
# 安装CPU版本（推荐初学者）
python -m pip install paddlepaddle

# 安装GPU版本（需要CUDA环境）
python -m pip install paddlepaddle-gpu
```

### 2. 安装PaddleOCR
```bash
# 安装基本OCR功能
python -m pip install paddleocr

# 安装完整功能（包含文档解析、信息提取等）
python -m pip install "paddleocr[all]"
```

### 3. 验证安装
```bash
# 验证PaddleOCR是否安装成功
python -c "from paddleocr import PaddleOCR; print('PaddleOCR安装成功！')"
```

## 🚀 基本OCR使用

### 命令行方式处理PDF文件

**完整命令示例：**
```bash
paddleocr ocr -i "/Users/ht-xx/Desktop/福建虚拟电厂项目/1.pdf" \
  --use_doc_orientation_classify False \
  --use_doc_unwarping False \
  --use_textline_orientation False
```

**命令分解说明：**

| 参数 | 说明 | 推荐设置 |
|------|------|----------|
| `ocr` | 指定使用OCR功能 | 必需 |
| `-i "/path/to/file.pdf"` | 输入文件路径 | 必需，支持PDF、图片 |
| `--use_doc_orientation_classify False` | 禁用文档方向分类 | False（加快速度） |
| `--use_doc_unwarping False` | 禁用文档展开 | False（加快速度） |
| `--use_textline_orientation False` | 禁用文本行方向检测 | False（加快速度） |

### 处理不同类型文件

```bash
# 处理单张图片
paddleocr ocr -i "image.jpg" --use_doc_orientation_classify False

# 处理多页PDF
paddleocr ocr -i "document.pdf" --use_doc_orientation_classify False

# 处理文件夹中的所有图片
paddleocr ocr -i "images_folder/" --use_doc_orientation_classify False
```

## 🔧 命令行参数详解

### 核心参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `-i`, `--input` | 字符串 | 必需 | 输入文件或文件夹路径 |
| `--lang` | 字符串 | "ch" | 语言设置：ch(中文)、en(英文)、multi(多语言) |
| `--ocr_version` | 字符串 | "PP-OCRv5" | OCR版本：PP-OCRv3, PP-OCRv4, PP-OCRv5 |
| `--use_doc_orientation_classify` | 布尔 | True | 是否进行文档方向分类 |
| `--use_doc_unwarping` | 布尔 | True | 是否进行文档展开校正 |
| `--use_textline_orientation` | 布尔 | True | 是否进行文本行方向检测 |
| `--enable_mkldnn` | 布尔 | False | 是否启用MKL-DNN加速 |
| `--cpu_threads` | 整数 | 10 | CPU线程数 |
| `--use_angle_cls` | 布尔 | False | 是否使用角度分类 |

### 性能优化参数

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `--use_doc_orientation_classify False` | 禁用文档方向分类，显著提升速度 | False |
| `--use_doc_unwarping False` | 禁用文档展开，提升处理速度 | False |
| `--use_textline_orientation False` | 禁用文本行方向检测 | False |
| `--enable_mkldnn True` | 启用Intel MKL-DNN加速 | True |
| `--cpu_threads 4` | 根据CPU核心数设置 | 4-8 |

## 🐍 Python API使用

### 基本OCR识别

```python
from paddleocr import PaddleOCR

# 初始化OCR引擎（推荐配置）
ocr = PaddleOCR(
    use_doc_orientation_classify=False,  # 禁用文档方向分类
    use_doc_unwarping=False,            # 禁用文档展开
    use_textline_orientation=False,      # 禁用文本行方向检测
    enable_mkldnn=True,                  # 启用MKL-DNN加速
    cpu_threads=4                        # 设置CPU线程数
)

# 执行OCR识别
result = ocr.predict(input="/Users/ht-xx/Desktop/福建虚拟电厂项目/1.pdf")

# 处理结果
for page_idx, res in enumerate(result):
    print(f"第 {page_idx + 1} 页识别结果:")
    print(f"识别到 {len(res.rec_texts)} 个文本区域")
    
    # 保存结果
    res.save_to_img("output")      # 保存可视化图片
    res.save_to_json("output")     # 保存JSON格式结果
    res.save_to_txt("output")      # 保存纯文本结果
```

### 批量处理文件

```python
import os
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_doc_orientation_classify=False)

# 处理文件夹中的所有PDF和图片
input_folder = "/Users/ht-xx/Desktop/福建虚拟电厂项目/"
output_folder = "ocr_results/"

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
        file_path = os.path.join(input_folder, filename)
        print(f"正在处理: {filename}")
        
        result = ocr.predict(input=file_path)
        
        # 为每个文件创建单独的输出文件夹
        file_output = os.path.join(output_folder, filename)
        os.makedirs(file_output, exist_ok=True)
        
        for res in result:
            res.save_to_json(file_output)
            res.save_to_img(file_output)
```

## 📁 文件保存位置说明

### 默认保存位置

| 文件类型 | 保存位置 | 文件名格式 |
|----------|----------|------------|
| 可视化图片 | `output/` | `{原文件名}_ocr_res_img.png` |
| JSON结果 | `output/` | `{原文件名}_res.json` |
| 纯文本 | `output/` | `{原文件名}_res.txt` |
| 模型缓存 | `~/.paddlex/official_models/` | 自动管理 |

### 自定义保存路径

```bash
# 命令行指定输出目录
paddleocr ocr -i "input.pdf" -o "custom_output/" --use_doc_orientation_classify False
```

```python
# Python API指定输出目录
result = ocr.predict(input="input.pdf")
for res in result:
    res.save_to_json("custom_output/")
    res.save_to_img("custom_output/")
```

## 🚨 常见报错及解决方案

### 1. 模型下载失败

**错误信息：**
```
ConnectionError: Failed to download model files
```

**解决方案：**
```bash
# 方法1：设置国内镜像源
export PADDLE_PDX_MODEL_SOURCE=BOS

# 方法2：手动下载模型
# 从 https://github.com/PaddlePaddle/PaddleOCR 手动下载模型文件
# 放置到 ~/.paddlex/official_models/ 目录
```

### 2. 内存不足

**错误信息：**
```
MemoryError: Unable to allocate array with shape...
```

**解决方案：**
```python
# 减小处理图片尺寸
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    det_limit_side_len=960,  # 限制检测图片尺寸
    det_limit_type='max'     # 按最大边限制
)

# 分批处理大文件
def process_large_pdf_in_batches(pdf_path, batch_size=10):
    # 实现分批处理逻辑
    pass
```

### 3. 依赖冲突

**错误信息：**
```
ImportError: cannot import name 'xxx' from 'yyy'
```

**解决方案：**
```bash
# 创建虚拟环境
python -m venv paddleocr_env
source paddleocr_env/bin/activate  # Linux/Mac
# 或 paddleocr_env\Scripts\activate  # Windows

# 重新安装
pip install paddleocr
```

### 4. 处理速度慢

**优化方案：**
```python
ocr = PaddleOCR(
    use_doc_orientation_classify=False,  # 关键优化
    use_doc_unwarping=False,            # 关键优化  
    use_textline_orientation=False,      # 关键优化
    enable_mkldnn=True,                  # Intel CPU加速
    cpu_threads=8,                       # 多线程
    det_limit_side_len=1280              # 限制图片尺寸
)
```

## ⚡ 性能优化建议

### 1. 硬件优化

```python
# GPU加速（需要安装GPU版本）
ocr = PaddleOCR(use_gpu=True)

# CPU多线程优化
ocr = PaddleOCR(
    enable_mkldnn=True,      # Intel MKL-DNN
    cpu_threads=8,           # 根据CPU核心数设置
    use_doc_orientation_classify=False  # 禁用复杂预处理
)
```

### 2. 处理参数优化

```python
# 针对文档的优化配置
ocr = PaddleOCR(
    # 禁用不必要的预处理
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    
    # 性能优化
    enable_mkldnn=True,
    cpu_threads=4,
    
    # 图片尺寸限制
    det_limit_side_len=1280,
    det_limit_type='max'
)
```

### 3. 批量处理优化

```python
import concurrent.futures

def process_single_file(file_path):
    ocr = PaddleOCR(use_doc_orientation_classify=False)
    return ocr.predict(input=file_path)

# 多进程处理多个文件
with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_single_file, file_list))
```

## 📊 实际应用示例

### 处理福建虚拟电厂项目PDF

```python
from paddleocr import PaddleOCR
import json
import os

def process_fujian_vpp_pdf():
    """处理福建虚拟电厂项目PDF文件"""
    
    # 初始化OCR引擎
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        enable_mkldnn=True,
        cpu_threads=4
    )
    
    # 输入文件路径
    pdf_path = "/Users/ht-xx/Desktop/福建虚拟电厂项目/1.pdf"
    output_dir = "福建虚拟电厂项目_OCR结果"
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"开始处理PDF文件: {pdf_path}")
    
    # 执行OCR识别
    results = ocr.predict(input=pdf_path)
    
    # 处理每一页结果
    all_text_content = []
    
    for page_idx, result in enumerate(results):
        print(f"处理第 {page_idx + 1} 页，识别到 {len(result.rec_texts)} 个文本区域")
        
        # 保存每页的可视化结果
        result.save_to_img(output_dir)
        result.save_to_json(output_dir)
        
        # 提取文本内容
        page_text = f"\n=== 第 {page_idx + 1} 页 ===\n"
        for text in result.rec_texts:
            page_text += text + "\n"
        
        all_text_content.append(page_text)
    
    # 保存完整的文本内容
    with open(os.path.join(output_dir, "完整文本内容.txt"), "w", encoding="utf-8") as f:
        f.writelines(all_text_content)
    
    print(f"处理完成！结果保存在: {output_dir}")
    return len(results)

# 执行处理
page_count = process_fujian_vpp_pdf()
print(f"成功处理了 {page_count} 页内容")
```

### 提取关键信息

```python
def extract_key_information(results):
    """从OCR结果中提取关键信息"""
    
    key_info = {
        "项目名称": [],
        "公司信息": [],
        "技术方案": [],
        "投资估算": [],
        "政策依据": []
    }
    
    for result in results:
        for text in result.rec_texts:
            text_lower = text.lower()
            
            # 提取项目名称
            if any(keyword in text_lower for keyword in ["虚拟电厂", "源网荷储"]):
                key_info["项目名称"].append(text)
            
            # 提取公司信息
            if any(keyword in text for keyword in ["科技有限公司", "有限公司", "公司"]):
                key_info["公司信息"].append(text)
            
            # 提取技术方案
            if any(keyword in text_lower for keyword in ["技术方案", "建设方案", "实施方案"]):
                key_info["技术方案"].append(text)
            
            # 提取投资信息
            if any(keyword in text for keyword in ["投资", "万元", "亿元"]):
                key_info["投资估算"].append(text)
            
            # 提取政策依据
            if any(keyword in text_lower for keyword in ["政策", "规划", "通知"]):
                key_info["政策依据"].append(text)
    
    return key_info

# 使用示例
key_info = extract_key_information(results)
for category, items in key_info.items():
    print(f"{category}: {len(items)} 条信息")
```

## 🎯 总结

通过本指南，您可以：

1. **快速上手**：使用简单的命令行或Python代码处理PDF和图片
2. **优化性能**：通过合理的参数配置提升处理速度
3. **解决问题**：应对常见的安装和使用问题
4. **批量处理**：高效处理大量文档
5. **提取信息**：从OCR结果中获取有价值的信息

**关键要点：**
- 使用 `--use_doc_orientation_classify False` 等参数显著提升速度
- 合理设置输出目录管理结果文件
- 针对不同场景调整优化参数
- 及时处理常见的错误信息

现在您可以高效地使用PaddleOCR处理各种文档识别任务了！
