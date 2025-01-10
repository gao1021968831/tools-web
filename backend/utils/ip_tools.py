import ipaddress
import socket

def get_network_info(ip, mask):
    """计算网络信息"""
    try:
        ip_net = f"{ip}/{mask}"
        net = ipaddress.ip_network(ip_net, strict=False)
        
        return {
            'is_private': net.is_private,
            'network': str(net.with_netmask),
            'network_cidr': f"{net.network_address}/{net.prefixlen}",
            'network_address': str(net.network_address),
            'broadcast_address': str(net.broadcast_address),
            'total_ips': net.num_addresses,
            'usable_ips': net.num_addresses - 2,
            'first_usable': str(net.network_address + 1),
            'last_usable': str(net.broadcast_address - 1),
            'prefix_length': net.prefixlen,
            'netmask': str(net.netmask),
            'hostmask': str(net.hostmask)
        }
    except Exception as e:
        raise ValueError(f"网络计算错误: {str(e)}")

def summarize_ip_ranges(ip_ranges):
    """汇总IP地址"""
    try:
        address_list = []
        for ip_range in ip_ranges:
            if not ip_range.strip():
                continue
            ip_network = ipaddress.ip_network(ip_range.strip(), strict=False)
            for ip in ip_network:
                address_list.append(ip)
                
        address_list = sorted(set(address_list))
        result = []
        
        if address_list:
            start_address = address_list[0]
            end_address = start_address
            
            for address in address_list[1:]:
                if address == end_address + 1:
                    end_address = address
                else:
                    if end_address == start_address:
                        result.append(str(start_address))
                    else:
                        result.append(f"{start_address}-{end_address}")
                    start_address = address
                    end_address = start_address
                    
            if end_address == start_address:
                result.append(str(start_address))
            else:
                result.append(f"{start_address}-{end_address}")
                
        return result
    except Exception as e:
        raise ValueError(f"IP汇总错误: {str(e)}")

def convert_ip_v4_to_v6(ipv4_list, ipv6_prefix):
    """IPv4转IPv6"""
    try:
        result = []
        for ip in ipv4_list:
            if not ip.strip():
                continue
            ipv4 = ipaddress.IPv4Address(ip.strip())
            ipv6 = ipaddress.IPv6Address(ipv6_prefix + str(ipv4))
            result.append(str(ipv6))
        return result
    except Exception as e:
        raise ValueError(f"IPv4转IPv6错误: {str(e)}")

def convert_ip_v6_to_v4(ipv6_list):
    """IPv6转IPv4"""
    try:
        result = []
        for ip in ipv6_list:
            if not ip.strip():
                continue
            ipv4_address = socket.inet_ntoa(socket.inet_pton(socket.AF_INET6, ip.strip())[-4:])
            result.append(ipv4_address)
        return result
    except Exception as e:
        raise ValueError(f"IPv6转IPv4错误: {str(e)}")

def validate_ip_decimal(ip):
    """验证十进制IP地址格式"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            raise ValueError("IP地址必须包含4个部分")
        
        for part in parts:
            num = int(part)
            if num < 0 or num > 255:
                raise ValueError("IP地址每个部分必须在0-255之间")
        return parts
    except ValueError as e:
        raise ValueError(str(e))

def ip_dec_to_bin(ip):
    """十进制IP转二进制"""
    parts = validate_ip_decimal(ip)
    binary_parts = [format(int(part), '08b') for part in parts]
    return '.'.join(binary_parts)

def ip_bin_to_dec(ip):
    """二进制IP转十进制"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            raise ValueError("IP地址必须包含4个部分")
        
        decimal_parts = []
        for part in parts:
            if not all(bit in '01' for bit in part):
                raise ValueError("二进制IP必须只包含0和1")
            if len(part) != 8:
                raise ValueError("每个部分必须是8位二进制数")
            decimal_parts.append(str(int(part, 2)))
        
        return '.'.join(decimal_parts)
    except ValueError as e:
        raise ValueError(str(e))

def ip_dec_to_hex(ip):
    """十进制IP转十六进制"""
    parts = validate_ip_decimal(ip)
    hex_parts = [format(int(part), '02X') for part in parts]
    return '.'.join(hex_parts)

def ip_hex_to_dec(ip):
    """十六进制IP转十进制"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            raise ValueError("IP地址必须包含4个部分")
        
        decimal_parts = []
        for part in parts:
            if not all(c in '0123456789ABCDEFabcdef' for c in part):
                raise ValueError("十六进制IP必须只包含0-9和A-F")
            num = int(part, 16)
            if num < 0 or num > 255:
                raise ValueError("转换后的值必须在0-255之间")
            decimal_parts.append(str(num))
        
        return '.'.join(decimal_parts)
    except ValueError as e:
        raise ValueError(str(e))

def mask_to_cidr(mask):
    """子网掩码转CIDR"""
    try:
        parts = validate_ip_decimal(mask)
        binary = ''.join([format(int(part), '08b') for part in parts])
        
        # 验证掩码格式：必须是连续的1后跟连续的0
        if '01' in binary:
            raise ValueError("无效的子网掩码格式")
        
        return str(binary.count('1'))
    except ValueError as e:
        raise ValueError(str(e))

def cidr_to_mask(cidr):
    """CIDR转子网掩码"""
    try:
        prefix_length = int(cidr)
        if prefix_length < 0 or prefix_length > 32:
            raise ValueError("CIDR必须在0-32之间")
        
        # 生成二进制掩码
        binary = '1' * prefix_length + '0' * (32 - prefix_length)
        
        # 转换为点分十进制
        parts = [
            str(int(binary[i:i+8], 2))
            for i in range(0, 32, 8)
        ]
        
        return '.'.join(parts)
    except ValueError as e:
        raise ValueError(str(e)) 