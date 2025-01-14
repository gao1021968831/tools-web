from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils.ip_tools import (
    get_network_info, 
    summarize_ip_ranges,
    convert_ip_v4_to_v6,
    convert_ip_v6_to_v4,
    ip_dec_to_bin, ip_bin_to_dec,
    ip_dec_to_hex, ip_hex_to_dec,
    mask_to_cidr, cidr_to_mask,
    divide_network, query_ip_location
)
from utils.dns_tools import query_dns_records
from utils.logger import app_logger, api_logger
import time
import os
from werkzeug.utils import secure_filename
from utils.doc_tools import DocConverter
import atexit
import schedule
import threading
import shutil
from urllib.parse import quote

app = Flask(__name__)
# 配置代理中间件，根据实际的代理层数调整参数
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
CORS(app)

# 初始化文档转换器
doc_converter = DocConverter()

# 请求计时中间件
@app.before_request
def before_request():
    request.start_time = time.time()

def get_client_ip():
    """获取真实的客户端IP地址"""
    # 按优先级依次尝试获取
    if request.headers.get('X-Forwarded-For'):
        # 如果有多个IP，取第一个（最原始的客户端IP）
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    client_ip = get_client_ip()
    
    # 扩展的请求信息记录
    request_info = {
        "method": request.method,
        "path": request.path,
        "status_code": response.status_code,
        "duration": f"{duration:.3f}s",
        "client_ip": client_ip,
        "x_forwarded_for": request.headers.get('X-Forwarded-For', '-'),
        "x_real_ip": request.headers.get('X-Real-IP', '-'),
        "host": request.headers.get('Host', '-'),
        "user_agent": request.headers.get('User-Agent', '-'),
        "referer": request.headers.get('Referer', '-')
    }
    
    # 格式化日志消息
    log_message = " | ".join([f"{k}: {v}" for k, v in request_info.items()])
    api_logger.info(log_message)
    
    # 添加必要的响应头
    if response.mimetype == 'application/pdf' or response.mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response

@app.errorhandler(Exception)
def handle_error(error):
    app_logger.error(f"Error occurred: {str(error)}", exc_info=True)
    return jsonify({'error': str(error)}), 500

@app.route('/api/network/calculate', methods=['POST'])
def calculate_network():
    try:
        data = request.json
        ip = data.get('ip')
        mask = data.get('mask')
        
        if not ip or not mask:
            api_logger.warning(f"Invalid input - IP: {ip}, Mask: {mask}")
            return jsonify({'error': 'IP和掩码不能为空'}), 400
            
        result = get_network_info(ip, mask)
        api_logger.info(f"Network calculation successful - IP: {ip}, Mask: {mask}")
        return jsonify({'data': result})
    except Exception as e:
        app_logger.error(f"Network calculation failed - IP: {ip}, Mask: {mask}", exc_info=True)
        return jsonify({'error': str(e)}), 400

@app.route('/api/ip/summary', methods=['POST'])
def summarize_ips():
    try:
        data = request.json
        ip_ranges = data.get('ipRanges', [])
        
        if not ip_ranges:
            api_logger.warning("Empty IP ranges list received")
            return jsonify({'error': 'IP列表不能为空'}), 400
            
        result = summarize_ip_ranges(ip_ranges)
        api_logger.info(f"IP summary successful - Input count: {len(ip_ranges)}, Output count: {len(result)}")
        return jsonify({'data': result})
    except Exception as e:
        app_logger.error("IP summary failed", exc_info=True)
        return jsonify({'error': str(e)}), 400

@app.route('/api/ip/convert', methods=['POST'])
def convert_ip():
    try:
        data = request.json
        direction = data.get('direction')
        ips = data.get('ips', [])
        ipv6_prefix = data.get('ipv6Prefix', '')
        
        if not ips:
            api_logger.warning("Empty IP list for conversion")
            return jsonify({'error': 'IP列表不能为空'}), 400
            
        if direction == 'v4tov6':
            if not ipv6_prefix:
                api_logger.warning("Missing IPv6 prefix for v4tov6 conversion")
                return jsonify({'error': 'IPv6前缀不能为空'}), 400
            result = convert_ip_v4_to_v6(ips, ipv6_prefix)
            api_logger.info(f"IPv4 to IPv6 conversion successful - Count: {len(ips)}")
        elif direction == 'v6tov4':
            result = convert_ip_v6_to_v4(ips)
            api_logger.info(f"IPv6 to IPv4 conversion successful - Count: {len(ips)}")
        else:
            api_logger.warning(f"Invalid conversion direction: {direction}")
            return jsonify({'error': '无效的转换方向'}), 400
            
        return jsonify({'data': result})
    except Exception as e:
        app_logger.error("IP conversion failed", exc_info=True)
        return jsonify({'error': str(e)}), 400

@app.route('/api/ip/format', methods=['POST'])
def format_ip():
    try:
        data = request.get_json()
        convert_type = data.get('type')
        inputs = data.get('inputs', [])

        if not inputs:
            return jsonify({'error': '请输入需要转换的内容'}), 400

        # 根据转换类型调用不同的转换函数
        convert_funcs = {
            'dec2bin': ip_dec_to_bin,
            'bin2dec': ip_bin_to_dec,
            'dec2hex': ip_dec_to_hex,
            'hex2dec': ip_hex_to_dec,
            'mask2cidr': mask_to_cidr,
            'cidr2mask': cidr_to_mask
        }

        if convert_type not in convert_funcs:
            return jsonify({'error': '不支持的转换类型'}), 400

        # 执行转换
        results = []
        for ip in inputs:
            try:
                result = convert_funcs[convert_type](ip.strip())
                results.append(result)
            except ValueError as e:
                return jsonify({'error': f'输入格式错误: {str(e)}'}), 400

        return jsonify({'data': results})

    except Exception as e:
        return jsonify({'error': f'转换失败: {str(e)}'}), 500

@app.route('/api/network/divide', methods=['POST'])
def divide_subnet():
    try:
        data = request.json
        network = data.get('network')
        divide_type = data.get('divideType')
        value = data.get('value')
        
        if not all([network, divide_type, value]):
            api_logger.warning(f"Incomplete parameters - Network: {network}, Type: {divide_type}, Value: {value}")
            return jsonify({'error': '参数不完整'}), 400
            
        result = divide_network(network, divide_type, value)
        api_logger.info(f"Network division successful - Network: {network}, Type: {divide_type}, Value: {value}")
        return jsonify({'data': result})
    except Exception as e:
        app_logger.error(f"Network division failed - Network: {network}", exc_info=True)
        return jsonify({'error': str(e)}), 400

@app.route('/api/ip/location', methods=['POST'])
def get_ip_location():
    try:
        data = request.json
        ips = data.get('ips', [])
        
        if not ips:
            api_logger.warning("Empty IP list for location query")
            return jsonify({'error': 'IP列表不能为空'}), 400
            
        results = []
        for ip in ips:
            result = query_ip_location(ip.strip())
            results.append(result)
            
        api_logger.info(f"IP location query successful - Count: {len(ips)}")
        return jsonify({'data': results})
    except Exception as e:
        app_logger.error("IP location query failed", exc_info=True)
        return jsonify({'error': str(e)}), 400

@app.route('/api/dns/query', methods=['POST'])
def query_dns():
    try:
        data = request.json
        domain = data.get('domain')
        record_types = data.get('types', [])
        
        if not domain:
            api_logger.warning("Empty domain for DNS query")
            return jsonify({'error': '域名不能为空'}), 400
            
        if not record_types:
            api_logger.warning(f"No record types specified for domain: {domain}")
            return jsonify({'error': '记录类型不能为空'}), 400
            
        results = query_dns_records(domain, record_types)
        api_logger.info(f"DNS query successful - Domain: {domain}, Types: {record_types}")
        return jsonify({'data': results})
    except Exception as e:
        app_logger.error(f"DNS query failed - Domain: {domain}", exc_info=True)
        return jsonify({'error': str(e)}), 400

@app.route('/api/ip/current-location', methods=['GET'])
def get_current_ip_location():
    try:
        # 获取客户端真实IP
        client_ip = get_client_ip()
        
        # 查询IP归属地
        result = query_ip_location(client_ip)
        api_logger.info(f"Current IP location query successful - IP: {client_ip}")
        return jsonify({'data': result})
    except Exception as e:
        app_logger.error(f"Current IP location query failed - IP: {client_ip}", exc_info=True)
        return jsonify({'error': str(e)}), 400

@app.route('/api/doc/convert', methods=['POST'])
def convert_document():
    """文档转换接口"""
    try:
        if 'file' not in request.files:
            app_logger.warning("No file uploaded")
            return jsonify({'error': '没有上传文件'}), 400
            
        file = request.files['file']
        if file.filename == '':
            app_logger.warning("No file selected")
            return jsonify({'error': '未选择文件'}), 400
            
        if file:
            # 处理中文文件名
            filename = file.filename
            # 仅对文件名中的特殊字符进行安全处理，保留中文
            safe_filename = "".join([c for c in filename if c.isalnum() or c.isspace() or c in '._-()[]{}中文韩文日文'])
            file_ext = os.path.splitext(filename)[1].lower()
            
            # 记录详细的文件信息
            app_logger.info(f"Processing file conversion request - "
                          f"Original filename: {filename}, "
                          f"Safe filename: {safe_filename}, "
                          f"Extension: {file_ext}, "
                          f"MIME: {file.mimetype}, "
                          f"Size: {file.content_length/1024:.2f}KB")
            
            # 验证文件类型
            valid_pdf = (file_ext == '.pdf' and 
                        (file.mimetype == 'application/pdf' or 
                         file.mimetype == 'application/octet-stream'))
            
            valid_docx = (file_ext == '.docx' and 
                         (file.mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or
                          file.mimetype == 'application/msword' or
                          file.mimetype == 'application/octet-stream'))
            
            if not (valid_pdf or valid_docx):
                app_logger.warning(f"Invalid file type - MIME: {file.mimetype}, Extension: {file_ext}")
                return jsonify({'error': '不支持的文件格式，仅支持PDF和DOCX文件'}), 400
            
            # 保存文件
            file_path = os.path.join(doc_converter.upload_folder, safe_filename)
            file.save(file_path)
            app_logger.info(f"File saved successfully - Path: {file_path}")
            
            try:
                conversion_type = "PDF to DOCX" if valid_pdf else "DOCX to PDF"
                app_logger.info(f"Starting {conversion_type} conversion for file: {safe_filename}")
                
                result = doc_converter.pdf_to_docx(file_path, safe_filename) if valid_pdf else \
                         doc_converter.docx_to_pdf(file_path, safe_filename)
                
                if result['status'] == 'success':
                    app_logger.info(f"Conversion successful - "
                                  f"Input: {safe_filename}, "
                                  f"Output: {result['output_filename']}, "
                                  f"Size: {os.path.getsize(result['output_file'])/1024:.2f}KB")
                    
                    # 对文件名进行 URL 编码
                    encoded_filename = quote(result['output_filename'])
                    
                    response = send_file(
                        result['output_file'],
                        as_attachment=True,
                        download_name=result['output_filename']
                    )
                    
                    # 使用 RFC 5987 编码格式设置 Content-Disposition
                    response.headers['Content-Disposition'] = \
                        f"attachment; filename=\"{encoded_filename}\"; filename*=UTF-8''{encoded_filename}"
                    
                    # 在发送文件后尝试清理
                    @response.call_on_close
                    def cleanup():
                        try:
                            time.sleep(1)  # 等待文件处理完成
                            if 'source_file' in result:
                                doc_converter._cleanup_files(result['source_file'])
                                app_logger.info(f"Cleanup completed for source file: {result['source_file']}")
                        except Exception as e:
                            app_logger.warning(f"Cleanup error: {str(e)}", exc_info=True)
                    
                    return response
                else:
                    app_logger.error(f"Conversion failed - Error: {result['message']}")
                    return jsonify({'error': result['message']}), 500
                    
            except Exception as e:
                app_logger.error(f"Conversion error - File: {safe_filename}, Error: {str(e)}", exc_info=True)
                doc_converter._cleanup_files(file_path)
                raise e
                
    except Exception as e:
        app_logger.error(f"Document conversion failed - Error: {str(e)}", exc_info=True)
        return jsonify({'error': f'文件转换失败: {str(e)}'}), 500

def cleanup_temp_files():
    """清理临时文件"""
    try:
        shutil.rmtree(doc_converter.upload_folder)
        shutil.rmtree(doc_converter.output_folder)
        os.makedirs(doc_converter.upload_folder)
        os.makedirs(doc_converter.output_folder)
        app_logger.info("Temporary files cleaned up")
    except Exception as e:
        app_logger.error(f"Failed to cleanup temporary files: {str(e)}")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# 设置定时清理任务
schedule.every().day.at("00:00").do(cleanup_temp_files)
scheduler_thread = threading.Thread(target=run_schedule)
scheduler_thread.daemon = True
scheduler_thread.start()

# 程序退出时清理
atexit.register(cleanup_temp_files)

if __name__ == '__main__':
    app_logger.info("Application starting...")
    app.run(debug=True) 