require('dotenv').config();
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs').promises;
const CronJob = require('cron').CronJob;

var id = process.env.ID
var duration = process.env.DURATION

const job = new CronJob('55 23 00 * * *', function() {

    axios.get(`https://www.walsall.gov.uk/Waste/bincollections/Details/${id}${duration}`)
        .then((response) => {
            if(response.status === 200) {
                const html = response.data;
                const $ = cheerio.load(html);
                const scrapedData = [];

                // Grey Bin (General waste)
                $("div#main > table:nth-of-type(1) > tbody > tr").each((index, element) => {        
                    if (index === 0) return true;
                    const tds = $(element).find('td');
                    const bin = $('div#main').find('h3:nth-child(2)').text().trim()
                    const day = $(tds[0]).text().replace(/(\r\n|\n|\r)/gm,"").trim();
                    const date = $(tds[1]).text().replace(/(\r\n|\n|\r)/gm,"").trim();
                    const tableRow = { bin, day, date };
                    scrapedData.push(tableRow);
                });

                // 240Ltr Green Bin (Recycling)
                $("div#main > table:nth-of-type(2) > tbody > tr").each((index, element) => {        
                    if (index === 0) return true;
                    const tds = $(element).find('td');
                    const bin = $('div#main').find('h3:nth-child(4)').text().trim()
                    const day = $(tds[0]).text().replace(/(\r\n|\n|\r)/gm,"").trim();
                    const date = $(tds[1]).text().replace(/(\r\n|\n|\r)/gm,"").trim();
                    const tableRow = { bin, day, date };
                    scrapedData.push(tableRow);
                });

                // 240Ltr Brown Bin (Garden waste)
                $("div#main > table:nth-of-type(3) > tbody > tr").each((index, element) => {        
                    if (index === 0) return true;
                    const tds = $(element).find('td');
                    const bin = $('div#main').find('h3:nth-child(6)').text().trim()
                    const day = $(tds[0]).text().replace(/(\r\n|\n|\r)/gm,"").trim();
                    const date = $(tds[1]).text().replace(/(\r\n|\n|\r)/gm,"").trim();
                    const tableRow = { bin, day, date };
                    scrapedData.push(tableRow);
                });
                return fs.writeFile('binDates.json', 
                JSON.stringify(scrapedData, null, 4)
                )}
            })
        .then(() => {
            console.log('Saved');
        })
        .catch((error) => {
            console.error(`Could not save: ${error}`);
        });

});

job.start();