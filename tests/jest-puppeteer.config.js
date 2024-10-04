const javaExe = process.env.JAVA_EXE || 'java';
const shinyProxyJar = process.env.SHINY_PROXY_JAR || 'shinyproxy-2.6.1.jar'

module.exports = {
  launch: {
    headless: true,
    dumpio: true,
    browser: 'chrome',
  },
  browserContext: 'default',
  server: {
    command: `cd ../shiny-proxy; ${javaExe} -jar ${shinyProxyJar}`,
    port: 8080,
    launchTimeout: 180000,
    debug: true
  },
};