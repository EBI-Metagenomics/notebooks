import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { requestAPI } from './handler';

/**
 * Initialization data for the jlab_query_params extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jlab_query_params:plugin',
  description: 'JupyterLab extension to set environment variables and support deep-links via query parameters.',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jlab_query_parms is activated!');

    const queryParams = new URLSearchParams(window.location.search);

    if (queryParams.has('jlpath')) {
      window.location.assign(window.location.origin + window.location.pathname + '/tree/' + queryParams.get('jlpath'));
    }

    requestAPI<any>('set-env-vars', { method: 'POST', body: queryParams })
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The jlab_query_parms server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
