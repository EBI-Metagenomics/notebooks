module.exports = {
  launch: {
    headless: true,
    dumpio: true,
    product: 'chrome',
  },
  browserContext: 'default',
  server: {
    command: "cd ../shiny-proxy; java -jar shinyproxy-2.6.1.jar",
    port: 8080,
    launchTimeout: 180000,
    debug: true
  },
};