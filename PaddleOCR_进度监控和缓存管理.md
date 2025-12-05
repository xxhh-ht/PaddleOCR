# PaddleOCR 进度监控和缓存管理指南

## 📊 进度监控方法

### 1. 命令行进度监控

#### 实时进度显示
PaddleOCR在命令行模式下会自动显示处理进度：

```bash
paddleocr ocr -i "/Users/ht-xx/Desktop/福建虚拟电厂项目/1.pdf" \
  --use_doc_orientation_classify False \
  --use_doc_unwarping False \
  --use_textline_orientation False
```

**进度信息解读：**
```
[2025/11/24 20:13:16] paddleocr INFO: Processed item 122 in 11960.133075714111 ms
```
- `Processed item 122` - 表示已处理第122页
- `11960.133075714111 ms` - 该页处理耗时（毫秒）
- 时间戳显示处理的具体时间

#### 进度统计信息
处理过程中会显示：
- 当前处理的页码
- 每页处理耗时
- 累计处理页数
- 处理状态信息

### 2. Python API进度监控

#### 使用回调函数监控进度
```python
from paddleocr import PaddleOCR
import time

class ProgressTracker:
    def __init__(self, total_pages):
        self.total_pages = total_pages
        self.processed_pages = 0
        self.start_time = time.time()
    
    def update_progress(self, page_result):
        self.processed_pages += 1
        elapsed_time = time.time() - self.start_time
        progress_percent = (self.processed_pages / self.total_pages) * 100
        
        print(f"进度: {self.processed_pages}/{self.total_pages} 页 "
              f"({progress_percent:.1f}%) - "
              f"耗时: {elapsed_time:.1f}秒")
        
        # 显示当前页识别结果统计
        if hasattr(page_result, 'rec_texts'):
            text_count = len(page_result.rec_texts)
            print(f"  第 {self.processed_pages} 页识别到 {text_count} 个文本区域")

# 使用进度监控
def process_with_progress(pdf_path):
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False
    )
    
    # 先获取总页数（需要先处理一次）
    temp_results = ocr.predict(input=pdf_path)
    total_pages = len(temp_results)
    
    print(f"文档总页数: {total_pages}")
    
    # 创建进度跟踪器
    tracker = ProgressTracker(total_pages)
    
    # 重新处理并监控进度
    results = ocr.predict(input=pdf_path)
    
    for page_result in results:
        tracker.update_progress(page_result)
    
    return results

# 使用示例
results = process_with_progress("/Users/ht-xx/Desktop/福建虚拟电厂项目/1.pdf")
```

#### 批量处理进度监控
```python
import os
from tqdm import tqdm  # 需要安装: pip install tqdm

def batch_process_with_progress(folder_path):
    ocr = PaddleOCR(use_doc_orientation_classify=False)
    
    # 获取所有PDF文件
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    
    # 使用进度条
    with tqdm(total=len(pdf_files), desc="处理PDF文件") as pbar:
        for pdf_file in pdf_files:
            file_path = os.path.join(folder_path, pdf_file)
            
            try:
                results = ocr.predict(input=file_path)
                pbar.set_postfix({
                    '文件': pdf_file,
                    '页数': len(results)
                })
                
            except Exception as e:
                print(f"处理文件 {pdf_file} 时出错: {e}")
            
            pbar.update(1)
```

## 📁 缓存文件位置说明

### 1. 模型缓存位置

#### 默认模型缓存目录
```
~/.paddlex/official_models/
```

**具体路径示例：**
```bash
# macOS/Linux
/Users/你的用户名/.paddlex/official_models/

# Windows
C:\Users\你的用户名\.paddlex\official_models\
```

#### 查看缓存文件
```bash
# 查看模型缓存目录
ls -la ~/.paddlex/official_models/

# 查看具体模型文件
ls -la ~/.paddlex/official_models/PP-OCRv5_server_det/
```

#### 缓存文件结构
```
~/.paddlex/official_models/
├── PP-OCRv5_server_det/
│   ├── inference.pdiparams
│   ├── inference.pdmodel
│   └── model.yml
├── PP-OCRv5_server_rec/
│   ├── inference.pdiparams
│   ├── inference.pdmodel
│   └── model.yml
├── PP-LCNet_x1_0_textline_ori/
│   └── ...
└── UVDoc/
    └── ...
```

### 2. 临时文件位置

#### 输入文件缓存
```
~/.paddlex/predict_input/
```

**示例：**
```bash
# 查看临时输入文件
ls -la ~/.paddlex/predict_input/
```

#### 输出文件位置
默认输出到当前目录下的 `output/` 文件夹：
```
./output/
├── 原文件名_ocr_res_img.png    # 可视化结果图片
├── 原文件名_res.json           # JSON格式识别结果
└── 原文件名_res.txt            # 纯文本结果
```

### 3. 自定义缓存位置

#### 设置环境变量
```bash
# 设置自定义模型缓存目录
export PADDLE_PDX_MODEL_DIR="/path/to/your/custom/models"

# 设置自定义临时文件目录
export PADDLE_PDX_TEMP_DIR="/path/to/your/temp/files"
```

#### Python代码中设置
```python
import os

# 在代码开始前设置环境变量
os.environ['PADDLE_PDX_MODEL_DIR'] = '/path/to/your/custom/models'
os.environ['PADDLE_PDX_TEMP_DIR'] = '/path/to/your/temp/files'

from paddleocr import PaddleOCR
ocr = PaddleOCR()
```

## 🔧 缓存管理操作

### 1. 清理缓存文件

#### 清理模型缓存
```bash
# 删除所有模型缓存
rm -rf ~/.paddlex/official_models/

# 删除特定模型缓存
rm -rf ~/.paddlex/official_models/PP-OCRv5_server_det/
```

#### 清理临时文件
```bash
# 清理输入文件缓存
rm -rf ~/.paddlex/predict_input/

# 清理输出目录
rm -rf ./output/
```

### 2. 强制重新下载模型

#### 方法1：删除缓存目录
```bash
rm -rf ~/.paddlex/official_models/PP-OCRv5_server_det/
```

#### 方法2：使用Python代码
```python
import shutil
import os

def force_redownload_model(model_name="PP-OCRv5_server_det"):
    """强制重新下载指定模型"""
    model_path = os.path.expanduser(f"~/.paddlex/official_models/{model_name}")
    
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
        print(f"已删除模型缓存: {model_path}")
    
    # 重新初始化会触发重新下载
    from paddleocr import PaddleOCR
    ocr = PaddleOCR()
    return ocr

# 使用示例
ocr = force_redownload_model("PP-OCRv5_server_det")
```

### 3. 缓存状态检查

#### 检查缓存使用情况
```python
import os
import shutil

def check_cache_usage():
    """检查PaddleOCR缓存使用情况"""
    cache_dirs = [
        os.path.expanduser("~/.paddlex/official_models"),
        os.path.expanduser("~/.paddlex/predict_input")
    ]
    
    total_size = 0
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            dir_size = 0
            for dirpath, dirnames, filenames in os.walk(cache_dir):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    dir_size += os.path.getsize(filepath)
            
            total_size += dir_size
            size_mb = dir_size / (1024 * 1024)
            print(f"{cache_dir}: {size_mb:.2f} MB")
    
    total_mb = total_size / (1024 * 1024)
    print(f"总缓存大小: {total_mb:.2f} MB")
    return total_mb

# 检查缓存使用情况
cache_size = check_cache_usage()
```

## 🚀 性能监控和优化

### 1. 处理时间统计

```python
import time
from paddleocr import PaddleOCR

def benchmark_processing(pdf_path):
    """性能基准测试"""
    ocr = PaddleOCR(use_doc_orientation_classify=False)
    
    start_time = time.time()
    results = ocr.predict(input=pdf_path)
    end_time = time.time()
    
    total_time = end_time - start_time
    page_count = len(results)
    avg_time_per_page = total_time / page_count if page_count > 0 else 0
    
    print(f"性能统计:")
    print(f"  总页数: {page_count}")
    print(f"  总耗时: {total_time:.2f} 秒")
    print(f"  平均每页: {avg_time_per_page:.2f} 秒")
    print(f"  处理速度: {page_count/total_time:.2f} 页/秒")
    
    return results

# 运行性能测试
results = benchmark_processing("/Users/ht-xx/Desktop/福建虚拟电厂项目/1.pdf")
```

### 2. 内存使用监控

```python
import psutil
import os

def monitor_memory_usage():
    """监控内存使用情况"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_mb = memory_info.rss / (1024 * 1024)
    
    print(f"当前内存使用: {memory_mb:.2f} MB")
    return memory_mb

# 在OCR处理前后监控内存
memory_before = monitor_memory_usage()
results = ocr.predict(input="document.pdf")
memory_after = monitor_memory_usage()

print(f"内存增加: {memory_after - memory_before:.2f} MB")
```

## 📋 实用脚本

### 完整的进度监控脚本

```python
#!/usr/bin/env python3
"""
PaddleOCR 完整进度监控脚本
"""

import os
import time
import psutil
from paddleocr import PaddleOCR
from tqdm import tqdm

class OCRProgressMonitor:
    def __init__(self):
        self.start_time = None
        self.total_pages = 0
        self.processed_pages = 0
        
    def start_monitoring(self, total_pages):
        self.start_time = time.time()
        self.total_pages = total_pages
        self.processed_pages = 0
        
        print(f"开始处理文档，总页数: {total_pages}")
        print("=" * 50)
    
    def update_progress(self, page_index, page_result):
        self.processed_pages += 1
        
        # 计算进度
        elapsed_time = time.time() - self.start_time
        progress_percent = (self.processed_pages / self.total_pages) * 100
        estimated_total_time = (elapsed_time / self.processed_pages) * self.total_pages
        remaining_time = estimated_total_time - elapsed_time
        
        # 显示进度信息
        print(f"[{page_index+1:3d}/{self.total_pages}] "
              f"进度: {progress_percent:5.1f}% | "
              f"已用: {elapsed_time:6.1f}s | "
              f"剩余: {remaining_time:6.1f}s | "
              f"文本: {len(page_result.rec_texts):3d}个")
    
    def finish_monitoring(self):
        total_time = time.time() - self.start_time
        print("=" * 50)
        print(f"处理完成! 总耗时: {total_time:.1f} 秒")
        print(f"平均速度: {self.total_pages/total_time:.2f} 页/秒")

def process_pdf_with_detailed_monitoring(pdf_path):
    """带详细进度监控的PDF处理"""
    
    # 初始化监控器
    monitor = OCRProgressMonitor()
    
    # 初始化OCR
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        enable_mkldnn=True
    )
    
    # 先获取总页数
    print("正在分析文档结构...")
    temp_results = ocr.predict(input=pdf_path)
    total_pages = len(temp_results)
    
    # 开始监控
    monitor.start_monitoring(total_pages)
    
    # 处理每一页
    results = []
    for page_idx, page_result in enumerate(ocr.predict(input=pdf_path)):
        monitor.update_progress(page_idx, page_result)
        results.append(page_result)
    
    monitor.finish_monitoring()
    return results

# 使用示例
if __name__ == "__main__":
    pdf_path = "/Users/ht-xx/Desktop/福建虚拟电厂项目/1.pdf"
    results = process_pdf_with_detailed_monitoring(pdf_path)
    
    # 保存结果
    output_dir = "detailed_results"
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, res in enumerate(results):
        res.save_to_json(output_dir)
        res.save_to_img(output_dir)
    
    print(f"结果已保存到: {output_dir}")
```

## 🎯 总结

### 进度监控要点：
1. **命令行模式**：自动显示页码和处理时间
2. **Python API**：可使用回调函数或进度条库监控
3. **性能统计**：监控处理速度、内存使用等

### 缓存管理要点：
1. **模型缓存**：`~/.paddlex/official_models/`
2. **临时文件**：`~/.paddlex/predict_input/`
3. **输出文件**：当前目录下的 `output/` 文件夹
4. **自定义路径**：通过环境变量设置

### 实用技巧：
- 定期清理缓存以释放磁盘空间
- 监控处理进度避免长时间等待
- 使用性能统计优化处理参数
- 设置自定义缓存目录便于管理

通过这些方法，您可以更好地了解PaddleOCR的处理进度并有效管理缓存文件。
