#!encoding=utf8

import random, sys, math


def main():
	field_name_list = []
	data_dict = {}

	fin = open('iris.txt', 'r')
	HEAD = True
	for line in fin:
		tokens	= line.rstrip().split('\t')
		if HEAD:
			field_name_list = tokens
			HEAD = False
			continue

		DataNum		= int(tokens[0])
		SepalLength	= float(tokens[1])
		SepalWidth	= float(tokens[2])
		PetalLength	= float(tokens[3])
		PetalWidth	= float(tokens[4])
		Species		= tokens[5]

		FeatureList	= [SepalLength, SepalWidth, PetalLength, PetalWidth]

		data_dict[DataNum] = {}
		data_dict[DataNum]["FeatureList"] 	= FeatureList
		data_dict[DataNum]["Species"] 		= Species
	fin.close()

	kmeans(data_dict, knums=3, dim=4)


def kmeans(data_dict, knums=3, dim=4):
	## 초기화
	center_dict = {}
	for center_number in range(1, knums+1):
		center_dict[center_number] = {}
		## center_dict[center_number]["center_vector"]	= data_dict[center_number]["FeatureList"][:]
		center_dict[center_number]["center_vector"]	= data_dict[random.randint(1, 150)]["FeatureList"][:]
		center_dict[center_number]["count"] 		= 0

	maxIterations = 1
	for i in range(maxIterations):

		## reassign the center
		for DataNum, DataInfo in data_dict.iteritems():
			new_center_number 	= 0
			new_distance_squared	= sys.float_info.max
			## 해당 데이터가 어느 센터에 가까운지를 평가하고 센터 번호를 부여한다
			for center_number in range(1, knums+1):
				first 	= data_dict[DataNum]["FeatureList"]
				second 	= center_dict[center_number]["center_vector"]
				distance_squared = sum([(x-y)*(x-y) for x, y in zip(first, second)])

				if distance_squared < new_distance_squared:
					new_center_number 		= center_number
					new_distance_squared 	= distance_squared
			## print new_center_number
			DataInfo["center_number"] = new_center_number
			data_dict[DataNum] = DataInfo
					

		for center_number in range(1, knums+1):
			center_dict[center_number]["count"]	= 0

		## 센터를 재계산하자
		for DataNum, DataInfo in data_dict.iteritems():
			center_number = DataInfo["center_number"]
			first 	= center_dict[center_number]["center_vector"]
			second 	= DataInfo["FeatureList"]
			center_vector = [x + y for x, y in zip(first, second)]
			center_dict[center_number]["center_vector"] = center_vector

			center_dict[center_number]["count"] += 1

		## update center
		for center_number in range(1, knums+1):
			first = center_dict[center_number]["center_vector"]
			count = center_dict[center_number]["count"]
			second = [count] * dim
			center_dict[center_number]["center_vector"] = [x / float(y) for x, y in zip(first, second)]

	for DataNum in range(1, len(data_dict)+1):
		FeatureList		= data_dict[DataNum]["FeatureList"]
		Species			= data_dict[DataNum]["Species"]
		center_number 	= data_dict[DataNum]["center_number"]
		print '%s\t%s\t%s' % (DataNum, Species, center_number)

	print
	for center_number in range(1, knums+1):
		print '%s\t%s' % (center_number, center_dict[center_number])



def main_online():
	field_name_list = []
	data_dict = {}

	fin = open('iris.txt', 'r')
	HEAD = True
	for line in fin:
		tokens	= line.rstrip().split('\t')
		if HEAD:
			field_name_list = tokens
			HEAD = False
			continue

		DataNum		= int(tokens[0])
		SepalLength	= float(tokens[1])
		SepalWidth	= float(tokens[2])
		PetalLength	= float(tokens[3])
		PetalWidth	= float(tokens[4])
		Species		= tokens[5]

		FeatureList	= [SepalLength, SepalWidth, PetalLength, PetalWidth]

		data_dict[DataNum] = {}
		data_dict[DataNum]["FeatureList"] 	= FeatureList
		data_dict[DataNum]["Species"] 		= Species
	fin.close()

	kmeans_online(data_dict, knums=3, dim=4)



def kmeans_online(data_dict, knums=3, dim=4):
	## 초기화
	center_dict = {}
	for center_number in range(1, knums+1):
		center_dict[center_number] = {}
		## center_dict[center_number]["center_vector"]	= data_dict[center_number]["FeatureList"][:]
		center_dict[center_number]["center_vector"]	= data_dict[random.randint(1, 150)]["FeatureList"][:]
		center_dict[center_number]["count"] 		= 0

	maxIterations = 1
	for i in range(maxIterations):
		for center_number in range(1, knums+1):
			center_dict[center_number]["count"]	= 0

		## reassign the center
		for DataNum, DataInfo in data_dict.iteritems():
			new_center_number 	= 0
			new_distance_squared	= sys.float_info.max
			## 해당 데이터가 어느 센터에 가까운지를 평가하고 센터 번호를 부여한다
			for center_number in range(1, knums+1):
				first 	= data_dict[DataNum]["FeatureList"]
				second 	= center_dict[center_number]["center_vector"]
				distance_squared = sum([(x-y)*(x-y) for x, y in zip(first, second)])

				if distance_squared < new_distance_squared:
					new_center_number 		= center_number
					new_distance_squared 	= distance_squared
			## print new_center_number
			DataInfo["center_number"] = new_center_number
			data_dict[DataNum] = DataInfo
			center_dict[new_center_number]["count"] += 1

					
			## 센터를 재계산하자
			center_number 	= DataInfo["center_number"]
			eta 			= 1.0/center_dict[center_number]["count"]
			first			= center_dict[center_number]["center_vector"]
			second			= DataInfo["FeatureList"]

			center_vector = [(1.0-eta) * x + eta * y for x, y in zip(first, second)]
			center_dict[center_number]["center_vector"] = center_vector


	## reassign the center
	for DataNum, DataInfo in data_dict.iteritems():
		new_center_number 	= 0
		new_distance_squared	= sys.float_info.max
		## 해당 데이터가 어느 센터에 가까운지를 평가하고 센터 번호를 부여한다
		for center_number in range(1, knums+1):
			first 	= data_dict[DataNum]["FeatureList"]
			second 	= center_dict[center_number]["center_vector"]
			distance_squared = sum([(x-y)*(x-y) for x, y in zip(first, second)])

			if distance_squared < new_distance_squared:
				new_center_number 		= center_number
				new_distance_squared 	= distance_squared
		## print new_center_number
		DataInfo["center_number"] = new_center_number
		data_dict[DataNum] = DataInfo


	for DataNum in range(1, len(data_dict)+1):
		FeatureList		= data_dict[DataNum]["FeatureList"]
		Species			= data_dict[DataNum]["Species"]
		center_number 	= data_dict[DataNum]["center_number"]
		print '%s\t%s\t%s' % (DataNum, Species, center_number)

	print
	for center_number in range(1, knums+1):
		print '%s\t%s' % (center_number, center_dict[center_number])



def main_cosine():
	field_name_list = []
	data_dict = {}

	fin = open('iris.txt', 'r')
	HEAD = True
	for line in fin:
		tokens	= line.rstrip().split('\t')
		if HEAD:
			field_name_list = tokens
			HEAD = False
			continue

		DataNum		= int(tokens[0])
		SepalLength	= float(tokens[1])
		SepalWidth	= float(tokens[2])
		PetalLength	= float(tokens[3])
		PetalWidth	= float(tokens[4])
		Species		= tokens[5]

		FeatureList	= [SepalLength, SepalWidth, PetalLength, PetalWidth]
		FeatureNorm = math.sqrt(sum(map(lambda x: x*x, FeatureList)))

		data_dict[DataNum] = {}
		data_dict[DataNum]["FeatureList"] 	= [x / float(y) for x, y in zip(FeatureList, [FeatureNorm]*len(FeatureList))]
		data_dict[DataNum]["Species"] 		= Species
	fin.close()

	kmeans_cosine(data_dict, knums=3, dim=4)


def kmeans_cosine(data_dict, knums=3, dim=4):
	## 초기화
	center_dict = {}
	for center_number in range(1, knums+1):
		center_dict[center_number] = {}
		## center_dict[center_number]["center_vector"]	= data_dict[center_number]["FeatureList"][:]
		center_dict[center_number]["center_vector"]	= data_dict[random.randint(1, 150)]["FeatureList"][:]
		center_dict[center_number]["count"] 		= 0

	maxIterations = 1
	for i in range(maxIterations):

		## reassign the center
		for DataNum, DataInfo in data_dict.iteritems():
			new_center_number 		= 0
			new_cosine_similarity	= -sys.float_info.max
			## 해당 데이터가 어느 센터에 가까운지를 평가하고 센터 번호를 부여한다
			for center_number in range(1, knums+1):
				first 	= data_dict[DataNum]["FeatureList"]
				second 	= center_dict[center_number]["center_vector"]

				cosine_similarity = sum([ x*y for x, y in zip(first, second) ])

				if cosine_similarity > new_cosine_similarity:
					new_center_number 		= center_number
					new_cosine_similarity 	= cosine_similarity
			## print new_center_number
			DataInfo["center_number"] = new_center_number
			data_dict[DataNum] = DataInfo
					

		for center_number in range(1, knums+1):
			center_dict[center_number]["count"]	= 0

		## 센터를 재계산하자
		for DataNum, DataInfo in data_dict.iteritems():
			center_number = DataInfo["center_number"]
			first 	= center_dict[center_number]["center_vector"]
			second 	= DataInfo["FeatureList"]
			center_vector = [x + y for x, y in zip(first, second)]
			center_dict[center_number]["center_vector"] = center_vector

			center_dict[center_number]["count"] += 1

		## update center
		for center_number in range(1, knums+1):
			first = center_dict[center_number]["center_vector"]
			second = [math.sqrt(sum(map(lambda x: x*x, first)))] * dim
			center_dict[center_number]["center_vector"] = [x / float(y) for x, y in zip(first, second)]
			## count = center_dict[center_number]["count"]
			## second = [count] * dim
			## center_dict[center_number]["center_vector"] = [x / float(y) for x, y in zip(first, second)]

	for DataNum in range(1, len(data_dict)+1):
		FeatureList		= data_dict[DataNum]["FeatureList"]
		Species			= data_dict[DataNum]["Species"]
		center_number 	= data_dict[DataNum]["center_number"]
		print '%s\t%s\t%s' % (DataNum, Species, center_number)

	print
	for center_number in range(1, knums+1):
		print '%s\t%s' % (center_number, center_dict[center_number])

			
if __name__=='__main__':
	## main()
	## main_online()
	main_cosine()




