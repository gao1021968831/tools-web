import os
import shutil
from pdf2docx import Converter
from docx2pdf import convert
from utils.logger import app_logger
import time
import pythoncom  # 导入 pythoncom

class DocConverter:
    def __init__(self, upload_folder='uploads', output_folder='converted'):
        # 创建上传和输出目录
        self.upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), upload_folder)
        self.output_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), output_folder)
        
        # 确保目录存在，但不清空
        for folder in [self.upload_folder, self.output_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def _cleanup_files(self, *files):
        """清理临时文件"""
        for file in files:
            try:
                if file and os.path.exists(file):
                    # 添加重试机制
                    max_retries = 3
                    for i in range(max_retries):
                        try:
                            os.remove(file)
                            app_logger.info(f"Successfully removed file: {file}")
                            break
                        except PermissionError:
                            if i == max_retries - 1:
                                app_logger.warning(
                                    f"Failed to remove file after {max_retries} attempts: {file}")
                            else:
                                app_logger.info(f"Retry {i+1}/{max_retries} to remove file: {file}")
                                time.sleep(1)  # 等待1秒后重试
                else:
                    app_logger.debug(f"File not found for cleanup: {file}")
            except Exception as e:
                app_logger.warning(f"Failed to cleanup file {file}: {str(e)}", exc_info=True)

    def _safe_convert_pdf(self, pdf_file, output_file):
        """安全的PDF转换处理"""
        cv = None
        try:
            cv = Converter(pdf_file)
            cv.convert(output_file, start=0, end=None, pages=None,
                      multi_processing=True,
                      cpu_count=None,
                      tables_settings={
                          'text_settings': {
                              'line_overlap': 0.8,
                              'font_size_detection': True,  # 启用字体大小检测
                              'char_inclusion': 0.9,  # 字符包含阈值
                              'char_distance': 0.3,  # 字符距离阈值
                          },
                          'table_settings': {
                              'min_rows': 1,
                              'min_cols': 1,
                              'edge_min_length': 3,
                              'cell_min_size': 3,
                          }
                      },
                      text_settings={
                          'line_margin': 0.1,
                          'line_overlap': 0.9,
                          'line_break_width': 5,
                          'line_break_free_space_ratio': 0.1,
                          'line_separate_threshold': 5,
                          'line_spacing_threshold': 5,
                          'line_merge_threshold': 2,
                          'line_height_threshold': 2,
                          'line_width_threshold': 2,
                          'line_alignment_threshold': 0.1,
                          'preserve_space': True,  # 保留空格
                          'detect_chinese': True,  # 检测中文
                          'char_merging_threshold': 0.3,  # 字符合并阈值
                      },
                      image_settings={
                          'min_image_area': 100,
                          'max_image_area': None,
                          'min_image_height': 10,
                          'min_image_width': 10,
                      },
                      layout_settings={
                          'section_height': None,
                          'section_width': None,
                          'section_overlap': 0.9,
                          'section_margin': 0.1,
                          'preserve_layout': True,  # 保留布局
                      })
        finally:
            if cv:
                cv.close()

    def pdf_to_docx(self, pdf_file, original_filename):
        """PDF转Word"""
        try:
            if not os.path.exists(pdf_file):
                raise FileNotFoundError("上传的文件不存在")
            
            app_logger.info(f"Starting PDF to DOCX conversion for file: {original_filename}")
            
            # 检查文件大小
            file_size = os.path.getsize(pdf_file)
            app_logger.info(f"PDF file size: {file_size/1024/1024:.2f}MB")
            
            if file_size == 0:
                raise ValueError("文件大小为0，可能是空文件")
            
            # 使用原始文件名（去掉.pdf后缀，添加.docx后缀）
            if original_filename.lower().endswith('.pdf'):
                output_filename = original_filename[:-4] + '.docx'
            else:
                output_filename = original_filename + '.docx'
            
            output_file = os.path.join(self.output_folder, output_filename)
            
            # 使用安全的转换方法
            try:
                self._safe_convert_pdf(pdf_file, output_file)
                
                # 验证输出文件
                if not os.path.exists(output_file):
                    raise Exception("转换失败，未生成输出文件")
                
                output_size = os.path.getsize(output_file)
                if output_size == 0:
                    raise Exception("转换失败，生成的文件为空")
                
                app_logger.info(f"Conversion successful. Output file: {output_filename}, size: {output_size/1024/1024:.2f}MB")
                
                # 不立即删除源文件，等待转换完成后再清理
                return {
                    'status': 'success',
                    'message': '转换成功',
                    'output_file': output_file,
                    'output_filename': output_filename,
                    'source_file': pdf_file  # 记录源文件路径，供后续清理
                }
            except Exception as e:
                app_logger.error(f"PDF conversion error: {str(e)}", exc_info=True)
                raise Exception(f"PDF转换失败: {str(e)}")
            
        except Exception as e:
            app_logger.error(f"PDF to DOCX conversion failed: {str(e)}", exc_info=True)
            raise

    def docx_to_pdf(self, docx_file, original_filename):
        """Word转PDF"""
        try:
            pythoncom.CoInitialize()
            try:
                import win32com.client
                word = win32com.client.Dispatch("Word.Application")
                try:
                    word.Visible = False
                    
                    # 修改文件名处理逻辑
                    base_name = original_filename
                    if base_name.lower().endswith('.docx'):
                        base_name = base_name[:-5]  # 移除 .docx
                    elif base_name.lower().endswith('.doc'):
                        base_name = base_name[:-4]  # 移除 .doc
                    
                    # 确保base_name不为空
                    if not base_name:
                        base_name = "converted"
                        
                    output_filename = f"{base_name}.pdf"
                    app_logger.info(f"Converting to PDF with filename: {output_filename}")  # 添加日志
                    output_file = os.path.join(self.output_folder, output_filename)
                    
                    # 打开文档
                    doc = word.Documents.Open(docx_file)
                    
                    try:
                        # 设置保存选项
                        wdFormatPDF = 17  # PDF 格式
                        
                        # 保存为PDF
                        doc.SaveAs2(output_file, FileFormat=wdFormatPDF)
                    finally:
                        # 关闭文档
                        doc.Close()
                    
                    # 验证输出文件
                    if not os.path.exists(output_file):
                        raise Exception("转换失败，未生成输出文件")
                    
                    output_size = os.path.getsize(output_file)
                    if output_size == 0:
                        raise Exception("转换失败，生成的文件为空")
                    
                    app_logger.info(f"Conversion successful. Output file: {output_filename}, size: {output_size/1024/1024:.2f}MB")
                    
                    return {
                        'status': 'success',
                        'message': '转换成功',
                        'output_file': output_file,
                        'output_filename': output_filename,
                        'source_file': docx_file
                    }
                finally:
                    # 退出 Word
                    word.Quit()
            finally:
                # 确保在完成后取消初始化
                pythoncom.CoUninitialize()
                
        except Exception as e:
            app_logger.error(f"DOCX to PDF conversion failed: {str(e)}", exc_info=True)
            # 清理临时文件
            self._cleanup_files(docx_file)
            if 'output_file' in locals():
                self._cleanup_files(output_file)
            return {
                'status': 'error',
                'message': f'转换失败: {str(e)}'
            } 

    def cleanup_old_files(self, max_age_hours=24):
        """清理旧文件"""
        try:
            current_time = time.time()
            files_cleaned = 0
            for folder in [self.upload_folder, self.output_folder]:
                if os.path.exists(folder):
                    for filename in os.listdir(folder):
                        filepath = os.path.join(folder, filename)
                        if os.path.isfile(filepath):
                            file_age = current_time - os.path.getmtime(filepath)
                            if file_age > (max_age_hours * 3600):
                                try:
                                    self._cleanup_files(filepath)
                                    files_cleaned += 1
                                except Exception as e:
                                    app_logger.error(f"Error cleaning up old file {filepath}: {str(e)}")
            
            app_logger.info(f"Cleaned up {files_cleaned} old files (age > {max_age_hours}h)")
        except Exception as e:
            app_logger.error(f"Error in cleanup_old_files: {str(e)}", exc_info=True) 