from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request, jsonify
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

app = Flask(__name__)
# 配置代理中间件，根据实际的代理层数调整参数
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
CORS(app)

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

if __name__ == '__main__':
    app_logger.info("Application starting...")
    app.run(debug=True) 