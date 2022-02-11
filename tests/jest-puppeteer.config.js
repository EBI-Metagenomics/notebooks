module.exports = {
  launch: {
    headless: true
  },
  server: {
    command: "cd ../shiny-proxy; java -jar shinyproxy-2.6.0.jar",
    port: 8080,
    launchTimeout: 180000
  },
  devtools: true
};