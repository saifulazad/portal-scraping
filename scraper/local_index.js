const puppeteer = require('puppeteer-core');
const extractor = require("./extractor");
const s3uploader = require("./s3_uploader");
(async ()=> {
  const browser = await puppeteer.launch({executablePath: '/usr/bin/brave-browser', headless: false});
  JobLinks = await extractor.scraper(browser)
  await browser.close();
  s3uploader.upload(JobLinks);
})();
