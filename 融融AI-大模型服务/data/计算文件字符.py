import os
import pdfplumber
import tiktoken


def count_tokens_in_pdf(pdf_path, encoding_name="cl100k_base"):
    """
    计算PDF文件中的token数量
    :param pdf_path: PDF文件路径
    :param encoding_name: 使用的编码器（默认cl100k_base，适用于gpt-3.5/4）
    :return: token数量
    """
    total_tokens = 0
    try:
        # 初始化tiktoken编码器
        enc = tiktoken.get_encoding(encoding_name)

        # 打开PDF文件
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # 提取页面文本
                text = page.extract_text()
                if text:
                    # 计算当前页token数并累加
                    tokens = enc.encode(text)
                    total_tokens += len(tokens)
    except Exception as e:
        print(f"处理文件 {pdf_path} 时出错: {str(e)}")
        return 0
    return total_tokens


def main():
    # 设置文件夹路径
    folder_path = "./金融行业知识库"
    total_tokens = 0
    processed_files = 0

    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误: 文件夹 '{folder_path}' 不存在")
        return

    print(f"开始扫描文件夹: {folder_path}")

    # 遍历所有PDF文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            print(f"正在处理: {filename}...", end='', flush=True)

            token_count = count_tokens_in_pdf(file_path)
            total_tokens += token_count
            processed_files += 1

            print(f" 完成! Token数: {token_count:,}")

    # 输出最终统计结果
    print("\n" + "=" * 50)
    print(f"处理完成! 共分析 {processed_files} 个PDF文件")
    print(f"总Token数量: {total_tokens:,}")
    print("=" * 50)


if __name__ == "__main__":
    main()