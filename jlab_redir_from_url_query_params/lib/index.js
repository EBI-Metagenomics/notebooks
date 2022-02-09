module.exports = [
  {
    id: 'jlab_redir_from_url_query_params',
    autoStart: true,
    activate: function (app) {
      const queryParams = Array.from(new URLSearchParams(window.location.search)).reduce((o, i) => ({ ...o, [i[0]]: i[1] }), {});
      if ('notebook' in queryParams) {
        window.location.assign(window.location.origin + window.location.pathname + '/tree/mgnify-examples/' + queryParams.notebook);
      }
    }
  }
];
