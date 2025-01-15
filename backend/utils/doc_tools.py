import os
import shutil
from pdf2docx import Converter
import platform
from utils.logger import app_logger
import time

class DocConverter:
    def __init__(self, upload_folder='uploads', output_folder='converted'):
        # 创建上传和输出目录
        self.upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), upload_folder)
        self.output_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), output_folder)
        
        # 确保目录存在
        for folder in [self.upload_folder, self.output_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)
        
        # 检查系统类型
        self.is_windows = platform.system() == 'Windows'
        if not self.is_windows:
            try:
                # 在 Linux 上尝试导入 unoconv
                import subprocess
                result = subprocess.run(['which', 'unoconv'], capture_output=True, text=True)
                if result.returncode != 0:
                    app_logger.warning("unoconv not found. Please install it using: sudo apt-get install unoconv")
            except Exception as e:
                app_logger.error(f"Error checking unoconv: {str(e)}")

    def _cleanup_files(self, *files):
        """清理临时文件"""
        for file in files:
            try:
                if file and os.path.exists(file):
                    max_retries = 3
                    for i in range(max_retries):
                        try:
                            os.remove(file)
                            app_logger.info(f"Successfully removed file: {file}")
                            break
                        except PermissionError:
                            if i == max_retries - 1:
                                app_logger.warning(f"Failed to remove file after {max_retries} attempts: {file}")
                            else:
                                app_logger.info(f"Retry {i+1}/{max_retries} to remove file: {file}")
                                time.sleep(1)
            except Exception as e:
                app_logger.warning(f"Failed to cleanup file {file}: {str(e)}")

    def docx_to_pdf(self, docx_file, original_filename):
        """Word转PDF"""
        try:
            # 处理文件名
            base_name = original_filename
            if base_name.lower().endswith('.docx'):
                base_name = base_name[:-5]
            elif base_name.lower().endswith('.doc'):
                base_name = base_name[:-4]
            
            if not base_name:
                base_name = "converted"
                
            output_filename = f"{base_name}.pdf"
            output_file = os.path.join(self.output_folder, output_filename)
            
            app_logger.info(f"Converting DOCX to PDF: {original_filename} -> {output_filename}")
            
            if self.is_windows:
                # Windows 系统使用 COM
                try:
                    import pythoncom
                    import win32com.client
                    
                    pythoncom.CoInitialize()
                    word = win32com.client.Dispatch("Word.Application")
                    try:
                        word.Visible = False
                        doc = word.Documents.Open(docx_file)
                        doc.SaveAs2(output_file, FileFormat=17)  # 17 = PDF
                        doc.Close()
                    finally:
                        word.Quit()
                        pythoncom.CoUninitialize()
                except Exception as e:
                    app_logger.error(f"Windows COM conversion failed: {str(e)}")
                    raise
            else:
                # Linux 系统使用 unoconv
                try:
                    import subprocess
                    result = subprocess.run(['unoconv', '-f', 'pdf', '-o', output_file, docx_file], 
                                         capture_output=True, text=True)
                    if result.returncode != 0:
                        raise Exception(f"unoconv failed: {result.stderr}")
                except Exception as e:
                    app_logger.error(f"Linux unoconv conversion failed: {str(e)}")
                    raise
            
            # 验证输出文件
            if not os.path.exists(output_file):
                raise Exception("转换失败，未生成输出文件")
            
            output_size = os.path.getsize(output_file)
            if output_size == 0:
                raise Exception("转换失败，生成的文件为空")
            
            app_logger.info(f"Conversion successful. Output file: {output_filename}, size: {output_size/1024:.2f}KB")
            
            return {
                'status': 'success',
                'message': '转换成功',
                'output_file': output_file,
                'output_filename': output_filename,
                'source_file': docx_file
            }
                
        except Exception as e:
            app_logger.error(f"DOCX to PDF conversion failed: {str(e)}", exc_info=True)
            self._cleanup_files(docx_file)
            if 'output_file' in locals():
                self._cleanup_files(output_file)
            return {
                'status': 'error',
                'message': f'转换失败: {str(e)}'
            }

    # PDF 转 Word 的方法保持不变，因为 pdf2docx 库在 Linux 上也能工作
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