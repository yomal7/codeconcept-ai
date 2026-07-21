#!/usr/bin/env node
/**
 * Renders every slide_*.html file in --dir to a same-named .png, using a
 * single headless Chromium instance for the whole batch (much faster than
 * launching a new browser per slide).
 *
 * Usage: node screenshot.js --dir <slides_dir> --width 1920 --height 1080
 *
 * Respects PUPPETEER_EXECUTABLE_PATH if set (useful in sandboxed/offline
 * environments with a pre-installed Chromium); otherwise uses whatever
 * Chromium `npm install puppeteer` downloaded.
 */
const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");

function parseArgs() {
    const args = process.argv.slice(2);
    const out = {};
    for (let i = 0; i < args.length; i += 2) {
        out[args[i].replace(/^--/, "")] = args[i + 1];
    }
    return out;
}

async function main() {
    const { dir, width, height } = parseArgs();
    if (!dir || !width || !height) {
        console.error("Usage: node screenshot.js --dir <slides_dir> --width <w> --height <h>");
        process.exit(1);
    }

    const files = fs
        .readdirSync(dir)
        .filter((f) => f.endsWith(".html"))
        .sort();

    if (files.length === 0) {
        console.error(`No .html files found in ${dir}`);
        process.exit(1);
    }

    const launchOptions = { headless: true, args: ["--no-sandbox", "--disable-gpu"] };
    if (process.env.PUPPETEER_EXECUTABLE_PATH) {
        launchOptions.executablePath = process.env.PUPPETEER_EXECUTABLE_PATH;
    }

    const browser = await puppeteer.launch(launchOptions);

    try {
        for (const file of files) {
            const htmlPath = path.join(dir, file);
            const pngPath = htmlPath.replace(/\.html$/, ".png");

            const page = await browser.newPage();
            await page.setViewport({ width: Number(width), height: Number(height) });
            await page.goto(`file://${htmlPath}`, { waitUntil: "networkidle0" });
            await page.screenshot({ path: pngPath });
            await page.close();

            console.log(pngPath);
        }
    } finally {
        await browser.close();
    }
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});