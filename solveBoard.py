


LETTERS = 26
MIN_WORD_LEN = 4
MATRIX = []



class Trie:
    class Node:
        def __init__(self):
            self.to = [0] * LETTERS
            self.isWord = False
    def newNode(self):
        self.nodeInd += 1
        self.nodes.append(self.Node())
        return self.nodeInd

    def __init__(self):
        self.nodeInd = 0
        self.nodes = [self.Node()]
        self.root = self.newNode()
    def addWord(self, w):
        v = self.root
        for it in w:
            ch = ord(it) - ord('a')
            if not self.nodes[v].to[ch]:
                self.nodes[v].to[ch] = self.newNode()
            v = self.nodes[v].to[ch]
        self.nodes[v].isWord = True


trie = Trie()




lines = open("./words.txt", "r").readlines()

words = []
for it in lines:
    word = it.split()[0].lower()
    words.append(word)
    trie.addWord(word)




DX = [-1, -1, 0, 1, 1, 1, 0, -1]
DY = [0, 1, 1, 1, 0, -1, -1, -1]

used = dict()
foundWords = []
res = dict()
path = []

def dfs(x, y, mask, v, word):
    key = (x, y, mask, v)
    if key in used: return
    used[key] = True

    vert = x * N + y
    mask |= (1 << vert)
    word += MATRIX[x][y]
    if MATRIX[x][y] == ' ': return
    ch = ord(MATRIX[x][y]) - ord('a')
    v = trie.nodes[v].to[ch]

    if not v: return
    path.append((x, y))

    if trie.nodes[v].isWord and len(word) >= MIN_WORD_LEN:
        res[word] = path.copy()
        foundWords.append(word)

    for i in range(len(DX)):
        nx, ny = x + DX[i], y + DY[i]
        if min(nx, ny) < 0 or max(nx, ny) >= N:
            continue

        to = nx * N + ny
        # this cell is already visited
        if (mask >> to) & 1:
            continue

        dfs(nx, ny, mask, v, word)
    path.pop(len(path) - 1)



def findWordsInTable(matrix):
    global MATRIX, N
    MATRIX = matrix
    N = len(MATRIX)

    print("matrix : ", MATRIX)
    res.clear()
    for i in range(N):
        for j in range(N):
            dfs(i, j, 0, trie.root, "")
    return res





