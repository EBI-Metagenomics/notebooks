
describe('Shiny Proxy launcher', () => {
  beforeAll(async () => {
    await page.goto('http://127.0.0.1:8080')
  })

  it('should display mgnify app', async () => {
    await expect(page).toMatch('EMBL-EBI MGnify | Jupyter Notebook Lab')
    await page.screenshot({ path: 'shiny_proxy_launched.png' })
  })
})

describe('Jupyter Lab launcher', () => {
  jest.setTimeout(20000)
  let frame

  beforeAll(async () => {
    await page.goto('http://127.0.0.1:8080/app/mgnify-notebook-lab')
    await page.screenshot({ path: 'launching_jl.png' })
    const frameHandle = await page.waitForSelector('iframe')
    frame = await frameHandle.contentFrame();
    await frame.waitForSelector('.jp-Launcher')
  })

  it ('should show python and R in launcher', async () => {
    await expect(frame).toMatch('Python 3 (ipykernel)')
    await expect(frame).toMatch('R file')
  })
})

describe('Deep-linking to a notebook', () => {
  jest.setTimeout(20000)
  let frame

  beforeAll(async () => {
    await page.goto('http://127.0.0.1:8080/app/mgnify-notebook-lab?jlpath=mgnify-examples/home.ipynb', {waitUntil: 'networkidle2'})
    const frameHandle = await page.waitForSelector('iframe')
    frame = await frameHandle.contentFrame();
    await frame.waitForSelector('#main')
  })

  it ('should be showing Home notebook content', async () => {
    await expect(frame).toMatch('Examples using Python and R to access data from MGnify', {timeout: 20000})
  })

})

describe('Environment variable insertion', () => {
  jest.setTimeout(20000)
  let frame

  beforeAll(async () => {
    await page.goto('http://127.0.0.1:8080/app/mgnify-notebook-lab?jlvar_TEST=TESTYMCTESTERSON', {waitUntil: 'networkidle2'})
    const frameHandle = await page.waitForSelector('iframe')
    frame = await frameHandle.contentFrame();
    await frame.waitForSelector('.jp-Launcher')
    const simpleModeSwitch = await frame.waitForSelector('button.jp-switch')
    await simpleModeSwitch.evaluate(b => b.click());
  })

  it ('should have env var available in new python kernel', async () => {
    const launcherOpener = await frame.waitForSelector('button[title^="New Launcher"]')
    await launcherOpener.click()
    await frame.waitForSelector('.jp-Launcher')
    const consoleOpener = await frame.waitForSelector('div[title= "Python 3 (ipykernel)"][data-category="Console"]')
    await consoleOpener.evaluate(b => b.click());

    await frame.waitForNavigation({
      waitUntil: 'networkidle2',
    });
    
    await expect(frame).toMatch("Type '?' for help.", {timeout: 20000})  // Python loaded

    const codeInput = await frame.waitForSelector('.jp-CodeConsole-input')
    await frame.type('.jp-CodeConsole-input', "import os; os.getenv('TEST')")
    await page.keyboard.down('Shift')
    await page.keyboard.press('Enter')
    await page.keyboard.up('Shift')

    await expect(frame).toMatch('TESTYMCTESTERSON')

  })

  it ('should have env var available in new R kernel', async () => {
    const launcherOpener = await frame.waitForSelector('button[title^="New Launcher"]')
    await launcherOpener.click()
    const consoleOpener = await frame.waitForSelector('div[title= "R"][data-category="Console"]')
    await consoleOpener.evaluate(b => b.click());

    await frame.waitForNavigation({
      waitUntil: 'networkidle2',
    });
    
    await expect(frame).toMatch("R version", {timeout: 20000})  // R loaded

    const codeInput = await frame.waitForSelector('.jp-CodeConsole-input')
    await frame.type('.jp-CodeConsole-input', "Sys.getenv('TEST', unset = NA)")
    await page.keyboard.down('Shift')
    await page.keyboard.press('Enter')
    await page.keyboard.up('Shift')

    await expect(frame).toMatch('TESTYMCTESTERSON')

  })

})

