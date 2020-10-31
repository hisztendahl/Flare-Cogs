def mergeDict(self, dict1, dict2):
    """Merge dictionaries and keep values of common keys in list"""
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            try:
                dict3[key] = value + dict1[key]
            except TypeError:
                self.log.info(f"Error merging dicts. {value} + {dict1[key]}")
    return dict3
