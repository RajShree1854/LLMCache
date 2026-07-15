import logging

import LLMCache

FORMAT = '%(asctime)s - %(thread)d - %(filename)s-%(module)s:%(lineno)s - %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT)

llmcache_log = logging.getLogger(f'LLMCache:{LLMCache.__version__}')
