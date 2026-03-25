
import xmindparser
import pandas as pd


def xmind_to_excel(xmind_file, excel_file):
    # 解析 XMind 文件
    xmind_content = xmindparser.xmind_to_dict(xmind_file)[0]
    sheet_data = []

    # 固定默认值
    important_level = 'P0'
    test_type = '手动'
    default_maintainer = "杨帆"
    default_case_type = "功能测试"
    excel_columns = [
        '模块', '编号', '标题', '维护人', '用例类型',
        '重要程度', '测试类型', '预估工时', '剩余工时',
        '关联工作项', '前置条件', '步骤描述', '预期结果'
    ]

    # 遍历根节点的子节点（模块节点，第2层节点）
    for module_node in xmind_content['topic'].get('topics', []):
        module_name = module_node.get('title', '')

        # 遍历模块节点的子节点（标题节点，第3层节点）
        for title_node in module_node.get('topics', []):
            title = title_node.get('title', '')

            # 初始化所有列默认值
            row_data = {
                '模块': module_name,
                '编号': '',
                '标题': title,
                '维护人': default_maintainer,
                '用例类型': default_case_type,
                '重要程度': important_level,
                '测试类型': test_type,
                '预估工时': '',
                '剩余工时': '',
                '关联工作项': '',
                '前置条件': '',
                '步骤描述': '',
                '预期结果': ''
            }

            # 提取步骤描述（第4层节点）
            step_nodes = title_node.get('topics', [])
            if step_nodes:
                step_description = step_nodes[0].get('title', '')

                # 提取预期结果（第5层节点）
                expect_nodes = step_nodes[0].get('topics', [])
                if expect_nodes and expect_nodes[0].get('title', '').strip():
                    row_data['预期结果'] = expect_nodes[0].get('title', '')
                    row_data['步骤描述'] = step_description
                else:
                    row_data['预期结果'] = step_description
                    row_data['步骤描述'] = ''  # 预期结果存在时步骤描述保留，否则步骤描述转为预期结果

            sheet_data.append([row_data[col] for col in excel_columns])

    # 创建 DataFrame 并保持列顺序
    df = pd.DataFrame(sheet_data, columns=excel_columns)

    # 保存为 Excel 文件
    df.to_excel(excel_file, index=False)

if __name__ == "__main__":
    xmind_file = 'C:/Users/farben/Desktop/123/设备管理/V0.97质控移动端.xmind'
    excel_file = 'D:/test/test_case.xlsx'
    xmind_to_excel(xmind_file, excel_file)
    print(f"XMind 文件已成功转换为 {excel_file}")