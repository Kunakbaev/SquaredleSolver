

import time
import asyncio
import pyautogui
import pyppeteer
import solveBoard

# side of board
N = 4
# website URL
URL = "https://squaredle.app/"

async def main():
    browser = await pyppeteer.launch(
        executablePath='/snap/chromium/2839/usr/lib/chromium-browser/chrome',
        userDataDir="~/snap/chromium/common/chromium/Default",
        headless=False,
        options={'args': ['--disable-gpu', '--disable-setuid-sandbox', '--no-sandbox', '--no-zygote']}
    )

    page = await browser.newPage()
    page.setDefaultNavigationTimeout(0)
    await page.goto(URL)

    board = await page.querySelector("div .board")
    letters = ""
    li = await board.querySelectorAll("div .unnecessaryWrapper")
    cells = [[] for i in range(N)]
    for i in range(len(li)):
        # position of element on web page
        tmp = await page.evaluate("""
        (obj) => {
            var x = obj.offsetLeft;
            var y = obj.offsetTop;
            while (obj.offsetParent) {
                x += obj.offsetParent.offsetLeft;
                y += obj.offsetParent.offsetTop;
                if (obj == document.getElementsByTagName("body")[0])
                    break;
                else
                    obj = obj.offsetParent;
            }
            return {x, y};
        }
        """, li[i])

        # letter that tile represents (can be space)
        ch = await page.evaluate("""(li) => li.textContent""", li[i])
        letters += ch
        cells[i // N].append((tmp['x'], tmp['y']))

    # deleting popups cause they will disturb working with mouse
    await page.evaluate("""
    (sel) => {
        document.querySelectorAll(sel).forEach(el => el.remove())
    }
    """, ".popup")
    await page.evaluate("""
        (sel) => {
            document.querySelectorAll(sel).forEach(el => el.remove())
        }
        """, ".fadeIn")

    matrix = []
    print(letters)
    for i in range(N):
        tmp = letters[N * i: N * (i + 1)].lower()
        matrix.append(tmp)

    X, Y = 545, 430
    # X and Y + position of element on webpage are coordinates
    # of the center of the top left tile of the matrix in the screen
    # BE is distance between center's of two neighbour tiles
    BE = 0
    for i in range(N):
        BE += cells[i][-1][0] - cells[i][0][0]
    BE //= (N * (N - 1))
    wordsInTable = solveBoard.findWordsInTable(matrix)

    # output all found words via mouse lib
    for word, path in wordsInTable.items():
        x, y = path[0]
        pyautogui.moveTo(X + y * BE, Y + x * BE)
        pyautogui.mouseDown()
        # drag mouse along tile that are in path
        for i in range(1, len(path)):
            x, y = path[i]
            pyautogui.moveTo(X + y * BE, Y + x * BE, duration=0.3)
        pyautogui.mouseUp()
    time.sleep(1)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

