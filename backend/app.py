from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.ip_tools import (
    get_network_info, 
    summarize_ip_ranges,
    convert_ip_v4_to_v6,
    convert_ip_v6_to_v4
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

if __name__ == '__main__':
    app.run(debug=True) 