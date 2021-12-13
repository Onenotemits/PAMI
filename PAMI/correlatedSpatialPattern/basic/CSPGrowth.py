#  Copyright (C)  2021 Rage Uday Kiran
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#      Copyright (C)  2021 Rage Uday Kiran

#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PAMI.correlatedSpatialPattern.basic import abstract as _ab


class _Node:
    """
        A class used to represent the node of frequentPatternTree

    Attributes:
    ----------
        itemId: int
            storing item of a node
        counter: int
            To maintain the support of node
        parent: node
            To maintain the parent of every node
        child: list
            To maintain the children of node
        nodeLink : node
            Points to the node with same itemId

    Methods:
    -------

        getChild(itemName)
            returns the node with same itemName from frequentPatternTree
    """

    def __init__(self):
        self.itemId = -1
        self.counter = 1
        self.parent = None
        self.child = []
        self.nodeLink = None

    def getChild(self, itemName):
        """ Retrieving the child from the tree

            :param itemName: name of the child
            :type itemName: list
            :return: returns the node with same itemName from frequentPatternTree
            :rtype: list

        """
        for i in self.child:
            if i.itemId == itemName:
                return i
        return None


class _Tree:
    """
        A class used to represent the frequentPatternGrowth tree structure

    Attributes:
    ----------
        headerList : list
            storing the list of items in tree sorted in ascending of their supports
        mapItemNodes : dictionary
            storing the nodes with same item name
        mapItemLastNodes : dictionary
            representing the map that indicates the last node for each item
        root : Node
            representing the root Node in a tree

    Methods:
    -------
        createHeaderList(items,minSup)
            takes items only which are greater than minSup and sort the items in ascending order
        addTransaction(transaction)
            creating transaction as a branch in frequentPatternTree
        fixNodeLinks(item,newNode)
            To create the link for nodes with same item
        printTree(Node)
            gives the details of node in frequentPatternGrowth tree
        addPrefixPath(prefix,port,minSup)
           It takes the items in prefix pattern whose support is >=minSup and construct a subtree
    """

    def __init__(self):
        self.headerList = []
        self.mapItemNodes = {}
        self.mapItemLastNodes = {}
        self.root = _Node()

    def addTransaction(self, transaction):
        """adding transaction into tree

        :param transaction: it represents the one transactions in database
        :type transaction: list
        """

        current = self.root
        for i in transaction:
            child = current.getChild(i)
            if not child:
                newNode = _Node()
                newNode.itemId = i
                newNode.parent = current
                current.child.append(newNode)
                self.fixNodeLinks(i, newNode)
                current = newNode
            else:
                child.counter += 1
                current = child

    def fixNodeLinks(self, item, newNode):
        """Fixing node link for the newNode that inserted into frequentPatternTree

        :param item: it represents the item of newNode
        :type item: int
        :param newNode: it represents the newNode that inserted in frequentPatternTree
        :type newNode: Node

        """
        if item in self.mapItemLastNodes.keys():
            lastNode = self.mapItemLastNodes[item]
            lastNode.nodeLink = newNode
        self.mapItemLastNodes[item] = newNode
        if item not in self.mapItemNodes.keys():
            self.mapItemNodes[item] = newNode

    def printTree(self, root):
        """Print the details of Node in frequentPatternTree

        :param root: it represents the Node in frequentPatternTree
        :type root: Node

        """

        # this method is used print the details of tree
        if not root.child:
            return
        else:
            for i in root.child:
                print(i.itemId, i.counter, i.parent.itemId)
                self.printTree(i)

    def createHeaderList(self, mapSupport, minSup):
        """To create the headerList

        :param mapSupport: it represents the items with their supports
        :type mapSupport: dictionary
        :param minSup: it represents the minSup
        :param minSup: float
        """
        t1 = []
        for x, y in mapSupport.items():
            if y >= minSup:
                t1.append(x)
        itemSetBuffer = [k for k, v in sorted(mapSupport.items(), key=lambda x: x[1], reverse=True)]
        self.headerList = [i for i in t1 if i in itemSetBuffer]

    def addPrefixPath(self, prefix, mapSupportBeta, minSup):
        """To construct the conditional tree with prefix paths of a node in frequentPatternTree

        :param prefix: it represents the prefix items of a Node
        :type prefix: list
        :param mapSupportBeta: it represents the items with their supports
        :param mapSupportBeta: dictionary
        :param minSup: to check the item meets with minSup
        :param minSup: float
        """
        pathCount = prefix[0].counter
        current = self.root
        prefix.reverse()
        for i in range(0, len(prefix) - 1):
            pathItem = prefix[i]
            if mapSupportBeta.get(pathItem.itemId) >= minSup:
                child = current.getChild(pathItem.itemId)
                if not child:
                    newNode = _Node()
                    newNode.itemId = pathItem.itemId
                    newNode.parent = current
                    newNode.counter = pathCount
                    current.child.append(newNode)
                    current = newNode
                    self.fixNodeLinks(pathItem.itemId, newNode)
                else:
                    child.counter += pathCount
                    current = child


class CSPGrowth(_ab._correlatedPatterns):
    """ 
        CSGrowth correlated algorithm is to discover the spatially correlated patterns from the database

    Attributes:
    ---------
        iFile : file
            Name of the Input file to mine complete set of frequent patterns
        oFile : file
            Name of the output file to store complete set of frequent patterns
        memoryUSS : float
            To store the total amount of USS memory consumed by the program
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTime:float
            To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
        minSup : float
            The user given minSup
        Database : list
            To store the transactions of a database in list
        mapSupport : Dictionary
            To maintain the information of item and their frequency
        lno : int
            it represents the total no of transactions
        tree : class
            it represents the Tree class
        itemSetCount : int
            it represents the total no of patterns
        finalPatterns : dict
            it represents to store the patterns
        itemSetBuffer : list
            it represents the store the items in mining
        maxPatternLength : int
           it represents the constraint for pattern length
        minSup: float
            user defined minimum support
        minAllConf: float
           user defined minimum ratio

    Methods:
    -------
        startMine()
            Mining process will start from here
        getPatterns()
            Complete set of patterns will be retrieved with this function
        savePatterns(oFile)
            Complete set of frequent patterns will be loaded in to a output file
        getPatternsAsDataFrame()
            Complete set of frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function
        check(line)
            To check the delimiter used in the user input file
        creatingItemSets(fileName)
            Scans the dataset or dataframes and stores in list format
        frequentOneItem()
            Extracts the one-frequent patterns from transactions
        saveAllCombination(tempBuffer,s,position,prefix,prefixLength)
            Forms all the combinations between prefix and tempBuffer lists with support(s)
        saveItemSet(pattern,support)
            Stores all the frequent patterns with their respective support
        frequentPatternGrowthGenerate(frequentPatternTree,prefix,port)
            Mining the frequent patterns by forming conditional frequentPatternTrees to particular prefix item.
            mapSupport represents the 1-length items with their respective support
        mapNeighbours(nFile):
            to map the items to their Neighbours
        getNeighbourItems(item):
            to get get neighbours of a item

    Executing the code on terminal:
    -------
        Format:
        -------
        python3 CSPGrowth.py <inputFile> <outputFile> <neighbourFile> <minSup> <minAllConf> <sep>

        Examples:
        ---------
        python3 CSPGrowth.py sampleTDB.txt output.txt sampleN.txt 0.25 0.2  (minSup will be considered in percentage of database transactions)
        python3 CSPGrowth.py sampleTDB.txt output.txt sampleN.txt 4  0.2  (minSup will be considered in support count or frequency)
                                                                    (it will consider "\t" as a separator)
        python3 CSPGrowth.py sampleTDB.txt output.txt sampleN.txt 0.25 0.2 ,
                                                                    (it will consider ',' as a separator)

    Sample run of the importing code:
    -----------
        import CSGrowth as alg

        obj = alg.CSGrowth(iFile,nFile,minSup,minAllConf)

        obj.startMine()

        correlatedPatterns = obj.getPatterns()

        print("Total number of correlated spatial frequent Patterns:", len(correlatedPatterns))

        obj.savePatterns(oFile)

        Df = obj.getPatternInDf()

        memUSS = obj.getMemoryUSS()

        print("Total Memory in USS:", memUSS)

        memRSS = obj.getMemoryRSS()

        print("Total Memory in RSS", memRSS)

        run = obj.getRuntime()

        print("Total ExecutionTime in seconds:", run)

    Credits:
    -------
        The complete program was written by B.Sai Chitra  under the supervision of Professor Rage Uday Kiran.

        """

    _startTime = float()
    _endTime = float()
    _minSup = str()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _nFile = " "
    _minAllConf = 0.0
    _memoryUSS = float()
    _memoryRSS = float()
    _Database = []
    _mapSupport = {}
    _lno = 0
    _tree = _Tree()
    _itemSetBuffer = None
    _fpNodeTempBuffer = []
    _itemSetCount = 0
    _maxPatternLength = 1000
    _sep = "\t"
    _neighboursMap = {}

    def __init__(self, iFile, nFile, minSup, minAllConf, sep="\t"):
        super().__init__(iFile, nFile, minSup, minAllConf, sep)

    def _creatingItemSets(self):
        """
            Storing the complete transactions of the database/input file in a database variable


            """
        self._Database = []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._Database = self._iFile['Transactions'].tolist()

        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    self._Database.append(temp)
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            self._Database.append(temp)
                except IOError:
                    print("File Not Found")
                    quit()

    def _mapNeighbours(self):
        """
            A function to map items to their Neighbours
        """
        self._neighboursMap = {}
        if isinstance(self._nFile, _ab._pd.DataFrame):
            data, items = [], []
            if self._nFile.empty:
                print("its empty..")
            i = self._nFile.columns.values.tolist()
            if 'items' in i:
                items = self._nFile['items'].tolist()
            if 'Neighbours' in i:
                data = self._nFile['neighbours'].tolist()
            for k in range(len(data)):
                self._neighboursMap[items[k]] = data[k]
        if isinstance(self._nFile, str):
            if _ab._validators.url(self._nFile):
                data = _ab._urlopen(self._nFile)
                for line in data:
                    line.strip()
                    line = line.decode("utf-8")
                    temp = [i.rstrip() for i in line.split(self._sep)]
                    temp = [x for x in temp if x]
                    item = temp[0]
                    nibs = temp[1:]
                    self._neighboursMap[item] = nibs
            else:
                try:
                    with open(self._nFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line.strip()
                            temp = [i.rstrip() for i in line.split(self._sep)]
                            temp = [x for x in temp if x]
                            item = temp[0]
                            nibs = temp[1:]
                            self._neighboursMap[item] = nibs
                except IOError:
                    print("File Not Found")
                    quit()

    def _getNeighbourItems(self, keySet):
        """
            A function to get Neighbours of a item
            :param keySet:itemSet
            :type keySet:str or tuple
            :return: set of common neighbours 
            :rtype:set
         """
        return self._neighboursMap.get(keySet)

    def _frequentOneItem(self):
        """Generating One frequent items sets

        """
        self._mapSupport = {}
        for i in self._Database:
            for j in i:
                if j not in self._mapSupport:
                    self._mapSupport[j] = 1
                else:
                    self._mapSupport[j] += 1

    def _saveItemSet(self, prefix, prefixLength, support, ratio):
        """To save the frequent patterns mined form frequentPatternTree

        :param prefix: the frequent pattern
        :type prefix: list
        :param prefixLength: the length of a frequent pattern
        :type prefixLength: int
        :param support: the support of a pattern
        :type support:  int
        """

        sample = []
        for i in range(prefixLength):
            sample.append(prefix[i])
        self._itemSetCount += 1
        self._finalPatterns[tuple(sample)] = str(support) + " : " + str(ratio)

    def _getPatternsInDF(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataframe

    def _saveAllCombinations(self, tempBuffer, s, position, prefix, prefixLength):
        """Generating all the combinations for items in single branch in frequentPatternTree

        :param tempBuffer: items in a list
        :type tempBuffer: list
        :param s: support at leaf node of a branch
        :param position: the length of a tempBuffer
        :type position: int
        :param prefix: it represents the list of leaf node
        :type prefix: list
        :param prefixLength: the length of prefix
        :type prefixLength: int
        
        """
        max1 = 1 << position
        for i in range(1, max1):
            commonNeighbours = self._commonitems
            newPrefixLength = prefixLength
            for j in range(position):
                isSet = i & (1 << j)
                if isSet > 0:
                    prefix.insert(newPrefixLength, tempBuffer[j].itemId)
                    newPrefixLength += 1
            ratio = s / self._mapSupport[self._getMaxItem(prefix, newPrefixLength)]
            if ratio >= self._minAllConf:
                self._saveItemSet(prefix, newPrefixLength, s, ratio)

    def _frequentPatternGrowthGenerate(self, frequentPatternTree, prefix, prefixLength, mapSupport, commonNeighbours,
                                      minConf):
        """Mining the fp tree

        :param frequentPatternTree: it represents the frequentPatternTree
        :type frequentPatternTree: class Tree
        :param prefix: it represents a empty list and store the patterns that are mined
        :type prefix: list
        :param param prefixLength: the length of prefix
        :type prefixLength: int
        :param mapSupport : it represents the support of item
        :type mapSupport : dictionary
        """
        singlePath = True
        position = 0
        s = 0
        if len(frequentPatternTree.root.child) > 1:
            singlePath = False
        else:
            currentNode = frequentPatternTree.root.child[0]
            while True:
                if len(currentNode.child) > 1:
                    singlePath = False
                    break
                self._fpNodeTempBuffer.insert(position, currentNode)
                s = currentNode.counter
                position += 1
                if len(currentNode.child) == 0:
                    break
                currentNode = currentNode.child[0]
        if singlePath is True:
            self._saveAllCombinations(self._fpNodeTempBuffer, s, position, prefix, prefixLength)
        else:
            for i in reversed(frequentPatternTree.headerList):
                item = i
                if item not in commonNeighbours or self._neighboursMap.get(item) is None:
                    continue
                newCommonNeighbours = list(set(commonNeighbours).intersection((set(self._neighboursMap.get(item)))))
                support = mapSupport[i]
                low = max(int(_ab._math.floor(mapSupport[i] * self._minAllConf)), self._minSup)
                high = max(int(_ab._math.floor(mapSupport[i] / minConf)), self._minSup)
                betaSupport = support
                prefix.insert(prefixLength, item)
                max1 = self._getMaxItem(prefix, prefixLength)
                if self._mapSupport[max1] < self._mapSupport[item]:
                    max1 = item
                ratio = support / self._mapSupport[max1]
                if ratio >= self._minAllConf:
                    self._saveItemSet(prefix, prefixLength + 1, betaSupport, ratio)
                if prefixLength + 1 < self._maxPatternLength:
                    prefixPaths = []
                    path = frequentPatternTree.mapItemNodes.get(item)
                    mapSupportBeta = {}
                    while path is not None:
                        if path.parent.itemId != -1 or path.parent.itemId in newCommonNeighbours:
                            prefixPath = [path]
                            pathCount = path.counter
                            parent1 = path.parent
                            neighboursTemp = self._commonitems
                            if low <= mapSupport.get(parent1.itemId) <= high:
                                while parent1.itemId != -1 and parent1.itemId in neighboursTemp:
                                    if neighboursTemp is None or self._neighboursMap.get(parent1.itemId) is None:
                                        break
                                    neighboursTemp = list(
                                        set(neighboursTemp).intersection((set(self._neighboursMap.get(parent1.itemId)))))
                                    mins = int(support / max(mapSupport.get(parent1.itemId), support))
                                    if mapSupport.get(parent1.itemId) >= mins:
                                        prefixPath.append(parent1)
                                        if mapSupportBeta.get(parent1.itemId) is None:
                                            mapSupportBeta[parent1.itemId] = pathCount
                                        else:
                                            mapSupportBeta[parent1.itemId] = mapSupportBeta[parent1.itemId] + pathCount
                                        parent1 = parent1.parent
                                    else:
                                        break
                                prefixPaths.append(prefixPath)
                        path = path.nodeLink
                    treeBeta = _Tree()
                    for k in prefixPaths:
                        treeBeta.addPrefixPath(k, mapSupportBeta, self._minSup)
                    if len(treeBeta.root.child) > 0:
                        treeBeta.createHeaderList(mapSupportBeta, self._minSup)
                        self._frequentPatternGrowthGenerate(treeBeta, prefix, prefixLength + 1, mapSupportBeta,
                                                           newCommonNeighbours, minConf)

    def _convert(self, value):
        """
        to convert the type of user specified minSup value
        :param value: user specified minSup value
        :return: converted type
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (len(self._Database) * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (len(self._Database) * value)
            else:
                value = int(value)
        return value

    def startMine(self):
        """main program to start the operation

        """

        self._startTime = _ab._time.time()
        if self._iFile is None:
            raise Exception("Please enter the file path or file name:")
        if self._minSup is None:
            raise Exception("Please enter the Minimum Support")
        self._creatingItemSets()
        self._minSup = self._convert(self._minSup)
        self._commonitems = set()
        self._mapNeighbours()
        self._frequentOneItem()
        self._finalPatterns = {}
        self._mapSupport = {k: v for k, v in self._mapSupport.items() if v >= self._minSup}
        _itemSetBuffer = [k for k, v in sorted(self._mapSupport.items(), key=lambda x: x[1], reverse=True)]
        for i in self._Database:
            _transaction = []
            for j in i:
                if j in _itemSetBuffer:
                    _transaction.append(j)
                    self._commonitems.add(j)
            _transaction.sort(key=lambda val: self._mapSupport[val], reverse=True)
            self._tree.addTransaction(_transaction)
        self._tree.createHeaderList(self._mapSupport, self._minSup)
        if len(self._tree.headerList) > 0:
            self._itemSetBuffer = []
            self._frequentPatternGrowthGenerate(self._tree, self._itemSetBuffer, 0, self._mapSupport, self._commonitems,
                                               self._minAllConf)
        print("Correlated Spatial Frequent Patterns were generated successfully using CSPGrowth algorithm")
        self._endTime = _ab._time.time()
        _process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryRSS = float()
        self._memoryUSS = float()
        self._memoryUSS = _process.memory_full_info().uss
        self._memoryRSS = _process.memory_info().rss

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryRSS

    def _getMaxItem(self, prefix, prefixLength):
        maxItem = prefix[0]
        for i in range(prefixLength):
            if self._mapSupport[maxItem] < self._mapSupport[prefix[i]]:
                maxItem = prefix[i]
        return maxItem

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process


        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataframe = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a, b])
            dataframe = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataframe

    def savePatterns(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            pattern = str()
            for i in x:
                pattern = pattern + i + " "
            s1 = str(pattern) + ": " + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 6 or len(_ab._sys.argv) == 7:
        if len(_ab._sys.argv) == 7:
            _ap = CSPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], float(_ab._sys.argv[5]), _ab._sys.argv[6])
        if len(_ab._sys.argv) == 6:
            _ap = CSPGrowth(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4], float(_ab._sys.argv[5]))
        _ap.startMine()
        _correlatedPatterns = _ap.getPatterns()
        print("Total number of correlated spatial frequent Patterns:", len(_correlatedPatterns))
        _ap.savePatterns(_ab._sys.argv[2])
        _memUSS = _ap.getMemoryUSS()
        print("Total Memory in USS:", _memUSS)
        _memRSS = _ap.getMemoryRSS()
        print("Total Memory in RSS", _memRSS)
        _run = _ap.getRuntime()
        print("Total ExecutionTime in seconds:", _run)
    else:
        '''l = [0.001, 0.002, 0.003, 0.01]
        for i in l:
            ap = CSPGrowth(
                '/Users/Likhitha/Downloads/Datasets/BMS1_itemset_mining.txt',
                '/Users/Likhitha/Downloads/Datasets/bms1_neighbours', i, 0.7, ' ')
            ap.startMine()
            print(ap._minSup, ap._minAllConf, len(ap._Database))
            correlatedPatterns = ap.getPatterns()
            print("Total number of correlated-Frequent Patterns:", len(correlatedPatterns))
            ap.savePatterns('/Users/Likhitha/Downloads/output')
            memUSS = ap.getMemoryUSS()
            print("Total Memory in USS:", memUSS)
            memRSS = ap.getMemoryRSS()
            print("Total Memory in RSS", memRSS)
            run = ap.getRuntime()
            print("Total ExecutionTime in seconds:", run)'''
        print("Error! The number of input parameters do not match the total number of parameters provided")
