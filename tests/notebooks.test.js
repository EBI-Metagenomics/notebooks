
describe('Shiny Proxy launcher', () => {
  jest.retryTimes(3, {logErrorsBeforeRetry: true})

  beforeAll(async () => {
    await page.goto('http://127.0.0.1:8080')
  })

  it('should display mgnify app', async () => {
    await expect(await page.content()).toMatch('EMBL-EBI MGnify | Jupyter Notebook Lab')
    await page.screenshot({ path: 'shiny_proxy_launched.png' })
  })
})

describe('Jupyter Lab launcher', () => {
  jest.setTimeout(30000)
  jest.retryTimes(3, {logErrorsBeforeRetry: true})

  let frame

  beforeEach(async () => {
    await page.goto('http://127.0.0.1:8080/app/mgnify-notebook-lab', {waitUntil: 'networkidle2'})
    await page.screenshot({ path: 'launching_jl.png' })
    const frameHandle = await page.waitForSelector('iframe')
    frame = await frameHandle.contentFrame();
    await frame.waitForSelector('.jp-Launcher')
    await page.screenshot({ path: 'jl_launched.png' })
  })

  it('should show python and R in launcher', async () => {
    await expect(await frame.content()).toMatch('Python')
    await expect(await frame.content()).toMatch('R file')
  })
})

describe('Deep-linking to a notebook', () => {
  jest.setTimeout(60000)
  jest.retryTimes(3, {logErrorsBeforeRetry: true})

  let frame

  beforeAll(async () => {
    await page.goto('http://127.0.0.1:8080/app/mgnify-notebook-lab?jlpath=mgnify-examples/home.ipynb', {waitUntil: 'networkidle2'})
    const frameHandle = await page.waitForSelector('iframe')
    frame = await frameHandle.contentFrame();
    await frame.waitForSelector('.jp-NotebookPanel-toolbar')
    await page.screenshot({ path: 'home_notebook.png' })
  }, 60000)

  it('should be showing Home notebook content', async () => {
    await expect(await frame.content()).toMatch('Examples using Python and R to access data from MGnify', {timeout: 20000})
  })

})

describe.skip('Environment variable insertion', () => {
  jest.setTimeout(40000)
  jest.retryTimes(1, {logErrorsBeforeRetry: true})
  
  let frame

  beforeEach(async () => {
    await page.goto('http://127.0.0.1:8080/app/mgnify-notebook-lab?jlvar_TEST=TESTYMCTESTERSON', {waitUntil: 'networkidle2'})
    const frameHandle = await page.waitForSelector('#shinyframe')
    frame = await frameHandle.contentFrame();
    const simpleModeSwitch = await frame.waitForSelector('button.jp-switch')
    await simpleModeSwitch.evaluate(b => b.click());
  }, 40000)

  it('should have env var available in new python kernel', async () => {
    const launcherOpener = await frame.waitForSelector('jp-button[title^="New Launcher"]')
    await launcherOpener.click()
    await page.waitForSelector('.jp-Launcher')
    const consoleOpener = await frame.waitForSelector('div[title= "Python 3 (ipykernel)"][data-category="Console"]')
    await consoleOpener.evaluate(b => b.click());

    await frame.waitForNavigation({
      waitUntil: 'networkidle2',
    });
    
    await expect(await frame.content()).toMatch("Type '?' for help.", {timeout: 20000})  // Python loaded

    const codeInput = await frame.waitForSelector('.jp-CodeConsole-input')
    await frame.type('.jp-CodeConsole-input', "import os; os.getenv('TEST')")
    await page.keyboard.down('Shift')
    await page.keyboard.press('Enter')
    await page.keyboard.up('Shift')

    await expect(await frame.content()).toMatch('TESTYMCTESTERSON')

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

