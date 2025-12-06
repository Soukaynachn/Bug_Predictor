"""
Complex Python file - Should get HIGH RISK
This has high cyclomatic complexity with many nested conditions
"""

def process_data(data, config, options=None):
    """
    Complex data processing function with many branches
    """
    results = []
    errors = []
    warnings = []
    
    if data is None:
        return None, ["No data provided"]
    
    if not isinstance(data, list):
        data = [data]
    
    for item in data:
        try:
            if config.get('validate', True):
                if not item:
                    warnings.append(f"Empty item: {item}")
                    continue
                    
                if isinstance(item, dict):
                    if 'id' not in item:
                        errors.append(f"Missing ID in {item}")
                        continue
                    
                    if 'value' in item:
                        value = item['value']
                        
                        if isinstance(value, str):
                            if len(value) > 100:
                                warnings.append(f"Value too long: {item['id']}")
                            elif len(value) == 0:
                                errors.append(f"Empty value: {item['id']}")
                            else:
                                if config.get('uppercase', False):
                                    value = value.upper()
                                elif config.get('lowercase', False):
                                    value = value.lower()
                                    
                        elif isinstance(value, (int, float)):
                            if value < 0:
                                if config.get('allow_negative', False):
                                    warnings.append(f"Negative value: {item['id']}")
                                else:
                                    errors.append(f"Negative not allowed: {item['id']}")
                                    continue
                            elif value > 1000000:
                                warnings.append(f"Very large value: {item['id']}")
                                
                        item['processed_value'] = value
                        
                    if options:
                        if 'filter' in options:
                            filter_func = options['filter']
                            if not filter_func(item):
                                continue
                                
                        if 'transform' in options:
                            transform_func = options['transform']
                            try:
                                item = transform_func(item)
                            except Exception as e:
                                errors.append(f"Transform failed for {item.get('id')}: {e}")
                                continue
                    
                    results.append(item)
                    
                elif isinstance(item, (str, int, float)):
                    processed = {'value': item, 'type': type(item).__name__}
                    results.append(processed)
                else:
                    warnings.append(f"Unknown type: {type(item)}")
                    
            else:
                results.append(item)
                
        except KeyError as e:
            errors.append(f"Key error: {e}")
        except ValueError as e:
            errors.append(f"Value error: {e}")
        except TypeError as e:
            errors.append(f"Type error: {e}")
        except Exception as e:
            errors.append(f"Unexpected error: {e}")
    
    if config.get('sort', False):
        try:
            if config.get('sort_key'):
                results.sort(key=lambda x: x.get(config['sort_key'], 0))
            else:
                results.sort()
        except Exception as e:
            warnings.append(f"Sort failed: {e}")
    
    if config.get('deduplicate', False):
        seen = set()
        unique_results = []
        for item in results:
            item_id = item.get('id') if isinstance(item, dict) else str(item)
            if item_id not in seen:
                seen.add(item_id)
                unique_results.append(item)
        results = unique_results
    
    return results, errors, warnings


def validate_config(config):
    """Validate configuration with many checks"""
    if not config:
        return False, "Config is required"
    
    if not isinstance(config, dict):
        return False, "Config must be a dictionary"
    
    required_keys = ['validate', 'sort', 'deduplicate']
    for key in required_keys:
        if key not in config:
            return False, f"Missing required key: {key}"
    
    if config.get('validate'):
        if 'allow_negative' not in config:
            config['allow_negative'] = False
        if 'uppercase' not in config and 'lowercase' not in config:
            config['lowercase'] = True
    
    return True, "Valid"


class DataProcessor:
    """Complex class with many methods and conditions"""
    
    def __init__(self, config):
        self.config = config
        self.cache = {}
        self.stats = {'processed': 0, 'errors': 0, 'warnings': 0}
    
    def process(self, data, options=None):
        is_valid, msg = validate_config(self.config)
        if not is_valid:
            raise ValueError(msg)
        
        results, errors, warnings = process_data(data, self.config, options)
        
        self.stats['processed'] += len(results)
        self.stats['errors'] += len(errors)
        self.stats['warnings'] += len(warnings)
        
        return results
    
    def get_stats(self):
        return self.stats.copy()
    
    def reset_stats(self):
        self.stats = {'processed': 0, 'errors': 0, 'warnings': 0}
