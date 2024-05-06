# SquaredleSolver
Solves game posted on squaredle.app.

  You are given a board containing english letters, usually it looks like square 4x4 (sometimes 5x5) and your goal is to get highest possible score. You have to find various words in it by dragging through cells. You can move to adjacent cell if it's not visited and you can move to it horizontally, vertically or diagonally for one tile. Some words are considered as bonus words and they are not counted in the game score. Longer words gives your more points and you can input only words with len greater than 3.
  
  My app is simple. I have file that contains english words (NSWL2023). I use puppeteer (python library) that helps me scrap information from website by imitating user behaviour and using browser. First, I get current board and find all words that I can get. For that I use simple bruteforce dfs solution. State in recursion contains: current cell, visited cells (it's just a number with N * N bits, 1 is visited and 0 not visited) and vertex in trie. Before main dfs I precount words from words.txt in this trie. Using this structure helps me understand when to stop recursion and rollback (that happens when I come to a leaf).
  
  After I've got words that can be found in puzzle I use pyautogui to immitate mouse behaviour by python. However there are still some problems. First is because words are inputed very fast and some of them can accidentically get skipped. Second is that I couldn't manage to get screen coordinates of top left tile and my only choice was to hardcode it.
