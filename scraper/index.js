const chromium = require('chrome-aws-lambda')
const extractor = require('./extractor')
const s3uploader = require('./s3_uploader')
exports.handler = async (event) => {
  const browser = await chromium.puppeteer.launch({
    args: chromium.args,
    defaultViewport: chromium.defaultViewport,
    executablePath: await chromium.executablePath,
    headless: chromium.headless,
    headless: true,
    ignoreHTTPSErrors: true
  })
  JobLinks = await extractor.scraper(browser)
  await browser.close()
  s3uploader.upload(JobLinks)
}
