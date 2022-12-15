import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette } from '@jupyterlab/apputils';

import { LabIcon } from '@jupyterlab/ui-components';

import mgnifySVG from '../style/icons/mgnify_g.svg';
import mgnifyWordmark from '../style/icons/mgnify_wordmark.png';
import galaxyWordmark from '../style/icons/galaxy.png';

export const mgnifyIcon = new LabIcon({ name: 'mgnify', svgstr: mgnifySVG });

import { BoxPanel, Widget } from '@lumino/widgets';

const SECTION_CLASS = 'jp-RunningSessions-section';
const SECTION_HEADER_CLASS = 'jp-RunningSessions-sectionHeader';
const SECTION_TEXT_CLASS = 'jp-extensionmanager-entry-name';

const extension: JupyterFrontEndPlugin<void> = {
  id: 'mgnify-jupyter-lab-ui:plugin',
  autoStart: true,
  requires: [ICommandPalette],
  activate: async (app: JupyterFrontEnd, palette: ICommandPalette) => {
    console.log('JupyterLab extension mgnify-jupyter-lab-ui is activated!');

    const widget = new BoxPanel({ direction: 'left-to-right', spacing: 0 });
    widget.id = 'mgnify-jupyterlab-help';
    widget.title.icon = mgnifyIcon;
    widget.title.caption = 'MGnify Resources';

    widget.addClass('jp-mgnifyui-view');
    const content = new Widget();
    widget.addWidget(content);

    const helpArea: HTMLElement = (await document.createElement(
      'div'
    )) as HTMLElement;
    helpArea.innerHTML = `
      <div>
        <img src="${mgnifyWordmark}" alt="MGnify resources" class="jp-mgnifyui-wordmark"/>
        <div class="${SECTION_CLASS}">
          <div class="${SECTION_HEADER_CLASS}">
            <h2>MGnify</h2>
          </div>
          <div class="${SECTION_TEXT_CLASS} jp-mgnifyui-section-text">
            <a href="https://www.ebi.ac.uk/metagenomics">MGnify</a>
            is EMBL-EBI's metagenomics resources.
          </div>
        </div>
        
        <div class="${SECTION_CLASS}">
          <div class="${SECTION_HEADER_CLASS}">
            <h2>MGnify's API</h2>
          </div>
          <div class="${SECTION_TEXT_CLASS} jp-mgnifyui-section-text">
            The <a href="https://www.ebi.ac.uk/metagenomics/api">MGnify API</a>
            is the service to programatically access data in MGnify.
            It is a set of URLs that return data in JSON format.
            <br/><br/>
            It can be inspected using a web browser, 
            or called from command line tools
            or scripts written in any language.
          </div>
        </div>
        
        <div class="${SECTION_CLASS}">
          <div class="${SECTION_HEADER_CLASS}">
            <h2>These notebooks</h2>
          </div>
          <div class="${SECTION_TEXT_CLASS} jp-mgnifyui-section-text">
            These notebooks are editable Python and R code, 
            showing common use-cases for MGnify data and how to
            retrieve data from the MGnify API to complete them.
          </div>
        </div>
        
        <div class="${SECTION_CLASS}">
          <div class="${SECTION_HEADER_CLASS}">
            <h2>Galaxy infrastructure</h2>
          </div>
          <div class="${SECTION_TEXT_CLASS} jp-mgnifyui-section-text">
            <img src="${galaxyWordmark}" height="24px" alt="usegalaxy.eu"/><br/>
            The MGnify notebooks are available on
            <a href="https://usegalaxy.eu/root?tool_id=interactive_tool_mgnify_notebook">UseGalaxy.eu</a>.
            This service lets you use, edit, save and resume these notebooks
            in a free cloud computing environment.
          </div>
        </div>
        
        <div class="${SECTION_CLASS}">
          <div class="${SECTION_HEADER_CLASS}">
            <h2>Documentation</h2>
          </div>
          <div class="${SECTION_TEXT_CLASS} jp-mgnifyui-section-text">
            MGnify's  
            <a href="https://docs.mgnify.org">documentation</a>
            describes how to use the API, Notebooks, and MGnify more generally.
            <br/><br/>
            For more help, 
            <a href="https://www.ebi.ac.uk/about/contact/support/metagenomics">contact the MGnify team</a>.
          </div>
        </div>
        
      </div>
    `;
    content.node.appendChild(helpArea);

    await app.shell.add(widget, 'left', { rank: 501 });
    app.shell.activateById(widget.id);

    // Docs
    const docsCommand = 'mgnify:open-resource-docs';
    app.commands.addCommand(docsCommand, {
      label: 'MGnify Documentation',
      caption: 'MGnify Documentation',
      execute: () => {
        window.open('https://docs.mgnify.org', '_newtab');
      }
    });

    // Website
    const webCommand = 'mgnify:open-resource-website';
    app.commands.addCommand(webCommand, {
      label: 'MGnify Website',
      caption: 'MGnify Website',
      execute: () => {
        window.open('https://www.ebi.ac.uk/metagenomics', '_newtab');
      }
    });

    // API
    const apiCommand = 'mgnify:open-resource-api';
    app.commands.addCommand(apiCommand, {
      label: 'MGnify Browsable API',
      caption: 'MGnify Browsable API',
      execute: () => {
        window.open('https://www.ebi.ac.uk/metagenomics/api', '_newtab');
      }
    });

    // Service status
    const statusCommand = 'mgnify:open-resource-status';
    app.commands.addCommand(statusCommand, {
      label: 'MGnify System Status',
      caption: 'MGnify System Status',
      execute: () => {
        window.open('https://status.mgnify.org', '_newtab');
      }
    });

    // Galaxy
    const galaxyCommand = 'mgnify:open-resource-galaxy';
    app.commands.addCommand(galaxyCommand, {
      label: 'Galaxy-hosted Notebooks',
      caption: 'Galaxy-hosted Notebooks',
      execute: () => {
        window.open(
          'https://usegalaxy.eu/root?tool_id=interactive_tool_mgnify_notebook',
          '_newtab'
        );
      }
    });

    palette.addItem({ command: docsCommand, category: 'MGnify' });
    palette.addItem({ command: webCommand, category: 'MGnify' });
    palette.addItem({ command: apiCommand, category: 'MGnify' });
    palette.addItem({ command: galaxyCommand, category: 'MGnify' });
    palette.addItem({ command: statusCommand, category: 'MGnify' });
  }
};

export default extension;
