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