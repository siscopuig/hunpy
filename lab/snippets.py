# Convert list of tuples in list using a list comprehension

fruits = [(1, ), (2, ), (3, )]
array = [i[0] for i in fruits]
print(array)


########################################################################################################

module_name = 'body_processor'
class_name = ''

for name_part in module_name.split('_'):  # splits body_processor ['body', 'processor']

	# Appending string, uppercase first character([name_part[:1]) +
	# print('First char: ', name_part[:1].upper())  # Displays first string character
	# print('String: ', name_part[1:])  # Displays string except first char

	class_name += ''.join([name_part[:1].upper() + name_part[1:]])  # 1: 'Body', 2: 'Processor'

# Output:	class_name = 'BodyProcessor'



# Using list comprehension
classname = ''.join([name_part[:1].upper() + name_part[1:] for name_part in module_name.split('_')])
# Output:	BodyProcessor

########################################################################################################
