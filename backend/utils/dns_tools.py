import dns.resolver
import dns.reversename
from dns.exception import DNSException
import concurrent.futures
import threading
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建线程本地存储的解析器
thread_local = threading.local()

def get_resolver():
    """获取线程本地的DNS解析器"""
    if not hasattr(thread_local, 'resolver'):
        thread_local.resolver = dns.resolver.Resolver()
        # 设置超时时间
        thread_local.resolver.timeout = 3
        thread_local.resolver.lifetime = 3
        # 使用可靠的DNS服务器
        thread_local.resolver.nameservers = [
            '8.8.8.8',  # Google DNS
            '1.1.1.1',  # Cloudflare DNS
            '223.5.5.5'  # AliDNS
        ]
    return thread_local.resolver

def query_single_record(domain, record_type):
    """查询单个DNS记录"""
    try:
        logger.info(f"开始查询 {domain} 的 {record_type} 记录")
        resolver = get_resolver()
        answers = resolver.resolve(domain, record_type)
        records = []
        
        for rdata in answers:
            if record_type == 'MX':
                value = f"{rdata.preference} {rdata.exchange}"
            elif record_type == 'SOA':
                value = f"{rdata.mname} {rdata.rname} {rdata.serial}"
            else:
                value = str(rdata)
                
            records.append({
                'name': domain,
                'type': record_type,
                'value': value,
                'ttl': answers.ttl
            })
            
        logger.info(f"成功查询到 {len(records)} 条 {record_type} 记录")
        return {
            'type': record_type,
            'records': records
        }
                
    except dns.resolver.NXDOMAIN:
        logger.warning(f"域名 {domain} 不存在")
        return {
            'type': record_type,
            'records': [{
                'name': domain,
                'type': record_type,
                'value': '域名不存在',
                'ttl': 0
            }]
        }
    except dns.resolver.NoAnswer:
        logger.warning(f"域名 {domain} 没有 {record_type} 记录")
        return {
            'type': record_type,
            'records': [{
                'name': domain,
                'type': record_type,
                'value': f'没有 {record_type} 记录',
                'ttl': 0
            }]
        }
    except dns.resolver.Timeout:
        logger.error(f"查询 {domain} 的 {record_type} 记录超时")
        return {
            'type': record_type,
            'records': [{
                'name': domain,
                'type': record_type,
                'value': '查询超时',
                'ttl': 0
            }]
        }
    except DNSException as e:
        logger.error(f"DNS查询异常: {str(e)}")
        return {
            'type': record_type,
            'records': [{
                'name': domain,
                'type': record_type,
                'value': f'查询失败: {str(e)}',
                'ttl': 0
            }]
        }
    except Exception as e:
        logger.error(f"未知错误: {str(e)}")
        return {
            'type': record_type,
            'records': [{
                'name': domain,
                'type': record_type,
                'value': f'查询错误: {str(e)}',
                'ttl': 0
            }]
        }

def query_dns_records(domain, record_types):
    """并发查询多个DNS记录"""
    logger.info(f"开始查询域名 {domain} 的记录: {record_types}")
    results = []
    
    # 使用线程池并发查询
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(record_types), 3)) as executor:
        future_to_type = {
            executor.submit(query_single_record, domain, record_type): record_type
            for record_type in record_types
        }
        
        # 收集结果
        for future in concurrent.futures.as_completed(future_to_type):
            try:
                result = future.result()
                if result and result.get('records'):
                    results.append(result)
            except Exception as e:
                record_type = future_to_type[future]
                logger.error(f"处理查询结果时出错: {str(e)}")
                results.append({
                    'type': record_type,
                    'records': [{
                        'name': domain,
                        'type': record_type,
                        'value': f'查询异常: {str(e)}',
                        'ttl': 0
                    }]
                })
    
    # 按记录类型排序
    results.sort(key=lambda x: record_types.index(x['type']))
    logger.info(f"查询完成，共获取 {len(results)} 种记录")
    return results 