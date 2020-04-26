/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-2bzp453o.eu', // the auth0 domain prefix
    audience: 'barista', // the audience set for the auth0 app
    clientId: 'UrkzA1M0g6eaRncDiGkmmidre6ynV0Ec', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application.
  }
};
