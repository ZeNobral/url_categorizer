from collections import namedtuple
#--------------------------------------------------------------------------------------------------
# CLASS NodeVisitor
# Base Class used by NodeEvaluator to evaluate the rule Tree
# based on Generators and Coroutines
#--------------------------------------------------------------------------------------------------		
class NodeVisitor:
	def __init__(self, node):
		self.node = node

	def visit(self, node):
		stack = [node]
		lnode_result = None
		while stack: 
			try:
				lnode = stack[-1]
				if isinstance (lnode, types.GeneratorType):
					stack.append (lnode.send(lnode_result))
					lnode_result = None
				elif isinstance(lnode, Node):
					stack.append(self._visit(stack.pop()))
				else:
					lnode_result = stack.pop()
			except StopIteration:
				stack.pop()
		return lnode_result

	def _visit(self, node):
		methname = 'visit_' + node.type
		meth = getattr(self, methname, None)
		if meth is None:
			meth = self._generic_visit
		return meth(node)
	
	def _generic_visit(self, node):
	 raise RuntimeError('No {} method'.format('visit_' + node.type))


#--------------------------------------------------------------------------------------------------
# CLASS NodeEvaluator
# evaluate an Url against the rule Tree
#--------------------------------------------------------------------------------------------------	 
class NodeEvaluator(nodeVisitor):
	Url = namedtuple('Url', 'url scheme hostname path query pathquery')
	
	def __init__(self, node):
		super().__init__(node)
		self.result_stack = []
		self.url = None
		
	def evaluate_url(self, url):
		parsed = urlparse(url)
		pathquery = parsed.path
		if parsed.query:
			pathquery += '?' + parsed.query
		self.url = self.Url(url, parsed.scheme, parsed.hostname, parsed.path, parsed.query, pathquery)
		self.visit(self.node)

	def get_url_component(self, cpt):
		if cpt in ('host', 'hostname', 'domain'):
			return self.url.hostname
		if cpt in ('proto', 'protocol', 'scheme'):
			return self.url.scheme
		else:
			return getattr(self.url,cpt)

	def visit_begin(self, node):
		segments = []
		for child in node.childs:
			segment = self.visit(child)
			segments.append(segment)
		print(self.get_url_component('url'),*segments, sep=';')
			
	def visit_segment(self, node):
		for child in node.childs:
			category_name = self.visit(child)
			if category_name:
				yield (node.value, category_name)
				break
			else:
				yield (node.value, 'no_match')
		
	def visit_category(self, node):
		for child in node.childs:
			category_match = self.visit(child)
			if category_match:
				yield node.value
				break
			else:
				yield False
			
	def visit_boolean(self, node):
		if node.value == 'and':
			for child in node.childs:
				result = self.visit(child)
				if not result:
					yield result
					break
			else:
				yield True
		else:
		# node.value = "or"
			for child in node.childs:
				result = self.visit(child)
				if result:
					yield result
					break
			else:
				yield False

	def visit_selector(self, node):
		return self.get_url_component(node.value)
		
	def visit_pattern(self, node):
		selector = yield node.childs[0]
		yield node.value.match(selector)