import io
from contextlib import redirect_stdout
import re
import csv
from Journal import ACS, Wiley, Elsevier, RSC, Springer, Nature, APS, mdpi, Taylor, Aip, Science
from Journal import csv_reader

def capture_print_output(func, *args, **kwargs):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args, **kwargs)
    return buffer.getvalue()

# 读取数据
reader = csv_reader.read_csv_input()
reader["file_path"] = r"C:\Users\air14 2020\Desktop\paqu"
reader["file_name"] = "Perovskite1.csv"
reader["url_col"] = 6  # F列的索引
reader["publisher_col"] = 5  # G列的索引
reader["year_col"] = 3  # D列的索引
data = reader["read"](reader)

# 设置输出文件的绝对路径，以便将结果保存到桌面上的一个文件中。
output_file_path = r"C:\Users\air14 2020\Desktop\test\Perovskite11-out.csv"
output_txt_file_path = r"C:\Users\air14 2020\Desktop\test\Perovskite11-out.txt"

# 打开保存结果的文件
with open(output_file_path, "a", encoding="utf-8-sig", newline='') as f, \
     open(output_txt_file_path, "a", encoding="utf-8") as txt_f:
    writer = csv.writer(f)

    # 检查文件是否为空，如果为空，则写入标题行
    if f.tell() == 0:
        writer.writerow(["Paper Title", "Journal Title", "Authors", "Paper DOI", "Paper Abstract", "year"])
        txt_f.write("Paper Title\tJournal Title\tAuthors\tPaper DOI\tPaper Abstract\tyear\n")

    # 遍历数据并根据每个出版商调用对应的方法
    for entry in data:
        url = entry.get('url')
        publisher = entry.get('publisher')
        year = entry.get('year')
        if url and publisher:
            try:
                if publisher == "Wiley Online Library":
                    result = capture_print_output(Wiley.Wiley_function, url)
                elif publisher == "ACS Publications":
                    result = capture_print_output(ACS.ACS_function, url)
                elif publisher == "Elsevier":
                    result = capture_print_output(Elsevier.Elsevier_function, url)
                elif publisher == "pubs.rsc.org":
                    result = capture_print_output(RSC.RSC_function, url)
                elif publisher == "Springer":
                    result = capture_print_output(Springer.Springer_function, url)
                elif publisher == "nature.com":
                    result = capture_print_output(Nature.Nature_function, url)
                elif publisher == "mdpi.com":
                    result = capture_print_output(mdpi.mdpi_function, url)
                elif publisher == "APS":
                    result = capture_print_output(APS.APS_function, url)
                elif publisher == "aip.scitation.org":
                    result = capture_print_output(Aip.Aip_function, url)
                elif publisher == "Taylor &Francis":
                    result = capture_print_output(Taylor.Taylor_function, url)
                elif publisher == "science.org":
                    result = capture_print_output(Science.Science_function, url)
                else:
                    continue

                if result:
                    # 提取论文信息
                    result_dict = {
                        "paper_title": re.search(r"Paper Title: (.+)\n", result).group(1) if re.search(
                            r"Paper Title: (.+)\n", result) else "",
                        "journal_title": re.search(r"Journal Title: (.+)\n", result).group(1) if re.search(
                            r"Journal Title: (.+)\n", result) else "",
                        "authors": re.search(r"Authors: (.+)\n", result).group(1) if re.search(r"Authors: (.+)\n",
                                                                                               result) else "",
                        "paper_doi": re.search(r"DOI: (.+)\n", result).group(1) if re.search(r"DOI: (.+)\n",
                                                                                             result) else "",
                        "paper_abstract": re.search(r"Abstract: (.+)", result).group(1) if re.search(r"Abstract: (.+)",
                                                                                                     result) else "",
                    }

                    # 将结果逐条写入文件并打印到屏幕
                    row = [result_dict["paper_title"], result_dict["journal_title"], result_dict["authors"],
                           result_dict["paper_doi"], result_dict["paper_abstract"], entry.get('year')]
                    writer.writerow(row)
                    print(row)
                    txt_row = "\t".join(row) + "\n"  # 将列表转换为用制表符分隔的字符串
                    txt_f.write(txt_row)  # 将字符串写入 .txt 文件
                    f.flush()  # 立即将缓冲区的数据写入文件
                    txt_f.flush()  # 立即将缓冲区的数据写入 .txt 文件
            except Exception as e:
                # 将错误信息保存到文件并打印到屏幕
                print(f"Error occurred: {e}")
                continue

    # 输出提示信息
    print("文件已成功写入。")
# 在运行完毕后等待一分钟后自动关机
#os.system("shutdown /s /t 60")