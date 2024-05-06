

import time
import asyncio
import pyautogui
import pyppeteer
import solveBoard


N = 4
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
    # tmp = await page.evaluate("(board) => board.textContent", board)

    letters = ""
    li = await board.querySelectorAll("div .unnecessaryWrapper")
    cells = [[] for i in range(N)]
    for i in range(len(li)):
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

    # 545 and 430 are coordinates of the center of the top left tile of the matrix in the screen
    # BE is distance between center's of two neighbour tiles
    BE = 0
    for i in range(N):
        BE += cells[i][-1][0] - cells[i][0][0]
    BE //= (N * (N - 1))
    print(BE)
    wordsInTable = solveBoard.findWordsInTable(matrix)
    print(len(wordsInTable))
    for word, path in wordsInTable.items():
        x, y = path[0]
        # print(word, path)
        pyautogui.moveTo(545 + y * BE, 430 + x * BE)
        pyautogui.mouseDown()
        for i in range(1, len(path)):
            x, y = path[i]

            pyautogui.moveTo(545 + y * BE, 430 + x * BE, duration=0.3)
        pyautogui.mouseUp()

        # exit(0)
    time.sleep(1)

    await browser.close()


# while True:
#     print(pyautogui.position())

asyncio.get_event_loop().run_until_complete(main())


