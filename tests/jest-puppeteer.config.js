module.exports = {
  launch: {
    headless: true,
    dumpio: true

  },
  browser: 'chromium',
  browserContext: 'default',
  server: {
    command: "cd ../shiny-proxy; java -jar shinyproxy-2.6.0.jar",
    port: 8080,
    launchTimeout: 180000,
    debug: true
  },
};