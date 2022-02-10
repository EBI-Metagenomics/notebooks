import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { requestAPI } from './handler';

/**
 * Initialization data for the shiny-proxy-jlab-query-parms extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'shiny-proxy-jlab-query-parms:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension shiny-proxy-jlab-query-parms is activated!');

    const queryParams = new URLSearchParams(window.location.search);

    if (queryParams.has('jlpath')) {
      window.location.assign(window.location.origin + window.location.pathname + '/tree/' + queryParams.get('jlpath'));
    }

    requestAPI<any>('set_env_vars', { method: 'POST', body: queryParams })
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The shiny_proxy_jlab_query_parms server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
