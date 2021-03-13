
exports.scraper = async (browser) => {

    const page = await browser.newPage();
    await page.goto('https://jobs.bdjobs.com/jobsearch.asp?fcatId=8&icatId=', {waitUntil: 'load', timeout: 0});
    let hrefs1 = await page.evaluate(
        () => Array.from(
            document.querySelectorAll('a[href]'),
            a => {
                const link = a.getAttribute('href');
                return link
            }
        )
    );
    let joblinks = hrefs1.filter(name => name.includes('jobdetails.asp?id='));
    for (let i = 2; i < 3; i++) {
        let path = `//*[@id="bottomPagging"]/ul/li[${i}]/a`;
        await page.waitFor(15000);
        const linkHandlers = await page.$x(path);

        if (linkHandlers.length > 0) {
            await linkHandlers[0].click();
            hrefs1 = await page.evaluate(
                () => Array.from(
                    document.querySelectorAll('a[href]'),
                    a => {
                        const link = a.getAttribute('href');
                        return link
                    }
                )
            );
            // console.log(hrefs1.filter(name => name.includes('jobdetails.asp?id=')))
            joblinks = joblinks.concat(hrefs1.filter(name => name.includes('jobdetails.asp?id=')));
        } else {
            throw new Error("Link not found");
        }
    }

    return  joblinks
};
