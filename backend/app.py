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
    divide_network
)

app = Flask(__name__)
CORS(app)

@app.route('/api/network/calculate', methods=['POST'])
def calculate_network():
    try:
        data = request.json
        ip = data.get('ip')
        mask = data.get('mask')
        
        if not ip or not mask:
            return jsonify({'error': 'IP和掩码不能为空'}), 400
            
        result = get_network_info(ip, mask)
        return jsonify({'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/ip/summary', methods=['POST'])
def summarize_ips():
    try:
        data = request.json
        ip_ranges = data.get('ipRanges', [])
        
        if not ip_ranges:
            return jsonify({'error': 'IP列表不能为空'}), 400
            
        result = summarize_ip_ranges(ip_ranges)
        return jsonify({'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/ip/convert', methods=['POST'])
def convert_ip():
    try:
        data = request.json
        direction = data.get('direction')
        ips = data.get('ips', [])
        ipv6_prefix = data.get('ipv6Prefix', '')
        
        if not ips:
            return jsonify({'error': 'IP列表不能为空'}), 400
            
        if direction == 'v4tov6':
            if not ipv6_prefix:
                return jsonify({'error': 'IPv6前缀不能为空'}), 400
            result = convert_ip_v4_to_v6(ips, ipv6_prefix)
        elif direction == 'v6tov4':
            result = convert_ip_v6_to_v4(ips)
        else:
            return jsonify({'error': '无效的转换方向'}), 400
            
        return jsonify({'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/ip/format', methods=['POST'])
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

@app.route('/network/divide', methods=['POST'])
def divide_subnet():
    try:
        data = request.json
        network = data.get('network')
        divide_type = data.get('divideType')
        value = data.get('value')
        
        if not all([network, divide_type, value]):
            return jsonify({'error': '参数不完整'}), 400
            
        result = divide_network(network, divide_type, value)
        return jsonify({'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 